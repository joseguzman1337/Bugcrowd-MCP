const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { ListToolsRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const server = new Server({ name: "bugcrowd", version: "1.0.0" }, { capabilities: { tools: {} } });
server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: [{ name: "list_submissions", description: "List Bugcrowd submissions", inputSchema: { type: "object" } }] }));
const transport = new StdioServerTransport();
server.connect(transport);
