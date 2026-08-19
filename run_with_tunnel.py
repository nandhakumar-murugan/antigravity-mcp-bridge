import os
import sys
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.routing import Route
from pyngrok import ngrok, conf
from server import mcp

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN", "36nOKqLSzMkccTe8rmIIsWeoF3n_6SQiDNeFQoB8AvVGLSDHT")

# Build SSE App with redirects for / and /mcp
sse_app = mcp.sse_app()

async def redirect_to_sse(request):
    return RedirectResponse(url="/sse", status_code=307)

app = Starlette(
    routes=[
        Route("/", redirect_to_sse),
        Route("/mcp", redirect_to_sse),
        *sse_app.routes,
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
    tunnel = ngrok.connect(port, "http")
    public_url = tunnel.public_url.replace("http://", "https://")
    
    print("=" * 60)
    print("NGROK TUNNEL IS LIVE!")
    print(f"PRIMARY MCP SSE URL: {public_url}/sse")
    print(f"ALT URL: {public_url}/mcp")
    print("=" * 60)
    
    print(f"\n[2/2] Starting Unified MCP Server on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
