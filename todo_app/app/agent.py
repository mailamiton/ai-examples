import sys

from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# IMPORTANT: Dynamically compute the absolute path to your server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "main_mcp_adk.py").resolve())
print("PATH_TO_YOUR_MCP_SERVER_SCRIPT :: ", PATH_TO_YOUR_MCP_SERVER_SCRIPT)

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="db_to_do_client_agent",
    instruction="""
    Analyze the list of 'To-Do' items and identify or create a new 'To-Do' based on the user's request.
    Ensure that the new 'To-Do' aligns with the user's specified needs and preferences. 
    Provide a detailed response that outlines the 'To-Do' item's description, priority, and any relevant deadlines.
    output :-
    1. Ensure that the new 'To-Do' aligns with the user's specified needs and preferences.
    2. Provide a detailed response that outlines the 'To-Do' item's description, priority, and any relevant deadlines.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python",
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
                timeout_sec=30,  # Timeout for MCP server process startup
            ),
            # tool_filter=['list_tables'] # Optional: ensure only specific tools are loaded
        )
    ],
)