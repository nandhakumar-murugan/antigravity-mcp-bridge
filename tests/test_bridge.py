"""
Unit and Integration Test Suite for Gemini Antigravity Bridge
Tests MCP server initialization, tool schemas, file operations, batch tools, and dashboard endpoints.
"""

import os
import sys
import unittest
import json
from starlette.testclient import TestClient

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server import (
    mcp, read_file, write_file, edit_file, append_file,
    list_directory, batch_write_files, run_batch_commands,
    create_full_project, get_bridge_history, save_session_note,
    get_session_notes, send_spark_to_antigravity_task,
    sync_project_to_gemini, request_gemini_brainstorm
)
from run_with_tunnel import create_app


class TestBridgeTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.abspath("test_sandbox")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_file_operations(self):
        """Test write, read, edit, append file tools."""
        test_file = os.path.join(self.test_dir, "sample.txt")

        # 1. Write file
        write_res = write_file(test_file, "Hello World!\nLine 2")
        self.assertIn("[Success]", write_res)
        self.assertTrue(os.path.exists(test_file))

        # 2. Read file
        content = read_file(test_file)
        self.assertEqual(content, "Hello World!\nLine 2")

        # 3. Edit file (search & replace)
        edit_res = edit_file(test_file, "World", "Gemini")
        self.assertIn("[Success]", edit_res)
        self.assertEqual(read_file(test_file), "Hello Gemini!\nLine 2")

        # 4. Append file
        append_res = append_file(test_file, "\nLine 3")
        self.assertIn("[Success]", append_res)
        self.assertIn("Line 3", read_file(test_file))

    def test_batch_write_files(self):
        """Test composite batch write tool."""
        files = {
            "module_a.py": "def a(): return 'A'",
            "module_b.py": "def b(): return 'B'",
            "sub/module_c.py": "def c(): return 'C'",
        }
        res = batch_write_files(files=files, base_dir=self.test_dir)
        self.assertIn("[Batch Write Complete]", res)
        self.assertIn("3/3 files written", res)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "sub", "module_c.py")))

    def test_run_batch_commands(self):
        """Test composite batch command execution."""
        commands = [
            "python -c \"print('Step 1 OK')\"",
            "python -c \"print('Step 2 OK')\"",
        ]
        res = run_batch_commands(commands=commands, working_dir=self.test_dir)
        self.assertIn("Step 1 OK", res)
        self.assertIn("Step 2 OK", res)
        self.assertIn("SUCCESS", res)

    def test_create_full_project(self):
        """Test 1-click full project creation tool."""
        files = {
            "app.py": "print('App running')",
            "README.md": "# Demo App",
        }
        setup_cmds = ["python -c \"print('Setup completed')\""]
        res = create_full_project(
            project_name="demo_app",
            files=files,
            setup_commands=setup_cmds,
            working_dir=self.test_dir
        )
        self.assertIn("Project Created: demo_app", res)
        self.assertIn("Setup completed", res)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "demo_app", "app.py")))

    def test_session_notes_and_history(self):
        """Test persistent memory and note logging."""
        save_res = save_session_note("Architecture decision: Use FastAPI", tag="decision")
        self.assertIn("[Success]", save_res)

        notes = get_session_notes(tag_filter="decision")
        self.assertIn("Architecture decision: Use FastAPI", notes)

        history = get_bridge_history(limit=5)
        self.assertIn("=== Bridge History", history)

    def test_sync_tools(self):
        """Test Antigravity ➔ Gemini synchronization tools."""
        sync_res = sync_project_to_gemini(
            project_name="TestApp",
            summary="Testing sync tool",
            tech_stack=["Python", "FastAPI"],
            key_files=["main.py"]
        )
        self.assertIn("[Success]", sync_res)


class TestDashboardAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = TestClient(self.app)

    def test_dashboard_page(self):
        """Test that the /dashboard web page loads with 200 OK."""
        res = self.client.get("/dashboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Gemini Antigravity Bridge", res.text)

    def test_root_redirect(self):
        """Test root / redirects to /dashboard."""
        res = self.client.get("/", follow_redirects=False)
        self.assertEqual(res.status_code, 307)
        self.assertEqual(res.headers["location"], "/dashboard")

    def test_api_status(self):
        """Test /api/status returns valid JSON structure."""
        res = self.client.get("/api/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("system", data)
        self.assertIn("cpu_percent", data["system"])

    def test_api_history(self):
        """Test /api/history returns history array."""
        res = self.client.get("/api/history")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("history", data)


if __name__ == "__main__":
    unittest.main()
