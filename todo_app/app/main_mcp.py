from mcp.server.fastmcp import FastMCP
from app.services.business.todo_service import TodoService



todo_service = TodoService()
mcp = FastMCP("Todo App")


# Add an addition tool
@mcp.tool()
def get_todos():
    data =  todo_service.get_todos()
    print(data)
    return data
    #return "Hello World from FastMCP"

if __name__ == "__main__":
    mcp.run(transport="stdio")