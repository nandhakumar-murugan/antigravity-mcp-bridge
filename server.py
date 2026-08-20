"""
Antigravity & Local System MCP Server Bridge
Exposes system tools, file operations, terminal execution, Antigravity Agent orchestration,
and full cross-client history/session logging to Gemini Spark AND Antigravity over MCP.
"""

import os
import sys
import uuid
import json
import asyncio
import subprocess
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List
from mcp.server.mcpserver import MCPServer

# Initialize MCP Server
mcp = MCPServer(name="Antigravity-System-Bridge")

# In-memory background task tracking
tasks: Dict[str, Dict[str, Any]] = {}

# Default base directory
BASE_DIR = os.path.abspath(os.getcwd())

# Persistent history log file — shared between Gemini Spark and Antigravity
HISTORY_FILE = os.path.join(BASE_DIR, "bridge_history.json")


# ─── History Helpers ─────────────────────────────────────────────────────────

def _load_history() -> List[Dict]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_history(history: List[Dict]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def _log_action(tool: str, inputs: Dict, result: str, source: str = "gemini_spark"):
    history = _load_history()
    history.append({
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "tool": tool,
        "inputs": inputs,
        "result_preview": result[:300] + ("..." if len(result) > 300 else ""),
    })
    # Keep last 500 entries
    _save_history(history[-500:])


# ─── Core Tools ──────────────────────────────────────────────────────────────

@mcp.tool()
def run_system_command(command: str, working_dir: Optional[str] = None, source: Optional[str] = None) -> str:
    """
    Executes a shell/PowerShell command on the local system (e.g. python, npm, git, tests, pip).
    Returns standard output and standard error. Pass source='antigravity' or 'gemini_spark' to tag history.
    """
    target_dir = os.path.abspath(working_dir) if working_dir else BASE_DIR
    try:
        process = subprocess.run(
            command, shell=True, cwd=target_dir,
            capture_output=True, text=True, timeout=180,
        )
        result = f"[Exit Code: {process.returncode}]\n--- STDOUT ---\n{process.stdout}\n--- STDERR ---\n{process.stderr}"
        _log_action("run_system_command", {"command": command, "working_dir": working_dir},
                    result, source or "gemini_spark")
        return result
    except subprocess.TimeoutExpired:
        return "[Error] Command timed out after 180 seconds."
    except Exception as e:
        return f"[Error] Failed to execute command: {str(e)}"


@mcp.tool()
def read_file(file_path: str, source: Optional[str] = None) -> str:
    """
    Reads the content of a file from the local filesystem.
    """
    abs_path = os.path.abspath(file_path if os.path.isabs(file_path) else os.path.join(BASE_DIR, file_path))
    if not os.path.exists(abs_path):
        return f"[Error] File not found: {abs_path}"
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        _log_action("read_file", {"file_path": abs_path}, content, source or "gemini_spark")
        return content
    except Exception as e:
        return f"[Error] Failed to read file: {str(e)}"


@mcp.tool()
def write_file(file_path: str, content: str, source: Optional[str] = None) -> str:
    """
    Creates or overwrites a file on the local filesystem with specified content.
    Automatically creates parent directories if they don't exist.
    """
    abs_path = os.path.abspath(file_path if os.path.isabs(file_path) else os.path.join(BASE_DIR, file_path))
    try:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        result = f"[Success] File written to {abs_path}"
        _log_action("write_file", {"file_path": abs_path, "content_length": len(content)},
                    result, source or "gemini_spark")
        return result
    except Exception as e:
        return f"[Error] Failed to write file: {str(e)}"


@mcp.tool()
def list_directory(directory_path: Optional[str] = None, source: Optional[str] = None) -> str:
    """
    Lists files and directories at the specified path.
    """
    target_dir = os.path.abspath(directory_path if directory_path else BASE_DIR)
    if not os.path.exists(target_dir):
        return f"[Error] Directory not found: {target_dir}"
    try:
        entries = os.listdir(target_dir)
        output = [f"Directory contents of: {target_dir}"]
        for entry in entries:
            full_path = os.path.join(target_dir, entry)
            is_dir = "[DIR] " if os.path.isdir(full_path) else "[FILE]"
            size = os.path.getsize(full_path) if not os.path.isdir(full_path) else "-"
            output.append(f"{is_dir} {entry} ({size} bytes)")
        result = "\n".join(output)
        _log_action("list_directory", {"directory_path": target_dir}, result, source or "gemini_spark")
        return result
    except Exception as e:
        return f"[Error] Failed to list directory: {str(e)}"


@mcp.tool()
async def run_agent_task(prompt: str, workspace_dir: Optional[str] = None, source: Optional[str] = None) -> str:
    """
    Launches an autonomous Antigravity AI agent task using ANTIGRAVITY's credits and models.
    Routes the task into a real Antigravity conversation via message injection.
    Antigravity does the heavy AI lifting — Spark just delegates.
    Returns a task_id to check status via get_agent_status.
    """
    task_id = str(uuid.uuid4())[:8]
    target_dir = os.path.abspath(workspace_dir if workspace_dir else BASE_DIR)

    tasks[task_id] = {
        "task_id": task_id,
        "prompt": prompt,
        "status": "running",
        "output": "",
        "error": None,
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source or "gemini_spark",
        "routed_to": "antigravity",
    }
    _log_action("run_agent_task", {"prompt": prompt[:200], "task_id": task_id},
                f"Task launched with ID: {task_id}", source or "gemini_spark")

    async def _run():
        try:
            # Try official SDK first
            from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
            config = LocalAgentConfig(
                system_instructions="You are an autonomous pair programmer working in the user's workspace.",
                capabilities=CapabilitiesConfig(),
            )
            async with Agent(config) as agent:
                resp = await agent.chat(prompt)
                full_text = ""
                async for token in resp:
                    full_text += token
                tasks[task_id]["output"] = full_text
                tasks[task_id]["status"] = "completed"
        except ImportError:
            # SDK not installed — route through inject_message to an active Antigravity conversation
            # Find the most recently active conversation to delegate to
            target_conv = None
            if os.path.exists(BRAIN_DIR):
                convs = sorted(
                    [e for e in os.scandir(BRAIN_DIR)
                     if e.is_dir() and len(e.name) == 36 and e.name.count("-") == 4],
                    key=lambda e: e.stat().st_mtime, reverse=True
                )
                if convs:
                    target_conv = convs[0].name

            if target_conv:
                msg_dir = os.path.join(BRAIN_DIR, target_conv, ".system_generated", "messages")
                os.makedirs(msg_dir, exist_ok=True)
                msg_id = str(uuid.uuid4())
                payload = {
                    "id": msg_id,
                    "recipient": target_conv,
                    "sender": f"mcp-bridge/task-{task_id}",
                    "priority": "MESSAGE_PRIORITY_HIGH",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
                    "renderDetails": {"messageTitle": f"Spark Task [{task_id}]: AI work delegated to Antigravity"},
                    "content": (
                        f"**Task delegated from Gemini Spark (Task ID: {task_id})**\n\n"
                        f"Working directory: `{target_dir}`\n\n"
                        f"**Your task:**\n{prompt}\n\n"
                        f"Please complete this task using your full capabilities and Antigravity credits. "
                        f"When done, save a note using save_session_note with tag='task_result' and task_id='{task_id}'."
                    ),
                    "sourceMetadata": {}
                }
                with open(os.path.join(msg_dir, f"{msg_id}.json"), "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2)
                # Ensure it's unread
                read_path = os.path.join(msg_dir, "read.json")
                read_data = {}
                if os.path.exists(read_path):
                    try:
                        with open(read_path) as f:
                            read_data = json.load(f)
                    except Exception:
                        pass
                read_data.pop(msg_id, None)
                with open(read_path, "w") as f:
                    json.dump(read_data, f)

                tasks[task_id]["output"] = (
                    f"Task successfully routed to Antigravity conversation '{target_conv}'.\n"
                    f"Antigravity AI will execute using its own credits and models.\n"
                    f"Switch to Antigravity IDE to see it working in real time.\n"
                    f"Results will appear as a session note with tag='task_result'."
                )
                tasks[task_id]["status"] = "delegated_to_antigravity"
                tasks[task_id]["routed_to_conv"] = target_conv
            else:
                tasks[task_id]["output"] = "[Info] No active Antigravity conversation found to delegate to. Open Antigravity IDE first."
                tasks[task_id]["status"] = "failed"
        except Exception as e:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = f"{str(e)}\n{traceback.format_exc()}"

    asyncio.create_task(_run())
    return f"Task started successfully. Task ID: {task_id}\nRouting to Antigravity AI — uses Antigravity credits, not Spark credits."




@mcp.tool()
def get_agent_status(task_id: str) -> Dict[str, Any]:
    """
    Fetches the live status and output of a running or completed agent task.
    """
    if task_id not in tasks:
        return {"status": "not_found", "message": f"Task ID {task_id} does not exist."}
    return tasks[task_id]


@mcp.tool()
def terminate_task(task_id: str) -> str:
    """
    Terminates or cancels a running agent task by task ID.
    """
    if task_id in tasks:
        tasks[task_id]["status"] = "cancelled"
        _log_action("terminate_task", {"task_id": task_id}, "Task cancelled.", "system")
        return f"Task {task_id} has been marked as cancelled."
    return f"Task ID {task_id} not found."


# ─── History & Session Tools ──────────────────────────────────────────────────

@mcp.tool()
def get_bridge_history(limit: Optional[int] = 50, tool_filter: Optional[str] = None,
                       source_filter: Optional[str] = None) -> str:
    """
    Returns the full shared history of all tool calls made through this bridge —
    from Gemini Spark, Antigravity, or any other connected client.
    Use limit to control how many recent entries to return (default 50).
    Use tool_filter to show only a specific tool (e.g. 'write_file').
    Use source_filter to show only from 'gemini_spark' or 'antigravity'.
    """
    history = _load_history()

    if tool_filter:
        history = [h for h in history if h.get("tool") == tool_filter]
    if source_filter:
        history = [h for h in history if h.get("source") == source_filter]

    recent = history[-(limit or 50):]

    if not recent:
        return "[Info] No history found. Start using tools to build up a record."

    lines = [f"=== Bridge History ({len(recent)} entries) ===\n"]
    for entry in reversed(recent):
        lines.append(
            f"[{entry.get('timestamp', '?')}] [{entry.get('source', '?').upper()}] "
            f"Tool: {entry.get('tool', '?')} | ID: {entry.get('id', '?')}\n"
            f"  Input:  {json.dumps(entry.get('inputs', {}), ensure_ascii=False)[:150]}\n"
            f"  Result: {entry.get('result_preview', '')}\n"
            f"  {'─'*60}"
        )
    return "\n".join(lines)


@mcp.tool()
def save_session_note(note: str, tag: Optional[str] = None, source: Optional[str] = None) -> str:
    """
    Saves a note or memory to the shared bridge session log.
    Both Gemini Spark and Antigravity can read and write notes here.
    Use tag to categorize (e.g. 'decision', 'error', 'milestone', 'idea').
    """
    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source or "gemini_spark",
        "tool": "save_session_note",
        "inputs": {"note": note, "tag": tag or "general"},
        "result_preview": f"Note saved: {note[:200]}",
    }
    history = _load_history()
    history.append(entry)
    _save_history(history[-500:])
    return f"[Success] Note saved with ID {entry['id']} | Tag: {tag or 'general'}"


@mcp.tool()
def get_session_notes(tag_filter: Optional[str] = None) -> str:
    """
    Retrieves all saved session notes from the shared bridge log.
    Optionally filter by tag (e.g. 'decision', 'error', 'milestone').
    """
    history = _load_history()
    notes = [h for h in history if h.get("tool") == "save_session_note"]

    if tag_filter:
        notes = [n for n in notes if n.get("inputs", {}).get("tag") == tag_filter]

    if not notes:
        return "[Info] No session notes found."

    lines = [f"=== Session Notes ({len(notes)} entries) ===\n"]
    for n in reversed(notes):
        lines.append(
            f"[{n.get('timestamp')}] [{n.get('source', '?').upper()}] "
            f"Tag: {n.get('inputs', {}).get('tag', 'general')}\n"
            f"  {n.get('inputs', {}).get('note', '')}\n"
            f"  {'─'*60}"
        )
    return "\n".join(lines)


# ─── Antigravity Conversation Injection ──────────────────────────────────────

BRAIN_DIR = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")


def _extract_conversation_title(conv_path: str) -> str:
    """Extract conversation title from transcript CONVERSATION_HISTORY step or first USER_INPUT."""
    import re
    transcript = os.path.join(conv_path, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(transcript):
        return ""
    try:
        with open(transcript, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        # 1. Look for CONVERSATION_HISTORY step which contains "Conversation <id>: <Title>"
        for line in lines:
            try:
                data = json.loads(line)
                if data.get("type") == "CONVERSATION_HISTORY":
                    content = data.get("content", "")
                    match = re.search(r"##\s*Conversation\s+[\w-]+:\s*(.+)", content)
                    if match:
                        return match.group(1).strip()
            except Exception:
                continue

        # 2. Fallback: use first USER_INPUT content as title
        for line in lines:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "").strip()
                    if content:
                        return content[:60] + ("..." if len(content) > 60 else "")
            except Exception:
                continue
    except Exception:
        pass
    return ""


def _count_conversation_stats(conv_path: str) -> dict:
    """Count messages, artifacts, and tasks in a conversation."""
    transcript = os.path.join(conv_path, ".system_generated", "logs", "transcript.jsonl")
    stats = {"messages": 0, "user_messages": 0, "tasks": 0, "artifacts": 0}
    if not os.path.exists(transcript):
        return stats
    try:
        with open(transcript, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    t = data.get("type", "")
                    if t == "USER_INPUT":
                        stats["user_messages"] += 1
                    stats["messages"] += 1
                except Exception:
                    pass
        # Count tasks
        tasks_dir = os.path.join(conv_path, ".system_generated", "tasks")
        if os.path.exists(tasks_dir):
            stats["tasks"] = len([f for f in os.listdir(tasks_dir) if f.endswith(".log")])
        # Count artifacts (non-.system_generated files)
        for root, dirs, files in os.walk(conv_path):
            dirs[:] = [d for d in dirs if d != ".system_generated"]
            stats["artifacts"] += len([f for f in files if not f.endswith(".metadata.json")])
    except Exception:
        pass
    return stats


@mcp.tool()
def list_antigravity_conversations() -> str:
    """
    Lists ALL Antigravity projects/conversations with their real names (titles),
    conversation IDs, last active time, message count, artifact count, and task count.
    Exactly what you see in the Antigravity sidebar — use conversation_id with inject_message.
    """
    if not os.path.exists(BRAIN_DIR):
        return "[Error] Antigravity brain directory not found."

    results = []
    for entry in sorted(os.scandir(BRAIN_DIR), key=lambda e: e.stat().st_mtime, reverse=True):
        if not (entry.is_dir() and len(entry.name) == 36 and entry.name.count("-") == 4):
            continue

        title = _extract_conversation_title(entry.path) or "(Untitled)"
        stats = _count_conversation_stats(entry.path)
        mtime = datetime.fromtimestamp(entry.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

        results.append(
            f"📁 \"{title}\"\n"
            f"   ID       : {entry.name}\n"
            f"   Last Active: {mtime}\n"
            f"   Messages : {stats['user_messages']} user / {stats['messages']} total\n"
            f"   Tasks    : {stats['tasks']}  |  Artifacts: {stats['artifacts']}"
        )

    if not results:
        return "[Info] No conversations found."
    return "=== Antigravity Conversations & Projects ===\n\n" + "\n\n".join(results)


@mcp.tool()
def inject_message(
    conversation_id: str,
    message: str,
    sender: Optional[str] = None,
    priority: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """
    Injects a message directly into any Antigravity conversation's inbox.
    Antigravity picks it up immediately and wakes the agent — exactly like
    receiving a message from another agent or background task.

    Parameters:
        conversation_id : The target Antigravity conversation UUID
                          (get it from list_antigravity_conversations)
        message         : The text content to inject
        sender          : Optional sender label (default: 'mcp-bridge/gemini-spark')
        priority        : 'MESSAGE_PRIORITY_HIGH' or 'MESSAGE_PRIORITY_LOW' (default HIGH)
        title           : Optional title shown in the Antigravity notification
    """
    msg_dir = os.path.join(BRAIN_DIR, conversation_id, ".system_generated", "messages")
    if not os.path.exists(msg_dir):
        return f"[Error] Conversation '{conversation_id}' not found or has no message inbox."

    msg_id = str(uuid.uuid4())
    payload = {
        "id": msg_id,
        "recipient": conversation_id,
        "sender": sender or "mcp-bridge/gemini-spark",
        "priority": priority or "MESSAGE_PRIORITY_HIGH",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
        "renderDetails": {
            "messageTitle": title or "Message from MCP Bridge"
        },
        "content": message,
        "sourceMetadata": {}
    }

    msg_file = os.path.join(msg_dir, f"{msg_id}.json")
    try:
        with open(msg_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        # Mark as unread by ensuring it's NOT in read.json
        read_file_path = os.path.join(msg_dir, "read.json")
        read_data = {}
        if os.path.exists(read_file_path):
            try:
                with open(read_file_path, "r", encoding="utf-8") as f:
                    read_data = json.load(f)
            except Exception:
                read_data = {}
        # Remove from read if somehow already there
        read_data.pop(msg_id, None)
        with open(read_file_path, "w", encoding="utf-8") as f:
            json.dump(read_data, f)

        _log_action("inject_message", {
            "conversation_id": conversation_id,
            "message_preview": message[:200],
            "msg_id": msg_id
        }, f"Injected message {msg_id}", "mcp-bridge")

        return (
            f"[Success] Message injected into conversation '{conversation_id}'\n"
            f"Message ID: {msg_id}\n"
            f"Antigravity will pick it up on its next active check or immediately if idle."
        )
    except Exception as e:
        return f"[Error] Failed to inject message: {str(e)}"


if __name__ == "__main__":
    print("[INFO] Starting Antigravity MCP Server...")
    mcp.run(transport="sse")
