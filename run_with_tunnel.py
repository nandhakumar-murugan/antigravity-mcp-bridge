"""
Dual-Transport Launcher & Live Dashboard for Antigravity MCP Bridge
Serves Streamable HTTP (/mcp), SSE (/sse, /messages), and Live Visual Web Dashboard (/dashboard, /)
on the SAME port (8000) over ngrok and localhost.
"""

import os
import webbrowser
import threading
import uvicorn
from dotenv import load_dotenv
from pyngrok import ngrok, conf
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.routing import Route
from server import mcp
from dashboard import DASHBOARD_ROUTES, set_public_url

load_dotenv()

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN")
PORT = 8000
HOST = "127.0.0.1"


async def root_redirect(request):
    return RedirectResponse(url="/dashboard")


def create_app() -> Starlette:
    app_sse = mcp.sse_app()
    app_streamable = mcp.streamable_http_app()

    combined_routes = [
        Route("/", root_redirect, methods=["GET"]),
    ] + DASHBOARD_ROUTES + list(app_streamable.routes) + list(app_sse.routes)

    combined_middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
            expose_headers=["*"],
        )
    ]

    return Starlette(
        routes=combined_routes,
        middleware=combined_middleware,
        lifespan=app_streamable.router.lifespan_context,
    )


def open_browser_delayed():
    import time
    time.sleep(1.5)
    webbrowser.open(f"http://127.0.0.1:{PORT}/dashboard")


def main(open_browser: bool = False):
    if not AUTHTOKEN:
        print("[WARNING] NGROK_AUTHTOKEN not set in environment or .env.")
    else:
        conf.get_default().auth_token = AUTHTOKEN

    print("[1/2] Connecting ngrok tunnel with host_header rewrite...")
    try:
        ngrok.kill()
        tunnel = ngrok.connect(PORT, "http", host_header="rewrite")
        public_url = tunnel.public_url.replace("http://", "https://")
        set_public_url(public_url)
        print("=" * 65)
        print("[INFO] DUAL-TRANSPORT NGROK MCP TUNNEL IS LIVE!")
        print(f"[DASHBOARD]     : http://127.0.0.1:{PORT}/dashboard")
        print(f"[GEMINI SPARK]  : {public_url}/mcp")
        print(f"[ANTIGRAVITY]   : http://127.0.0.1:{PORT}/sse")
        print("=" * 65)
    except Exception as e:
        print(f"[ERROR] ngrok tunnel error: {e}")

    app = create_app()

    if open_browser:
        threading.Thread(target=open_browser_delayed, daemon=True).start()

    print(f"\n[2/2] Starting Unified MCP Server & Dashboard on {HOST}:{PORT}...")
    print(f"      - Web Dashboard: http://{HOST}:{PORT}/dashboard")
    print(f"      - Streamable HTTP: http://{HOST}:{PORT}/mcp")
    print(f"      - Server-Sent Events (SSE): http://{HOST}:{PORT}/sse")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    import sys
    should_open = "--open" in sys.argv or "-o" in sys.argv
    main(open_browser=should_open)
