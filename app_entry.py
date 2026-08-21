"""
Standalone Windows Executable Entry Point for Antigravity MCP Bridge
"""

import sys
from run_with_tunnel import main

if __name__ == "__main__":
    # In desktop app mode, automatically open the dashboard in browser
    main(open_browser=True)
