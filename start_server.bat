@echo off
title Antigravity MCP Bridge (Server + Ngrok)
cd /d "%~dp0"
echo ===================================================
echo   Starting Antigravity MCP Server + Ngrok Tunnel
echo ===================================================
echo.
python run_with_tunnel.py
pause
