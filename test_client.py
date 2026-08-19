import asyncio
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

SERVER_URL = "http://127.0.0.1:8000/sse"

async def main():
    print(f"Connecting to MCP Server at {SERVER_URL}...")
    async with sse_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n[OK] Connected successfully!")
            
            # List Tools
            tools = await session.list_tools()
            print("\n[TOOLS] Registered Tools:")
            for tool in tools.tools:
                print(f" - {tool.name}: {tool.description.splitlines()[0]}")
            
            # Test Tool Call
            print("\n[EXEC] Testing 'run_system_command' tool call:")
            result = await session.call_tool(
                "run_system_command", 
                {"command": "python --version"}
            )
            for content in result.content:
                print(content.text)

if __name__ == "__main__":
    asyncio.run(main())
