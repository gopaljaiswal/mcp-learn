import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# -------------------------------
# Sample Tools
# -------------------------------
async def echo_handler(arguments):
    """Echoes back the input."""
    return {"echo": arguments.get("text", "")}

async def add_handler(arguments):
    """Adds two numbers."""
    a = arguments.get("a")
    b = arguments.get("b")
    if a is None or b is None:
        raise ValueError("Both 'a' and 'b' are required.")
    return {"result": a + b}

TOOLS = {
    "echo": {
        "description": "Echoes back the provided text.",
        "schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to echo"}
            },
            "required": ["text"]
        },
        "handler": echo_handler
    },
    "add": {
        "description": "Adds two numbers.",
        "schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        },
        "handler": add_handler
    }
}

# -------------------------------
# REST API to get all tools
# -------------------------------
@app.get("/tools")
async def get_tools():
    tools_list = [
        {"name": name, "description": tool["description"], "inputSchema": tool["schema"]}
        for name, tool in TOOLS.items()
    ]
    return {"tools": tools_list}

# -------------------------------
# MCP Endpoint
# -------------------------------
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    body = await request.json()
    method = body.get("method")
    req_id = body.get("id")
    params = body.get("params", {})

    if method == "initialize":
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "capabilities": {"tools": True},
                    "serverInfo": {"name": "A Demo MCP Server", "version": "1.0.0"},
                },
            }
        )

    if method == "tools/list":
        tools_list = [
            {"name": name, "description": tool["description"], "inputSchema": tool["schema"]}
            for name, tool in TOOLS.items()
        ]
        return JSONResponse(content={"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

    if method == "tools/call":
        try:
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            if tool_name not in TOOLS:
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                    }
                )
            result = await TOOLS[tool_name]["handler"](arguments)
            content = [{"type": "text", "text": json.dumps(result, indent=2)}]
            return JSONResponse(content={"jsonrpc": "2.0", "id": req_id, "result": {"content": content}})
        except Exception as e:
            return JSONResponse(
                content={"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
            )

    return JSONResponse(
        content={"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {method} not found"}}
    )

if __name__ == "__main__":
    uvicorn.run("mcp:app", host="127.0.0.1", port=8000, reload=True)
