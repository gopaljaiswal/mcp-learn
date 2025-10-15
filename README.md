# mcp-learn
Code for MCP

# MCP Server Example

This project provides a simple MCP (Model Context Protocol) server using FastAPI, with sample tools.

## Requirements
- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

Start the server on localhost (port 8000):

```bash
python mcp.py
```

The server will be available at http://127.0.0.1:8000/mcp

## Example Usage

You can test the MCP endpoint using `curl` or any API client (like Postman).

### List Tools
```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"method": "tools/list", "id": 1}'
```

### Call Echo Tool
```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"method": "tools/call", "id": 2, "params": {"name": "echo", "arguments": {"text": "hello"}}}'
```

### Call Add Tool
```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"method": "tools/call", "id": 3, "params": {"name": "add", "arguments": {"a": 2, "b": 3}}}'
```
