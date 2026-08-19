import os
import sys
import uvicorn
from pyngrok import ngrok, conf
from server import app

AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN", "36nOKqLSzMkccTe8rmIIsWeoF3n_6SQiDNeFQoB8AvVGLSDHT")

def main():
    port = 8000
    host = "127.0.0.1"
    
    print("[1/2] Connecting ngrok tunnel...")
    conf.get_default().auth_token = AUTHTOKEN
    tunnel = ngrok.connect(port, "http")
    public_url = tunnel.public_url.replace("http://", "https://")
    
    print("=" * 60)
    print("NGROK TUNNEL IS LIVE!")
    print(f"PASTE THIS IN GEMINI SPARK: {public_url}/mcp")
    print("=" * 60)
    
    print(f"\n[2/2] Starting MCP Server on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
