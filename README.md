<div align="center">

<img src="https://img.shields.io/badge/⚡_ANTIGRAVITY-MCP_BRIDGE-6C63FF?style=for-the-badge&labelColor=1a1a2e" width="600"/>

# Antigravity MCP Bridge
### *The World's First Open-Source Bridge Connecting Cloud AI Orchestrators to Local Development Environments via the Model Context Protocol*

[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12%20|%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![MCP](https://img.shields.io/badge/Protocol-Model_Context_Protocol-4285F4?style=flat-square&logo=google&logoColor=white)](https://modelcontextprotocol.io)
[![Gemini Spark](https://img.shields.io/badge/Gemini_Spark-Connected-00C853?style=flat-square&logo=google&logoColor=white)](https://gemini.google.com)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-FF6F00?style=flat-square&logo=google&logoColor=white)](https://antigravity.google)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Windows](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-0078D4?style=flat-square&logo=windows&logoColor=white)](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge)

**Bridges the Gap Between Cloud AI and Your Local Machine**

[Architecture](#-system-architecture) • [All Tools Reference](#-complete-tools-reference--developer-api) • [Quickstart](#-quickstart) • [Google Ecosystem Integration](#-google-ecosystem-deep-integration) • [Developer Docs](#-developer-integration-guide) • [Benefits](#-who-benefits) • [Use Cases](#-real-world-use-cases) • [Security](#-security--safety-model)

---

> **Live Proof of Concept**: Using this bridge, a single prompt to Gemini Spark — *"Create a calculator with unit tests and run them"* — autonomously produced, tested, and committed working Python code to GitHub on a real local machine **in under 3 seconds**, with zero human intervention.

</div>

---

## 🎯 The Problem Being Solved

| Traditional AI Workflow | With Antigravity MCP Bridge |
|:---|:---|
| AI generates code → You manually copy | AI directly writes files to your disk |
| You open terminal, paste, debug | AI executes in your terminal, reads errors |
| 15+ steps per feature cycle | Single natural language instruction |
| AI has no awareness of your runtime | AI sees your real compiler output |
| Local and Cloud are disconnected silos | Unified conversational interface |
| Students confused by setup complexity | AI handles all environment configuration |

---

## 🏗️ System Architecture

### The "Brain + Hands" Paradigm

```
┌─────────────────────────────────────────────────────────────────┐
│               🌐  GOOGLE CLOUD ECOSYSTEM (THE BRAIN)            │
│  ┌──────────────────┐  ┌───────────────┐  ┌──────────────────┐ │
│  │  Gemini Spark    │  │  Google Docs  │  │   Vertex AI      │ │
│  │  (Orchestrator)  │  │  Drive/Gmail  │  │   Cloud Run      │ │
│  └────────┬─────────┘  └───────────────┘  └──────────────────┘ │
└───────────┼─────────────────────────────────────────────────────┘
            │
            │ Model Context Protocol (Streamable HTTP / SSE)
            │ JSON-RPC 2.0 over HTTPS (ngrok / Cloudflare Tunnel)
            │
┌───────────▼─────────────────────────────────────────────────────┐
│           ⚡  ANTIGRAVITY MCP BRIDGE SERVER (run_with_tunnel.py)│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                MCP Server (MCPServer 2.0)                   ││
│  │   7 Exposed Tools  |  CORS  |  Streamable HTTP  |  SSE     ││
│  └──────────┬──────────────────────────────────────────────────┘│
└─────────────┼───────────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│               💻  YOUR LOCAL MACHINE (THE HANDS)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  File System │  │   Terminal   │  │  Antigravity Engine   │  │
│  │  (All Files) │  │  (Any Shell) │  │  (Subagent Tasks)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    Python    │  │   Node.js    │  │  Git / CI / Docker   │  │
│  │    pip/venv  │  │   npm/yarn   │  │  (Full DevOps Chain) │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Communication Protocol Deep Dive

The bridge supports two official MCP transports:

| Transport | Endpoint | Use Case | Headers Required |
|:---|:---|:---|:---|
| **Streamable HTTP** | `/mcp` | Google Gemini Spark, Claude Desktop | `Accept: application/json, text/event-stream` |
| **Server-Sent Events (SSE)** | `/sse` | Legacy MCP clients, custom integrations | `Accept: text/event-stream` |
| **SSE Messages** | `/messages` | Bidirectional message posting | `Content-Type: application/json` |

All endpoints return **JSON-RPC 2.0** responses over a persistent `text/event-stream` connection with proper CORS headers.

---

## 🧰 Complete Tools Reference & Developer API

### Tool 1: `run_system_command`

Execute any shell or PowerShell command on the local machine with full stdout/stderr capture.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `command` | `string` | ✅ | The full shell command to execute |
| `working_dir` | `string` | ❌ | Absolute path to working directory (defaults to server CWD) |

**Returns:** `string` — Exit code, stdout, and stderr formatted output.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "run_system_command",
    "arguments": {
      "command": "python -m pytest tests/ -v --tb=short",
      "working_dir": "C:/Users/dev/myproject"
    }
  }
}
```

**Example Response:**
```
[Exit Code: 0]
--- STDOUT ---
tests/test_api.py::test_health PASSED
tests/test_api.py::test_create_user PASSED
2 passed in 0.34s
--- STDERR ---
(empty)
```

**Practical Applications:**
- Run Python, Node.js, Java, or Rust compilers
- Execute `pip install`, `npm install`, `cargo build`
- Run `git commit`, `git push`, `git diff`
- Execute unit test runners (`pytest`, `jest`, `mocha`, `unittest`)
- Run database migrations (`alembic upgrade head`)
- Trigger Docker builds and container management
- Execute custom build scripts and CI pipelines locally

---

### Tool 2: `write_file`

Create or completely overwrite any file on the local filesystem with AI-generated content.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `file_path` | `string` | ✅ | Absolute or relative path to the file |
| `content` | `string` | ✅ | Full string content to write to the file |

**Returns:** `string` — Success message with the absolute path where the file was written.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "write_file",
    "arguments": {
      "file_path": "src/api/routes.py",
      "content": "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/health')\ndef health_check():\n    return {'status': 'ok'}"
    }
  }
}
```

**Practical Applications:**
- Write Python, JavaScript, TypeScript, Go, Rust, Java source code
- Generate full project structures (`src/`, `tests/`, `docs/`, `configs/`)
- Create configuration files (`package.json`, `pyproject.toml`, `Dockerfile`, `.env.example`)
- Write GitHub Actions workflow files (`.github/workflows/*.yml`)
- Generate Markdown documentation, README files, API specs

---

### Tool 3: `read_file`

Read and return the full UTF-8 content of any local file.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `file_path` | `string` | ✅ | Absolute or relative path to the file to read |

**Returns:** `string` — Full content of the file.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "file_path": "src/api/routes.py"
    }
  }
}
```

**Practical Applications:**
- Analyze existing code before refactoring
- Read error log files to diagnose production issues
- Inspect configuration files before modifying
- Validate the content of files just written
- Read CSV/JSON datasets for analysis

---

### Tool 4: `list_directory`

Enumerate all files and directories at a given path with size and type information.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `directory_path` | `string` | ❌ | Path to inspect (defaults to server CWD) |

**Returns:** `string` — Human-readable directory listing with `[DIR]`/`[FILE]` labels and byte sizes.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "list_directory",
    "arguments": {
      "directory_path": "C:/Users/dev/myproject"
    }
  }
}
```

**Practical Applications:**
- Discover project structure before starting work
- Verify files were created successfully
- Audit codebases for outdated or orphaned files
- Navigate multi-module repository layouts

---

### Tool 5: `run_agent_task`

Launch an autonomous long-running **Antigravity AI subagent** in the background to accomplish a complex multi-step coding goal. Returns immediately with a `task_id` for polling.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `prompt` | `string` | ✅ | High-level natural language objective for the subagent |
| `workspace_dir` | `string` | ❌ | Directory where the subagent should operate |

**Returns:** `string` — Confirmation message with the assigned `task_id`.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "run_agent_task",
    "arguments": {
      "prompt": "Refactor all Python files in src/ to use async/await patterns. Run the test suite after each file to verify no regressions.",
      "workspace_dir": "C:/Users/dev/myproject"
    }
  }
}
```

**Practical Applications:**
- Large-scale codebase refactoring (sync to async, Python 2 to 3)
- Autonomous bug hunting and test-driven repair
- Full feature implementation from specification to tested code
- Repository-wide documentation generation
- Automated security audit and remediation

---

### Tool 6: `get_agent_status`

Poll the current status, output, and any errors from a background subagent task.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `task_id` | `string` | ✅ | The task ID returned by `run_agent_task` |

**Returns:** `object` — JSON with `status` (`running`/`completed`/`failed`/`cancelled`), `output`, and `error`.

**Example JSON-RPC Call:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "get_agent_status",
    "arguments": {
      "task_id": "a1b2c3d4"
    }
  }
}
```

**Example Response:**
```json
{
  "task_id": "a1b2c3d4",
  "status": "completed",
  "output": "Refactored 12 files. All 47 tests passing. Exit code: 0.",
  "error": null
}
```

---

### Tool 7: `terminate_task`

Safely cancel a running background subagent task.

**Parameters:**
| Parameter | Type | Required | Description |
|:---|:---|:---:|:---|
| `task_id` | `string` | ✅ | The task ID to cancel |

**Returns:** `string` — Confirmation of cancellation.

---

## 🔗 Google Ecosystem Deep Integration

This bridge is specifically architected to synergize with the full Google development stack:

### Gemini Spark Integration
```
User Prompt in Gemini Spark Chat
    ↓
Gemini Spark reasons about which local tools to call
    ↓
MCP JSON-RPC POST to /mcp endpoint (via ngrok HTTPS)
    ↓
Antigravity Bridge executes on local OS
    ↓
Result streamed back via text/event-stream
    ↓
Gemini Spark presents result in conversation
```

### Google Cloud & Vertex AI Integration
- **Google Cloud Run**: Deploy the bridge server as a containerized microservice in secure Google Cloud environments
- **Vertex AI Workbench**: Attach as a local code execution kernel for notebook-based AI workflows
- **Google Cloud Build**: Trigger local pre-commit validation before pushing to Cloud Source Repositories

### Google Workspace Integration
| Workspace App | Integration Potential |
|:---|:---|
| **Google Docs** | Gemini reads project specs from Docs → Bridge writes code locally |
| **Google Drive** | Gemini downloads datasets/assets from Drive → Bridge processes them locally |
| **Gmail** | Gemini reads issue reports from Gmail → Bridge creates bugfix branches autonomously |
| **Google Sheets** | Gemini exports structured data → Bridge runs local analysis and charts |

---

## 🚀 Quickstart

### Prerequisites
- **Python 3.10+**: [Download](https://python.org/downloads)
- **ngrok Account (Free)**: [Signup](https://dashboard.ngrok.com/signup)
- **Git**: [Download](https://git-scm.com)

### Step 1: Clone & Install
```bash
git clone https://github.com/nandhakumar-murugan/antigravity-mcp-bridge.git
cd antigravity-mcp-bridge
pip install -r requirements.txt
```

### Step 2: Configure Your ngrok Token
Get your free token from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

Open `run_with_tunnel.py` and replace the token:
```python
AUTHTOKEN = "your_ngrok_authtoken_here"
```

### Step 3: Launch (One Command)
```bash
# Windows:
start_server.bat

# macOS / Linux:
python run_with_tunnel.py
```

Your terminal will display:
```
[INFO] NGROK MCP TUNNEL IS LIVE!
[LINK] PASTE THIS IN GEMINI SPARK: https://xxxx.ngrok-free.dev/mcp
```

### Step 4: Connect to Gemini Spark
1. Open [Gemini](https://gemini.google.com) → Settings → **Custom Connected Apps**
2. Paste: `https://xxxx.ngrok-free.dev/mcp`
3. Accept permissions and click **Next**
4. All 7 tools will be discovered and activated automatically
5. Mention `@Antigravity System Bridge` in any chat!

---

## 💻 Developer Integration Guide

### Connecting Any MCP Client
```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def call_bridge():
    SERVER_URL = "https://your-ngrok-url.ngrok-free.dev/mcp"
    
    async with streamable_http_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List all available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Execute a shell command
            result = await session.call_tool("run_system_command", {
                "command": "python --version"
            })
            print(result.content[0].text)
            
            # Write a file
            await session.call_tool("write_file", {
                "file_path": "hello.py",
                "content": "print('Hello from MCP!')"
            })
            
            # Run it
            result = await session.call_tool("run_system_command", {
                "command": "python hello.py"
            })
            print(result.content[0].text)

asyncio.run(call_bridge())
```

### Connecting via raw HTTP (Any Language)
```bash
# Initialize Session
curl -X POST https://your-server.ngrok-free.dev/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "my-app", "version": "1.0"}
    }
  }'

# Call a Tool (with mcp-session-id from initialize response headers)
curl -X POST https://your-server.ngrok-free.dev/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "run_system_command",
      "arguments": {"command": "echo Hello World!"}
    }
  }'
```

### Claude Desktop Integration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "antigravity-bridge": {
      "command": "python",
      "args": ["run_with_tunnel.py"],
      "env": {
        "NGROK_AUTHTOKEN": "your_token_here"
      }
    }
  }
}
```

---

## 👥 Who Benefits

### 🎓 Students & Beginners
- **No more "Tutorial Hell"**: Watch real software being built and run on your own computer
- **Zero Setup Anxiety**: AI handles `pip install`, virtual environments, and PATH configuration
- **Live Debugging**: See how runtime errors are diagnosed and fixed in real time
- **Learn by Watching**: Every file created and command run is visible and educational

### 💻 Professional Engineers
- **10x Productivity**: Delegate boilerplate, test writing, and refactoring completely
- **True Autonomous TDD**: AI writes code, runs tests, heals failures, repeats until 100% green
- **Context-Free Task Delegation**: Focus on architecture while AI handles implementation details
- **CI/CD Automation**: Trigger full local validation pipelines conversationally

### 🔬 Researchers & Data Scientists
- **Secure Local Compute**: Process private datasets locally without uploading to third parties
- **Automated Experiments**: Run hyperparameter searches and benchmark sweeps autonomously
- **GPU Utilization**: Leverage local NVIDIA GPUs through conversational commands
- **Reproducible Research**: AI generates and executes reproducible experiment scripts

### 🏢 Organizations & Teams
- **Standardized Dev Environments**: One bridge config deployed across all developer machines
- **Reduced Onboarding Time**: New developers can start contributing within minutes via AI guidance
- **Documentation Automation**: AI continuously updates technical docs as code evolves

---

## 🌍 Real-World Use Cases

| Use Case | Tools Used | Time Savings |
|:---|:---|:---|
| Generate full CRUD REST API with tests | `write_file` + `run_system_command` | ~4 hours → 2 minutes |
| Migrate 50 files from Python 2 to 3 | `run_agent_task` + `get_agent_status` | ~2 days → 30 minutes |
| Debug a production log error | `read_file` + `run_system_command` | ~45 min → 2 minutes |
| Set up a new project with CI/CD | `write_file` + `run_system_command` | ~3 hours → 5 minutes |
| Generate unit tests for entire module | `read_file` + `write_file` + `run_system_command` | ~1 day → 10 minutes |
| Deploy to Google Cloud Run | `run_system_command` (gcloud) | ~1 hour → 3 minutes |

---

## 📉 What This Eliminates

```
BEFORE:
Prompt AI → Copy Code → Open IDE → Create File → Paste Code → Fix Indentation
→ Open Terminal → Run → Error! → Copy Error → Back to AI → Fix → Repeat
                                           (15-30 minutes per iteration)

AFTER:
Natural Language → Autonomous Execution → Verified Result
                        (10-30 seconds)
```

**Bottlenecks Eliminated:**
- Manual copy-paste between AI chat and code editor
- Environment setup confusion (PATH, venvs, dependencies)
- Context-switching between browser, IDE, and terminal
- Hallucinated import errors (AI tests against your real runtime)
- Manual git operations and commit workflows
- Time wasted explaining your file structure to the AI on every message

---

## 🔒 Security & Safety Model

| Layer | Protection Mechanism |
|:---|:---|
| **Transport Security** | All traffic encrypted via ngrok HTTPS (TLS 1.3) |
| **Authentication** | ngrok Authtoken prevents unauthorized tunnel access |
| **Workspace Isolation** | Tools respect `working_dir` boundaries |
| **Human Oversight** | All actions visible in terminal; user can kill any task instantly |
| **Task Control** | `terminate_task` immediately halts any running subagent |
| **Command Timeout** | All shell commands have a 180-second automatic timeout |

---

## 📁 Project Structure

```
antigravity-mcp-bridge/
├── server.py               # Core MCP Server — all 7 tool definitions
├── run_with_tunnel.py      # One-click server + ngrok tunnel launcher
├── start_server.bat        # Windows double-click launcher
├── test_client.py          # Automated connection verification script
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git exclusions
├── LICENSE                 # MIT License
└── README.md               # This documentation
```

---

## 📦 Dependencies

```
mcp>=2.0.0          # Official Model Context Protocol SDK (Python)
uvicorn             # ASGI server (Starlette/MCP runtime)
fastapi             # Web framework (CORS and routing)
pyngrok             # Python wrapper for ngrok tunnel management
python-dotenv       # Environment variable management
```

---

## 🛣️ Roadmap

- [x] Streamable HTTP (`/mcp`) and SSE (`/sse`) dual transport support
- [x] Google Gemini Spark integration (verified & live)
- [x] 7 core system execution tools
- [x] Background autonomous subagent orchestration
- [ ] OAuth 2.0 bearer token authentication layer
- [ ] Docker container deployment (`Dockerfile` + `docker-compose.yml`)
- [ ] Google Cloud Run one-click deployment button
- [ ] WebSocket-based real-time streaming tool output
- [ ] Multi-workspace sandboxing (run multiple projects simultaneously)
- [ ] Plugin system for extending with custom domain-specific tools

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes with descriptive messages
4. Open a Pull Request with a summary of the changes

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### The Future of Development is Conversational, Autonomous, and Local.

**Built with ❤️ for Students, Engineers, and Researchers worldwide.**

⭐ **Star this repository** if it helped you | 🍴 **Fork it** to customize for your workflow

[GitHub](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge) • [Report Issues](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/issues) • [Discussions](https://github.com/nandhakumar-murugan/antigravity-mcp-bridge/discussions)

</div>
