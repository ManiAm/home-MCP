
# The Model Context Protocol (MCP)

The Model Context Protocol (MCP) is an open standard, open-source framework to standardize the way artificial intelligence systems like large language models (LLMs) integrate and share data with external tools, systems, and data sources. MCP provides a universal interface for reading files, executing functions, and handling contextual prompts.

In agent-based architectures, MCP allows language models to behave like intelligent orchestrators that can dynamically select and invoke tools based on user input and context. For example, a reasoning agent can query weather APIs, search documents, call financial calculators, or interact with vector databases all via MCP-defined tool interfaces. This makes MCP a key enabler of tool-augmented agents, where reasoning and action are cleanly separated.

MCP was initially developed by [Anthropic](https://modelcontextprotocol.io/docs/getting-started/intro) to power multi-agent communication between Claude-based tools. However, the protocol quickly gained traction due to its practical benefits and is now community-driven and open-source. You can find the specification in [here](https://github.com/modelcontextprotocol/modelcontextprotocol). While not yet ratified by a formal standards body (like IEEE or IETF), it is becoming an emerging de facto standard in the open LLM tooling ecosystem.

## MCP Communication Model

MCP is fundamentally a client-server protocol:

- The **MCP server** is the execution engine. It manages functions (called tools) that can be invoked remotely. It listens for incoming JSON-RPC requests over supported transports, executes the specified tool or chain, and returns the result. It exposes schemas and capabilities (via `describe` methods) that let clients know which tools are available, what inputs they expect, and how to use them.

- The **MCP client** is the initiator and orchestrator. It fetches tool descriptions from the server and uses them to dynamically build user interfaces or invoke functions programmatically. It constructs JSON-RPC calls containing the method name (tool) and parameters, then sends them to the server. It parses the result or error returned by the server and acts accordingly (e.g., renders output, continues a chain of reasoning, retries on error).

## MCP Transport

MCP transport refers to the underlying communication mechanism used to transmit requests and responses between the client and the server. While MCP defines a standard format for interactions using JSON-RPC 2.0, the transport specifies how those structured messages are physically delivered over the network or between processes. In other words, MCP is transport-agnostic. It defines how to structure messages, not how they’re delivered. Three supported transports are:

- `stdio` (Standard Input/Output Transport): The stdio transport enables communication between the MCP client and server using standard input (stdin) and standard output (stdout) streams. This transport is ideal for local or embedded environments where the MCP server runs as a subprocess, such as within a CLI tool, IDE extension, or an automation script. Because it bypasses network overhead and relies on direct process I/O, stdio is lightweight and efficient for fast, synchronous interactions. It’s especially well-suited for tools that launch ephemeral AI subprocesses or integrate tightly with local development environments.

- `sse` (Server-Sent Events Transport): This transport leverages a unidirectional streaming model over HTTP, allowing the MCP server to continuously push data to the client in real time. Built on the standard `text/event-stream` content type, sse is commonly used when the server needs to stream incremental results, such as token-by-token generation from an LLM or progress updates during long-running operations. While the communication only flows from server to client, the initial request is still initiated by the client using a standard HTTP request. sse is a good fit for browser-based or real-time applications where low-latency updates are essential but bidirectional communication is not required.

- `streamable-http` (Streamable HTTP Transport): The streamable-http transport is a persistent, bidirectional communication channel built on top of HTTP, designed to support more complex, interactive workloads. Unlike traditional request-response HTTP or unidirectional sse, this transport enables two-way streaming, allowing the client to send a request and receive incremental or chunked responses from the server over time while still preserving the structure of JSON-RPC 2.0. This makes it ideal for conversational agents, toolchains with dynamic intermediate steps, and frontends that require fine-grained control over tool execution and output handling. It is particularly optimized for modern web environments where responsiveness and flexibility are critical.

## Centralized Tool Hosting

Centralized Tool Hosting is one of the core use cases enabled by MCP’s client-server architecture. A single MCP server acts as the authoritative host for a collection of reusable tools such as AI inference functions, data enrichment utilities, code formatters, or mathematical solvers. These tools are implemented and maintained on the server, and made accessible through a standardized JSON-RPC interface. This eliminates the need for individual clients or projects to duplicate logic, set up local environments, or manage dependencies for each tool.

By centralizing tools on an MCP server, multiple clients (whether CLI tools, web applications, LangChain agents, or automation pipelines) can interact with the same functionality in a consistent, structured, and version-controlled manner. This promotes reusability, reduces resource overhead, and ensures that updates to tool logic are immediately reflected for all consumers. It also allows teams to separate tool development and usage, fostering modularity and enabling faster iteration across projects that rely on shared AI or data-processing capabilities.

This architecture is especially valuable in environments like research labs, enterprise AI platforms, or devops automation frameworks where a curated set of tools needs to be shared across workflows, users, or systems without requiring redundant setup.

## MCP Implemetations

MCP has growing adoption across the open-source ecosystem, with implementations emerging in multiple programming languages, including Python, JavaScript (Node.js), Rust, and Go. This cross-language support enables integration of tools and services into LLM workflows, regardless of the underlying tech stack. Notable Python implementations are:

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk): This is the official reference Python implementation of the MCP, offering both a client and server framework to build MCP-compliant systems. It simplifies the process of creating servers that expose models or tools via MCP, with built-in support for multiple transports. The SDK provides foundational base classes and utilities for handling JSON-RPC messaging, tool registration, and schema introspection.

- [LangChain MCP Adapter](https://github.com/langchain-ai/langchain-mcp-adapters): The LangChain MCP Adapter acts as a bridge between LangChain’s agent and toolchain ecosystem and any MCP-compliant server, enabling interoperability. As an adapter in the software design sense, it converts LangChain’s internal model calls into MCP-compliant JSON-RPC requests and handles the corresponding responses, including token streaming and error propagation. This allows LangChain to treat any MCP server as a first-class LLM provider without requiring specialized integration logic. It decouples the LLM backend from LangChain’s core, promoting flexibility and modularity.
