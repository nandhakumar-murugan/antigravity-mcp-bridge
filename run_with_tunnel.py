"""
Dual-Transport Launcher for Antigravity MCP Bridge
Serves both Streamable HTTP (/mcp) for Gemini Spark and SSE (/sse, /messages) for Antigravity IDE
on the SAME port (8000) over ngrok and localhost.
"""

import os
import uvicorn
from dotenv import load_dotenv
from pyngrok import ngrok, conf
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from server import mcp

load_dotenv()

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN")
PORT = 8000
HOST = "127.0.0.1"


async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "server": "Antigravity-System-Bridge",
        "endpoints": {
            "streamable_http": "/mcp",
            "sse": "/sse",
            "messages": "/messages"
        }
    })


def create_app() -> Starlette:
    app_sse = mcp.sse_app()
    app_streamable = mcp.streamable_http_app()

    combined_routes = [
        Route("/", health_check, methods=["GET"]),
        Route("/health", health_check, methods=["GET"]),
    ] + list(app_streamable.routes) + list(app_sse.routes)

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


def main():
    if not AUTHTOKEN:
        print("[WARNING] NGROK_AUTHTOKEN not set in environment or .env.")
    else:
        conf.get_default().auth_token = AUTHTOKEN

    print("[1/2] Connecting ngrok tunnel with host_header rewrite...")
    try:
        ngrok.kill()
        tunnel = ngrok.connect(PORT, "http", host_header="rewrite")
        public_url = tunnel.public_url.replace("http://", "https://")
        print("=" * 60)
        print("[INFO] DUAL-TRANSPORT NGROK MCP TUNNEL IS LIVE!")
        print(f"[GEMINI SPARK]  : {public_url}/mcp")
        print(f"[ANTIGRAVITY]   : http://127.0.0.1:{PORT}/sse")
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] ngrok tunnel error: {e}")

    app = create_app()

    print(f"\n[2/2] Starting Unified MCP Server on {HOST}:{PORT}...")
    print(f"      - Streamable HTTP: http://{HOST}:{PORT}/mcp")
    print(f"      - Server-Sent Events (SSE): http://{HOST}:{PORT}/sse")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
