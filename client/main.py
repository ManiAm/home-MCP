
import asyncio
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

logging.basicConfig(level=logging.INFO, format='%(message)s')

log = logging.getLogger(__name__)

# Suppress HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("mcp.client.streamable_http").setLevel(logging.WARNING)

load_dotenv()


def print_tools(tools):

    for tool in tools:
        print(f"\n🔧 Tool: {tool.name}")
        print(f"Description: {tool.description}")


def print_banner(title):

    border = "=" * 80
    log.info("\n%s\n[User Question] %s\n%s\n", border, title, border)


def get_last_AI_message(message_list):

    for msg in reversed(message_list):

        if not isinstance(msg, AIMessage):
            continue

        content = msg.content.strip()
        if not content:
            continue

        return content

    return None


async def main():

    client = MultiServerMCPClient({
        "home": {
            "transport": "streamable_http",
            "url": "http://localhost:8089/mcp/"
        }
    })

    async with client.session("home") as home_session:

        tools = await load_mcp_tools(home_session)
        print_tools(tools)

        #####

        lite_llm_url = "http://apollo.home:4000"
        llm = ChatOpenAI(model="gpt-4o", base_url=lite_llm_url)
        agent = create_react_agent(llm, tools)

        #####

        user_questions = [
            "What is the time in Walnut Creek, CA?",
            "What is the time zone in Walnut Creek, CA?",
            "what's the timezone in Berlin?",

            "What is the current weather in Walnut Creek, CA ?",
            "What will the weather be like in Tokyo for the next 7 days?",

            "Get the current quote for Cisco Systems.",
            "Get company news for Cisco Systems from 2025-01-01 to 2025-04-01",
            "What is ticker symbol for microsoft?",
            "What are the top stock exchanges?",
            "Is US stock market open now?",
            "What are holidays for US stock market?",
            "What's the current market cap of NVIDIA?",
            "Compare NVIDIA stock price with Apple.",

            "Who owns SpaceX?",
            "What is Taylor Swift's net worth in 2025?"
        ]

        for user_question in user_questions:

            print_banner(user_question)

            response = await agent.ainvoke(
                {"messages": user_question},
                config={"recursion_limit": 10}
            )

            messages = response["messages"]
            final_answer = get_last_AI_message(messages)
            log.info("[Final Answer] %s", final_answer)

            # For debugging
            # for m in messages:
            #     print(f"[{m.__class__.__name__}] {m.content}")
            #     if hasattr(m, 'tool_calls'):
            #         print(f"Tool Calls: {m.tool_calls}")
            #     if hasattr(m, 'additional_kwargs'):
            #         print(f"Additional: {m.additional_kwargs}")


if __name__ == "__main__":

    asyncio.run(main())
