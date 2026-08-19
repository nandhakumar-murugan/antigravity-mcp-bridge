@echo off
title LocalTunnel for Antigravity MCP
cd /d "%~dp0"
echo ===================================================
echo   Starting Public Tunnel on Port 8000
echo ===================================================
echo.
npx localtunnel --port 8000
pause
