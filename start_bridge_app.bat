@echo off
title Antigravity MCP Bridge - Control Center
color 0B

echo ============================================================
echo   ⚡ ANTIGRAVITY MCP BRIDGE - WINDOWS CONTROL CENTER
echo   Connecting Cloud AI (Gemini Spark) to Local Machine
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo [2/2] Launching Unified MCP Server and opening Dashboard...
echo.
python run_with_tunnel.py --open

pause
