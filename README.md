# Antigravity & Local System MCP Bridge for Gemini Spark

This bridge allows **Gemini Spark** (or any external MCP client) to connect to your local computer and use Antigravity, execute terminal commands, edit code, and manage projects.

---

## 📁 Files Created
* [`server.py`](file:///C:/Users/smnk2/.gemini/antigravity/brain/b4f3a63b-2d56-4673-8117-91279693a131/scratch/antigravity-mcp-bridge/server.py): The MCP Server script.
* [`start_server.bat`](file:///C:/Users/smnk2/.gemini/antigravity/brain/b4f3a63b-2d56-4673-8117-91279693a131/scratch/antigravity-mcp-bridge/start_server.bat): Double-click launcher to run the server.

---

## 🛠️ How to Start & Connect

### 1. Launch the Server
Double-click `start_server.bat` or run:
```powershell
python server.py
```
Your server is now active on `http://localhost:8000/sse` (or stdio).

---

### 2. Expose the Server (For Cloud / External Agents)
If Gemini Spark runs in the cloud (web-based), expose your local port via **ngrok** or **Cloudflare**:

```powershell
ngrok http 8000
```
This gives you a public HTTPS URL like:
`https://your-subdomain.ngrok-free.app`

---

### 3. Add MCP Server in Gemini Spark
In Gemini Spark's MCP Settings:
* **Protocol**: SSE
* **URL**: `https://your-subdomain.ngrok-free.app/sse`

---

## 🧰 Available Tools for Gemini Spark
1. **`run_system_command(command, working_dir)`**: Runs PowerShell/CMD commands (e.g. `python main.py`, `npm test`, `git status`).
2. **`read_file(file_path)`**: Reads any project file.
3. **`write_file(file_path, content)`**: Writes/updates project code.
4. **`list_directory(directory_path)`**: Inspects workspace directory structures.
5. **`run_agent_task(prompt, workspace_dir)`**: Launches autonomous background AI coding agents.
6. **`get_agent_status(task_id)`**: Checks progress and retrieves task output.
7. **`terminate_task(task_id)`**: Stops running tasks.
