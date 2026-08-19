import os
import sys
from pyngrok import ngrok, conf
from server import mcp

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN", "36nOKqLSzMkccTe8rmIIsWeoF3n_6SQiDNeFQoB8AvVGLSDHT")

def main():
    port = 8000
    host = "127.0.0.1"
    
    print("[1/2] Connecting ngrok tunnel with host_header rewrite...")
    conf.get_default().auth_token = AUTHTOKEN
    ngrok.kill()
    tunnel = ngrok.connect(port, "http", host_header="rewrite")
    public_url = tunnel.public_url.replace("http://", "https://")
    
    print("=" * 60)
    print("[INFO] NGROK MCP TUNNEL IS LIVE!")
    print(f"[LINK] PASTE THIS IN GEMINI SPARK: {public_url}/mcp")
    print("=" * 60)
    
    print(f"\n[2/2] Starting Native Streamable HTTP MCP Server on {host}:{port}...")
    mcp.run(transport="streamable-http", host=host, port=port)

if __name__ == "__main__":
    main()
