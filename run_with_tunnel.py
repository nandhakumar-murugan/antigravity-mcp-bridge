import os
import sys
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount
from pyngrok import ngrok, conf
from server import mcp

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN", "36nOKqLSzMkccTe8rmIIsWeoF3n_6SQiDNeFQoB8AvVGLSDHT")

# Extract SSE endpoint and Messages mount from MCPServer
sse_app = mcp.sse_app()
sse_route = [r for r in sse_app.routes if r.path == "/sse"][0]
messages_mount = [r for r in sse_app.routes if r.path == "/messages"][0]

# Universal App: Serves MCP SSE on /, /mcp, /sse
app = Starlette(
    routes=[
        Route("/", sse_route.endpoint),
        Route("/mcp", sse_route.endpoint),
        Route("/sse", sse_route.endpoint),
        messages_mount,
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)

def main():
    port = 8000
    host = "127.0.0.1"
    
    print("[1/2] Connecting ngrok tunnel...")
    conf.get_default().auth_token = AUTHTOKEN
    ngrok.kill()
    tunnel = ngrok.connect(port, "http", host_header="rewrite")
    public_url = tunnel.public_url.replace("http://", "https://")
    
    print("=" * 60)
    print("[INFO] NGROK MCP TUNNEL IS LIVE!")
    print(f"[LINK] PRIMARY MCP URL: {public_url}/sse")
    print(f"[LINK] ALT MCP URL:     {public_url}/mcp")
    print("=" * 60)
    
    print(f"\n[2/2] Starting Unified MCP Server on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
