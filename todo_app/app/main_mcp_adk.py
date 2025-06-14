import asyncio
import json
import logging  # Added logging
import os
import mcp.server.stdio  # For running as a stdio server
from app.schemas import todo as To
# ADK Tool Imports
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# MCP Server Imports
from mcp import types as mcp_types  # Use alias to avoid conflict
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from app.services.business.todo_service import TodoService

# --- Logging Setup ---
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "mcp_server_activity.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="w"),
    ],
)
# --- End Logging Setup ---

todo_service = TodoService()



# async def get_todos() -> list[dict]:
#     results = [dict(row) for row in todo_service.get_todos()]
#     #results = todo_service.get_todos()
#     print("Results ::" , results)
#     return results

async def get_todos() -> list[dict]: # Return type will be list of dicts after model_dump
    # todo_service.get_todos() returns list[TodoSchema]
    pydantic_models = todo_service.get_todos()
    # Convert Pydantic models to dicts for JSON serialization
    results = [model.model_dump(mode="json") for model in pydantic_models]
    logging.debug(f"get_todos results: {results}") # Use logging
    return results


async def create_todo(todo: dict):
    return todo_service.create_todo(todo)


async def get_todo_by_id(todo_id: dict[str, int]) -> dict:
    # todo_service.get_todos() returns list[TodoSchema]
    pydantic_model = todo_service.get_todo_by_id(todo_id=todo_id.get("id"))
    # Convert Pydantic models to dicts for JSON serialization
    result = pydantic_model.model_dump(mode="json")
    print("result ::",result)
    return result

async def get_todo_by_email(todo_id: dict[str, str]) -> list[dict]:
    # todo_service.get_todos() returns list[TodoSchema]
    pydantic_models = todo_service.get_todo_by_email(email=todo_id.get("email"))
    # Convert Pydantic models to dicts for JSON serialization
    results = [model.model_dump(mode="json") for model in pydantic_models]
    return results

async def update_todo(todo_id: int, todo: dict):
    return todo_service.update_todo(todo_id, todo)

async def delete_todo(todo_id: int):
    return todo_service.delete_todo(todo_id)


# --- MCP Server Setup ---
logging.info(
    "Creating MCP Server instance for SQLite DB..."
)  # Changed print to logging.info
app = Server("to-do-app-mcp-server")

# Wrap database utility functions as ADK FunctionTools
ADK_TODO_TOOLS = {
    "get_todos": FunctionTool(func=get_todos),
    "create_todo": FunctionTool(func=create_todo),
    "get_todo_by_id": FunctionTool(func=get_todo_by_id),
    "get_todo_by_email": FunctionTool(func=get_todo_by_email),
    "update_todo": FunctionTool(func=update_todo),
    "delete_todo": FunctionTool(func=delete_todo),
}


@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """MCP handler to list tools this server exposes."""
    logging.info(
        "MCP Server: Received list_tools request."
    )  # Changed print to logging.info
    mcp_tools_list = []
    for tool_name, adk_tool_instance in ADK_TODO_TOOLS.items():
        if not adk_tool_instance.name:
            adk_tool_instance.name = tool_name

        mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_instance)
        logging.info(  # Changed print to logging.info
            f"MCP Server: Advertising tool: {mcp_tool_schema.name}, InputSchema: {mcp_tool_schema.inputSchema}"
        )
        mcp_tools_list.append(mcp_tool_schema)
    return mcp_tools_list


@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """MCP handler to execute a tool call requested by an MCP client."""
    logging.info(
        f"MCP Server: Received call_tool request for '{name}' with args: {arguments}"
    )  # Changed print to logging.info

    if name in ADK_TODO_TOOLS:
        adk_tool_instance = ADK_TODO_TOOLS[name]
        try:
            adk_tool_response = await adk_tool_instance.run_async(
                args=arguments,
                tool_context=None,  # type: ignore
            )
            logging.info(  # Changed print to logging.info
                f"MCP Server: ADK tool '{name}' executed. Response: {adk_tool_response}"
            )
            response_text = json.dumps(adk_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            logging.error(
                f"MCP Server: Error executing ADK tool '{name}': {e}", exc_info=True
            )  # Changed print to logging.error, added exc_info
            error_payload = {
                "success": False,
                "message": f"Failed to execute tool '{name}': {str(e)}",
            }
            error_text = json.dumps(error_payload)
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        logging.warning(
            f"MCP Server: Tool '{name}' not found/exposed by this server."
        )  # Changed print to logging.warning
        error_payload = {
            "success": False,
            "message": f"Tool '{name}' not implemented by this server.",
        }
        error_text = json.dumps(error_payload)
        return [mcp_types.TextContent(type="text", text=error_text)]


# --- MCP Server Runner ---
async def run_mcp_stdio_server():
    """Runs the MCP server, listening for connections over standard input/output."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logging.info(
            "MCP Stdio Server: Starting handshake with client..."
        )  # Changed print to logging.info
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        logging.info(
            "MCP Stdio Server: Run loop finished or client disconnected."
        )  # Changed print to logging.info

# --- MCP Server Setup ---

if __name__ == "__main__":
    logging.info(
        "Launching MCP Server via stdio..."
    )  # Changed print to logging.info
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        logging.info(
            "\nMCP Server (stdio) stopped by user."
        )  # Changed print to logging.info
    except Exception as e:
        logging.critical(
            f"MCP Server (stdio) encountered an unhandled error: {e}", exc_info=True
        )  # Changed print to logging.critical, added exc_info
    finally:
        logging.info(
            "MCP Server (stdio) process exiting."
        )  # Changed print to logging.info