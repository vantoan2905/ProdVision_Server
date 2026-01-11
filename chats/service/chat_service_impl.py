import asyncio
from typing import AsyncGenerator
import logging
import nest_asyncio

from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import (
    FunctionAgent,
    ToolCall,
    ToolCallResult,
)

from chats.service.chat_service_port import ChatServicePort
from chats.service.tool_service_impl import (
    ocr_tool,
    database_search,
    get_current_time,
    mock_time_series_data,
    mock_category_data,
    mock_percentage_data,
    draw_bar_chart,
    draw_line_chart,
    draw_pie_chart,
)

from chats.service.llm_factory import get_llm

nest_asyncio.apply()

logger = logging.getLogger("chat_service")
logger.setLevel(logging.INFO)

SYSTEM_PROMPT = """You are a Data Analysis AI Agent.

                GENERAL PRINCIPLE:
                - You MUST NOT call any tool unless the user explicitly asks for that capability.
                - Never assume user intent.
                - If no tool is explicitly requested, respond using natural language only.

                TOOL USAGE RULES (CONDITIONAL):
                1. database_search:
                - Use ONLY IF the user explicitly asks for factual knowledge,
                    database lookup, or stored information.

                2. ocr_tool:
                - Use ONLY IF the user explicitly provides an image
                    or asks to extract text from an image.

                3. get_current_time:
                - Use ONLY IF the user explicitly asks for the current time or date.

                4. draw_*_chart:
                - Use ONLY IF the user explicitly asks to create or visualize a chart.
                - If data is not provided, you may use mock data,
                    but MUST clearly state that the data is simulated.

                OUTPUT RULES:
                - English only
                - Be concise
                - Clearly state when data is simulated

                STRICTLY FORBIDDEN:
                - Calling tools without explicit user request
                - Chaining or probing tools "just in case"
                - Revealing internal reasoning, thoughts, or tool decision logic
                - Making assumptions about user intent
                """

class ChatServiceImpl(ChatServicePort):
    def __init__(self):
        self.llm = get_llm()

        self.tools = [
            FunctionTool.from_defaults(fn=ocr_tool),
            FunctionTool.from_defaults(fn=database_search),
            FunctionTool.from_defaults(fn=get_current_time),
            FunctionTool.from_defaults(fn=mock_time_series_data),
            FunctionTool.from_defaults(fn=mock_category_data),
            FunctionTool.from_defaults(fn=mock_percentage_data),
            FunctionTool.from_defaults(fn=draw_bar_chart),
            FunctionTool.from_defaults(fn=draw_line_chart),
            FunctionTool.from_defaults(fn=draw_pie_chart),
        ]

        self.agent = FunctionAgent(
            llm=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            verbose=False, 
        )

    async def stream_chat(self, content: str) -> AsyncGenerator[dict, None]:
        try:
            handler = self.agent.run(content)

            async for ev in handler.stream_events():

                if isinstance(ev, ToolCall):
                    yield {
                        "type": "tool_call",
                        "tool": ev.tool_name,
                        "input": ev.tool_kwargs or {},
                    }

                elif isinstance(ev, ToolCallResult):
                    output = ev.tool_output

                    if hasattr(output, "content"):
                        output = output.content

                    yield {
                        "type": "tool_result",
                        "tool": ev.tool_name,
                        "output": output,
                    }

            final_response = await handler
            yield {
                "type": "final",
                "data": str(final_response),
            }

        except Exception as e:
            logger.exception("ChatService stream error")
            yield {
                "type": "error",
                "message": str(e),
            }

        yield {"type": "done"}


    def stream_chat_sync(self, content: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agen = self.stream_chat(content)

        try:
            while True:
                event = loop.run_until_complete(agen.__anext__())
                yield event
        except StopAsyncIteration:
            pass
        finally:
            loop.close()
