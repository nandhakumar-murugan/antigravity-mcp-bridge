<div align="center">

<!-- HEADER LOGOS -->
<img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" width="60" alt="Gemini"/>
&nbsp;&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/1280px-Google_Cloud_logo.svg.png" width="140" alt="Google Cloud"/>
&nbsp;&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/115px-Python-logo-notext.svg.png" width="50" alt="Python"/>

# ⚡ Antigravity MCP Bridge

### *The Open-Source Bridge Connecting Google Cloud AI to Your Local Machine via the Model Context Protocol*

<!-- BADGES -->
[![Model Context Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-MCP%202.0-4285F4?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHoiLz48L3N2Zz4=&logoColor=white)](https://modelcontextprotocol.io)
[![Gemini Spark](https://img.shields.io/badge/Google%20Gemini-Spark%20Connected-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Integrated-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ngrok](https://img.shields.io/badge/Tunnel-ngrok-1F1E37?style=for-the-badge&logo=ngrok&logoColor=white)](https://ngrok.com)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/nandhakumar-murugan/antigravity-mcp-bridge?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/stargazers)

---

> **Verified Proof of Concept**: A single Gemini Spark prompt — *"Create a calculator with unit tests"* — produced, ran, and committed working Python code to GitHub in under 3 seconds. Zero human copy-pasting.

[Architecture](#-system-architecture) • [Tools API](#-complete-tools-reference) • [Quickstart](#-quickstart) • [Google Ecosystem](#-google-ecosystem-integration) • [Developer Docs](#-developer-integration-guide) • [Resources & Links](#-official-documentation--external-resources) • [Benefits](#-who-benefits)

</div>

---

## 🧩 What Is This Project?

**Antigravity MCP Bridge** breaks the barrier between Cloud AI and your local machine. It runs a local **Model Context Protocol (MCP)** server that exposes your entire operating system — terminal, files, compilers, and Git — to any MCP-compatible AI orchestrator over a secure HTTPS tunnel.

Connect it to **Google Gemini Spark** and you get a fully autonomous AI Software Engineer that can plan, code, test, fix, and ship software directly on your disk.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                🌐  GOOGLE CLOUD ECOSYSTEM                          │
│                                                                    │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  Gemini Spark   │  │  Google Workspace │  │  Vertex AI /    │  │
│  │  (Orchestrator) │  │  Docs/Drive/Gmail │  │  Cloud Run      │  │
│  └────────┬────────┘  └──────────────────┘  └─────────────────┘  │
└───────────┼────────────────────────────────────────────────────────┘
            │  JSON-RPC 2.0 (Streamable HTTP / SSE)
            │  HTTPS via ngrok / Cloudflare Tunnel
┌───────────▼────────────────────────────────────────────────────────┐
│          ⚡  ANTIGRAVITY MCP BRIDGE  (Your Machine)                │
│                                                                    │
│   /mcp  (Streamable HTTP)    /sse  (Server-Sent Events)           │
│   CORS · Authentication · 7 Registered MCP Tools                  │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  File System │  │   Terminal   │  │  Antigravity Subagents   │ │
│  │  Read/Write  │  │  Shell/CMD   │  │  (Autonomous Tasks)      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │   Python     │  │  Node.js/npm │  │   Git / Docker / CI      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

### Transport Protocol

| Endpoint | Protocol | Best For |
|:---|:---|:---|
| `/mcp` | Streamable HTTP (MCP 2.0) | Google Gemini Spark, Vertex AI, all modern MCP clients |
| `/sse` | Server-Sent Events (SSE) | Legacy MCP clients, custom integrations |
| `/messages` | HTTP POST | Posting messages in SSE sessions |

---

## 🧰 Complete Tools Reference

### 🔧 Tool 1: `run_system_command`
Execute any shell, PowerShell or Bash command. Captures exit code, stdout, stderr.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `command` | string | ✅ | Full shell command to execute |
| `working_dir` | string | ❌ | Working directory path (defaults to CWD) |

```json
// Example: Run Python unit tests
{
  "name": "run_system_command",
  "arguments": {
    "command": "python -m pytest tests/ -v",
    "working_dir": "C:/Users/dev/myproject"
  }
}
```
**Use for:** Running Python/Node/Java/Rust, pip install, npm install, git operations, test runners, Docker, CI pipelines.

---

### 📝 Tool 2: `write_file`
Create or overwrite any file on disk with AI-generated content. Auto-creates directories.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `file_path` | string | ✅ | Absolute or relative file path |
| `content` | string | ✅ | Full content to write |

```json
// Example: Write a FastAPI route
{
  "name": "write_file",
  "arguments": {
    "file_path": "src/api/routes.py",
    "content": "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/health')\ndef health(): return {'status': 'ok'}"
  }
}
```
**Use for:** Writing source code, configs, Dockerfiles, GitHub Actions YAML, Markdown docs, .env files.

---

### 📖 Tool 3: `read_file`
Read and return the full content of any local file.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `file_path` | string | ✅ | Path to the file |

```json
{
  "name": "read_file",
  "arguments": { "file_path": "src/main.py" }
}
```
**Use for:** Inspecting code before refactoring, reading logs, auditing configs, reading datasets.

---

### 📂 Tool 4: `list_directory`
Enumerate files and directories with type and size.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `directory_path` | string | ❌ | Directory to list (defaults to CWD) |

```json
{
  "name": "list_directory",
  "arguments": { "directory_path": "C:/Users/dev/myproject" }
}
```
**Use for:** Discovering project structure, verifying files were created, auditing repos.

---

### 🤖 Tool 5: `run_agent_task`
Spawn an autonomous long-running **Antigravity AI subagent** for complex multi-step goals. Returns instantly with a `task_id`.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `prompt` | string | ✅ | High-level natural language objective |
| `workspace_dir` | string | ❌ | Directory for the agent to operate in |

```json
{
  "name": "run_agent_task",
  "arguments": {
    "prompt": "Refactor all Python files to use async/await. Run tests after each file.",
    "workspace_dir": "C:/Users/dev/myproject"
  }
}
```
**Use for:** Large-scale refactoring, full feature development, autonomous TDD, security audits.

---

### 📊 Tool 6: `get_agent_status`
Poll the live progress, output, and errors of a background subagent task.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `task_id` | string | ✅ | Task ID from `run_agent_task` |

```json
{
  "name": "get_agent_status",
  "arguments": { "task_id": "a1b2c3d4" }
}
// Returns: { "status": "completed", "output": "...", "error": null }
```

---

### 🛑 Tool 7: `terminate_task`
Safely cancel any running background subagent task.

| Param | Type | Required | Description |
|:---|:---|:---:|:---|
| `task_id` | string | ✅ | Task ID to cancel |

---

## 🔗 Google Ecosystem Integration

<table>
<tr>
<td width="50%">

### <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" width="20"/> Gemini Spark
**Connect your bridge to Gemini via Custom Connected Apps.**

- 📖 [Gemini Home](https://gemini.google.com)
- 📖 [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- 📖 [Gemini for Google Workspace](https://workspace.google.com/intl/en/products/gemini/)

</td>
<td width="50%">

### <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/100px-Google_Cloud_logo.svg.png" width="80"/> Google Cloud
**Deploy the bridge to Cloud or integrate with Cloud AI.**

- 📖 [Google Cloud Console](https://console.cloud.google.com)
- 📖 [Cloud Run Docs](https://cloud.google.com/run/docs)
- 📖 [Cloud Build Docs](https://cloud.google.com/build/docs)

</td>
</tr>
<tr>
<td>

### <img src="https://www.gstatic.com/images/branding/product/1x/vertex_ai_64dp.png" width="22"/> Vertex AI
**Enterprise-grade AI orchestration with local execution.**

- 📖 [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- 📖 [Vertex AI Workbench](https://cloud.google.com/vertex-ai/docs/workbench/introduction)
- 📖 [Generative AI on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/overview)

</td>
<td>

### <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg" width="22"/> Google Workspace
**Use Docs, Drive, Gmail as AI context sources.**

- 📖 [Google Workspace APIs](https://developers.google.com/workspace)
- 📖 [Google Drive API](https://developers.google.com/drive)
- 📖 [Google Docs API](https://developers.google.com/docs/api)

</td>
</tr>
</table>

---

## 📚 Official Documentation & External Resources

### 🔵 Model Context Protocol (MCP)

| Resource | Link |
|:---|:---|
| 🏠 MCP Official Website | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| 📖 MCP Introduction | [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction) |
| 📖 MCP Quickstart Guide | [modelcontextprotocol.io/quickstart](https://modelcontextprotocol.io/quickstart) |
| 📖 MCP Specification | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io) |
| 🐍 Python MCP SDK (Official) | [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) |
| 📦 MCP on PyPI | [pypi.org/project/mcp](https://pypi.org/project/mcp/) |
| 🐙 MCP GitHub Organization | [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol) |
| 📖 MCP Transports Reference | [modelcontextprotocol.io/docs/concepts/transports](https://modelcontextprotocol.io/docs/concepts/transports) |
| 📖 MCP Tools Reference | [modelcontextprotocol.io/docs/concepts/tools](https://modelcontextprotocol.io/docs/concepts/tools) |

---

### 🟣 Google Antigravity (AGY)

| Resource | Link |
|:---|:---|
| 🏠 Antigravity Home | [antigravity.google](https://antigravity.google) |
| 📖 Antigravity Docs | [antigravity.google/docs](https://antigravity.google/docs) |
| 📖 MCP Integration Guide | [antigravity.google/docs/mcp](https://antigravity.google/docs/mcp) |
| 📖 Skills System | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| 📖 Python SDK | [antigravity.google/docs/sdk](https://antigravity.google/docs/sdk) |
| 📖 Hooks & Plugins | [antigravity.google/docs/hooks](https://antigravity.google/docs/hooks) |
| 📖 Agent Permissions | [antigravity.google/docs/permissions](https://antigravity.google/docs/permissions) |
| 📖 Changelog | [antigravity.google/changelog](https://antigravity.google/changelog) |

---

### 🔵 Google Gemini & AI APIs

| Resource | Link |
|:---|:---|
| 🏠 Google Gemini App | [gemini.google.com](https://gemini.google.com) |
| 📖 Gemini API Documentation | [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs) |
| 📖 Gemini API Quickstart | [ai.google.dev/gemini-api/docs/quickstart](https://ai.google.dev/gemini-api/docs/quickstart) |
| 📖 Gemini for Google Workspace | [workspace.google.com/intl/en/products/gemini](https://workspace.google.com/intl/en/products/gemini/) |
| 📖 Google AI Studio | [aistudio.google.com](https://aistudio.google.com) |
| 📖 Connected Apps (MCP) Help | [support.google.com/gemini?p=lm_custom_mcp_trust](https://support.google.com/gemini?p=lm_custom_mcp_trust) |
| 🐙 Google Generative AI GitHub | [github.com/google-gemini](https://github.com/google-gemini) |

---

### ☁️ Google Cloud Platform

| Resource | Link |
|:---|:---|
| 🏠 Google Cloud Console | [console.cloud.google.com](https://console.cloud.google.com) |
| 📖 Vertex AI Documentation | [cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs) |
| 📖 Cloud Run Documentation | [cloud.google.com/run/docs](https://cloud.google.com/run/docs) |
| 📖 Cloud Build Documentation | [cloud.google.com/build/docs](https://cloud.google.com/build/docs) |
| 📖 Google Cloud APIs Explorer | [cloud.google.com/apis](https://cloud.google.com/apis) |
| 📖 AI & Machine Learning Products | [cloud.google.com/products/ai](https://cloud.google.com/products/ai) |

---

### 🐍 Python & Core Libraries

| Resource | Link |
|:---|:---|
| 🏠 Python Official Website | [python.org](https://python.org) |
| 📖 Python Docs | [docs.python.org/3](https://docs.python.org/3/) |
| 📦 PyPI Package Index | [pypi.org](https://pypi.org) |
| 📖 pip Documentation | [pip.pypa.io/en/stable](https://pip.pypa.io/en/stable/) |
| 📖 asyncio Documentation | [docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html) |
| 📖 subprocess Documentation | [docs.python.org/3/library/subprocess.html](https://docs.python.org/3/library/subprocess.html) |

---

### 🌐 Web & ASGI Framework

| Resource | Link |
|:---|:---|
| 🏠 Uvicorn (ASGI Server) | [uvicorn.org](https://www.uvicorn.org/) |
| 📖 Uvicorn Docs | [uvicorn.org/settings](https://www.uvicorn.org/settings/) |
| 🏠 Starlette Framework | [starlette.io](https://www.starlette.io/) |
| 📖 Starlette Docs | [starlette.io/applications](https://www.starlette.io/applications/) |
| 📖 Starlette Routing | [starlette.io/routing](https://www.starlette.io/routing/) |
| 📖 CORS Middleware | [starlette.io/middleware/#corsmiddleware](https://www.starlette.io/middleware/#corsmiddleware) |
| 🏠 FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| 📖 FastAPI Docs | [fastapi.tiangolo.com/tutorial](https://fastapi.tiangolo.com/tutorial/) |

---

### 🔒 Tunneling & Secure Exposure

| Resource | Link |
|:---|:---|
| 🏠 ngrok Official Website | [ngrok.com](https://ngrok.com) |
| 📖 ngrok Documentation | [ngrok.com/docs](https://ngrok.com/docs) |
| 📖 ngrok HTTP Tunnels | [ngrok.com/docs/http](https://ngrok.com/docs/http/) |
| 📦 pyngrok (Python SDK) | [pypi.org/project/pyngrok](https://pypi.org/project/pyngrok/) |
| 📖 pyngrok Docs | [pyngrok.readthedocs.io](https://pyngrok.readthedocs.io/en/latest/) |
| 🏠 Cloudflare Tunnel | [cloudflare.com/products/tunnel](https://www.cloudflare.com/products/tunnel/) |
| 📖 Cloudflare Tunnel Docs | [developers.cloudflare.com/cloudflare-one/connections/connect-networks](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) |

---

### 📡 JSON-RPC & SSE Specifications

| Resource | Link |
|:---|:---|
| 📖 JSON-RPC 2.0 Specification | [jsonrpc.org/specification](https://www.jsonrpc.org/specification) |
| 📖 Server-Sent Events (SSE) — MDN | [developer.mozilla.org/en-US/docs/Web/API/Server-sent_events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) |
| 📖 HTTP Status Codes — MDN | [developer.mozilla.org/en-US/docs/Web/HTTP/Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) |

---

### 🔧 Development Tools

| Resource | Link |
|:---|:---|
| 🏠 Git | [git-scm.com](https://git-scm.com) |
| 📖 Git Documentation | [git-scm.com/doc](https://git-scm.com/doc) |
| 🏠 GitHub | [github.com](https://github.com) |
| 📖 GitHub CLI (gh) | [cli.github.com](https://cli.github.com) |
| 🏠 Python IDLE | [docs.python.org/3/library/idle.html](https://docs.python.org/3/library/idle.html) |
| 📖 pytest Testing Framework | [docs.pytest.org](https://docs.pytest.org) |
| 📖 unittest (Built-in) | [docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html) |

---

## 🚀 Quickstart

### Prerequisites
[![Python](https://img.shields.io/badge/Python%203.10%2B-Download-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![ngrok](https://img.shields.io/badge/ngrok-Free%20Signup-1F1E37?style=flat-square&logo=ngrok&logoColor=white)](https://dashboard.ngrok.com/signup)
[![Git](https://img.shields.io/badge/Git-Download-F05032?style=flat-square&logo=git&logoColor=white)](https://git-scm.com/downloads)

### Step 1 — Clone & Install
```bash
git clone https://github.com/nandhakumar-murugan/antigravity-mcp-bridge.git
cd antigravity-mcp-bridge
pip install -r requirements.txt
```

### Step 2 — Add Your ngrok Token
Get your token at [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

Edit `run_with_tunnel.py`:
```python
AUTHTOKEN = "your_ngrok_authtoken_here"
```

### Step 3 — Launch
```bash
# Windows (Double-click or run):
start_server.bat

# macOS / Linux:
python run_with_tunnel.py
```

Output:
```
[INFO] NGROK MCP TUNNEL IS LIVE!
[LINK] PASTE THIS IN GEMINI SPARK: https://xxxx.ngrok-free.dev/mcp
```

### Step 4 — Connect to Gemini Spark
1. Open [gemini.google.com](https://gemini.google.com)
2. Go to **Settings → Custom Connected Apps**
3. Paste: `https://xxxx.ngrok-free.dev/mcp`
4. Accept permissions → Click **Save**
5. Type `@Antigravity System Bridge` in any chat to activate!

---

## 💻 Developer Integration Guide

### Python (Official MCP SDK)
```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    url = "https://xxxx.ngrok-free.dev/mcp"
    async with streamable_http_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print([t.name for t in tools.tools])

            # Run a command
            result = await session.call_tool("run_system_command", {
                "command": "python --version"
            })
            print(result.content[0].text)

asyncio.run(main())
```

### cURL (Any Language)
```bash
curl -X POST https://xxxx.ngrok-free.dev/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"my-app","version":"1.0"}}}'
```

### Claude Desktop Config
```json
{
  "mcpServers": {
    "antigravity-bridge": {
      "command": "python",
      "args": ["run_with_tunnel.py"],
      "env": { "NGROK_AUTHTOKEN": "your_token" }
    }
  }
}
```

---

## 👥 Who Benefits

### 🎓 Students
- See real code written and run on your disk — not in fake sandboxes
- AI handles `pip install`, virtual environments, and PATH setup for you
- Learn debugging by watching the AI fix real terminal errors live

### 💻 Engineers
- Full autonomous TDD: AI writes code → runs tests → fixes failures → repeats
- Delegate entire features: *"Build a REST API with auth"* → done in minutes
- No more copy-pasting between chat and editor

### 🔬 Researchers
- Run local Python pipelines without uploading sensitive data to the cloud
- Automate experiment scripts, benchmarks, and data analysis conversationally
- Use local GPU compute via terminal commands

---

## 📁 Project Structure

```
antigravity-mcp-bridge/
├── server.py               # Core MCP server with all 7 tool definitions
├── run_with_tunnel.py      # One-click launcher (server + ngrok tunnel)
├── start_server.bat        # Windows double-click starter
├── test_client.py          # MCP connection verification script
├── calculator.py           # Example: AI-generated code via Gemini Spark
├── test_calculator.py      # Example: AI-generated tests (all 6 passed)
├── requirements.txt        # Python dependencies
├── .gitignore
├── LICENSE                 # MIT
└── README.md
```

---

## 📦 requirements.txt

```
mcp>=2.0.0
uvicorn
fastapi
pyngrok
python-dotenv
```

---

## 🛡️ Security

- All traffic is **TLS-encrypted** via ngrok HTTPS
- ngrok **Authtoken** prevents unauthorized access
- 180-second **command timeout** on all terminal executions
- `terminate_task` **immediately halts** any running subagent
- All operations are **fully visible** in your local terminal

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

### Built with the Google Ecosystem. Powered by Open Standards.

[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://gemini.google.com)
[![Cloud](https://img.shields.io/badge/Google-Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com)
[![MCP](https://img.shields.io/badge/Model%20Context-Protocol-blue?style=flat-square)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![ngrok](https://img.shields.io/badge/ngrok-1F1E37?style=flat-square&logo=ngrok&logoColor=white)](https://ngrok.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge)

**⭐ Star this repo** if it helped you! | **🍴 Fork** to customize for your team

[🐛 Report Issues](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/issues) · [💬 Discussions](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/discussions) · [🤝 Contribute](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/pulls)

</div>
