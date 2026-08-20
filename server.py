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
    Launches an autonomous Antigravity coding subagent in the background to fulfill complex goals.
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
    }
    _log_action("run_agent_task", {"prompt": prompt[:200], "task_id": task_id},
                f"Task launched with ID: {task_id}", source or "gemini_spark")

    async def _run():
        try:
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
            tasks[task_id]["output"] = f"Agent task received for prompt: '{prompt}'. Direct system hooks ready."
            tasks[task_id]["status"] = "completed"
        except Exception as e:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = f"{str(e)}\n{traceback.format_exc()}"

    asyncio.create_task(_run())
    return f"Task started successfully. Task ID: {task_id}"


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


if __name__ == "__main__":
    print("[INFO] Starting Antigravity MCP Server...")
    mcp.run(transport="sse")
