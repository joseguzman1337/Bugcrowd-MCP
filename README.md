# Bugcrowd MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that exposes the [Bugcrowd REST API](https://docs.bugcrowd.com/api/2025-04-23/) as callable tools for LLMs and AI agents. Built with [FastMCP](https://github.com/jlowin/fastmcp) and `httpx`.

## Features

- Full coverage of the Bugcrowd API (submissions, programs, engagements, disclosures, organisations, rewards, and more)
- Async requests via `httpx`
- Credentials loaded from environment variables or a `.env` file — nothing hardcoded
- Ready to use with Claude Desktop, VS Code Copilot, MCP Inspector, or any MCP-compatible client


Inspired by **[Mohd Haji Bugcrowd-MCP](https://github.com/mohdhaji87/Bugcrowd-MCP)**

## Setup

### 1. Clone and install

```sh
git clone <repo-url>
cd Bugcrowd-MCP
make install
```

### 2. Configure credentials

Create a `.env` file in the project root (it is gitignored):

```sh
BUGCROWD_API_USERNAME=your_api_username
BUGCROWD_API_PASSWORD=your_api_password
```

Alternatively, export them as shell environment variables.

### 3. Run the server

The server communicates over **stdio** — no HTTP port is opened.

```sh
python server.py
```

### 4. Connect to Claude Desktop

Add the following block to your Claude Desktop MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "BugcrowdMCP": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/Bugcrowd-MCP"
    }
  }
}
```

## Development

```sh
make format          # format with black
make format-check    # check formatting without writing changes
make test            # run unit tests (mocked, no credentials needed)
make test-integration  # run live API tests (requires .env credentials)
make clean           # remove build artefacts and caches
```

## Testing

Unit tests live in `tests/test_server.py` and mock all HTTP calls via `respx` — no real credentials are needed.

Integration tests are marked with `@pytest.mark.integration` and hit the live Bugcrowd API. They are skipped automatically if credentials are not present.
