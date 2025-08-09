
import logging

from mcp.server.fastmcp import FastMCP
from langchain_mcp_adapters.tools import to_fastmcp

from tools.generate_tools import generate_tools_from_client
from tools.tools_duckduckgo import DuckDuckGoSearch
from tools.tools_stock import LLM_Stock
from tools.tools_tz import TZ_Info
from tools.tools_weather import Weather_Info
from tools.tools_gmail import Gmail_tool
from tools.tools_calendar import Tool_Calendar
from tools.tools_spotify import Tool_Spotify

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)

# Suppress HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)


if __name__ == "__main__":

    tools = generate_tools_from_client([
        DuckDuckGoSearch(),
        LLM_Stock(),
        TZ_Info(),
        Weather_Info(),
        Gmail_tool(),
        Tool_Calendar(),
        Tool_Spotify()
    ])

    mcp_tools = [to_fastmcp(tool) for tool in tools]

    mcp = FastMCP(
        "Home-MCP",
        host="0.0.0.0",
        port=8089,
        tools=mcp_tools)

    mcp.run(transport="streamable-http")
