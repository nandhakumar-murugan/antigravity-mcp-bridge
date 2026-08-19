import os
import sys
from pyngrok import ngrok, conf
from server import mcp

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN", "36nOKqLSzMkccTe8rmIIsWeoF3n_6SQiDNeFQoB8AvVGLSDHT")

def main():
    print("[1/2] Connecting ngrok tunnel...")
    conf.get_default().auth_token = AUTHTOKEN
    tunnel = ngrok.connect(8000, "http")
    public_url = tunnel.public_url.replace("http://", "https://")
    
    print("=" * 60)
    print("NGROK TUNNEL IS LIVE!")
    print(f"PASTE THIS IN GEMINI SPARK: {public_url}/mcp")
    print("=" * 60)
    
    print("\n[2/2] Starting MCP Server on port 8000 (Streamable HTTP /mcp)...")
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
