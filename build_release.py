"""
Local Automated Standalone Binary & Release Builder
Builds the standalone AntigravityBridge.exe locally without requiring cloud CI.
"""

import os
import sys
import subprocess
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def build():
    print("=" * 60)
    print("⚡ GEMINI ANTIGRAVITY BRIDGE - LOCAL RELEASE BUILDER")
    print("=" * 60)

    # 1. Run Tests First
    print("\n[1/3] Running Unit Test Suite...")
    test_proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT_DIR)
    if test_proc.returncode != 0:
        print("[ERROR] Tests failed! Aborting release build.")
        sys.exit(1)
    print("✅ All unit tests passed successfully!")

    # 2. Build PyInstaller Executable
    print("\n[2/3] Compiling Standalone Executable with PyInstaller...")
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--name", "AntigravityBridge",
        "--hidden-import", "uvicorn",
        "--hidden-import", "starlette",
        "--hidden-import", "pyngrok",
        "--hidden-import", "dotenv",
        "--hidden-import", "psutil",
        "--hidden-import", "mcp",
        "app_entry.py"
    ]
    build_proc = subprocess.run(cmd, cwd=ROOT_DIR)
    if build_proc.returncode != 0:
        print("[ERROR] PyInstaller build failed!")
        sys.exit(1)

    # 3. Copy .env into dist folder if present
    env_src = os.path.join(ROOT_DIR, ".env")
    env_dst = os.path.join(ROOT_DIR, "dist", "AntigravityBridge", ".env")
    if os.path.exists(env_src):
        shutil.copyfile(env_src, env_dst)

    exe_path = os.path.join(ROOT_DIR, "dist", "AntigravityBridge", "AntigravityBridge.exe")
    print("\n[3/3] Build Completed Successfully! 🚀")
    print("=" * 60)
    print(f"📦 Executable created at: {exe_path}")
    print("=" * 60)


if __name__ == "__main__":
    build()
