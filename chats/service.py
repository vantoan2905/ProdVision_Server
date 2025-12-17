from typing import Generator, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

from chats.tools import (
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
from config import settings


class ChatService:
    """
    ChatService orchestrates interactions between:
    - Client
    - LLM Agent
    - Tool system (OCR, search, mock data, chart generation)

    Responsibilities:
    - Route user input to LLM
    - Allow LLM to call tools
    - Return final message + optional chart JSON to client
    """

    def __init__(self):
        llm = ChatOpenAI(
            model="glm-4-flash",
            temperature=0.6,
            openai_api_key=settings.BIGMODEL_KEY,
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
            streaming=True,
        )

        tools = [
            # Utility
            ocr_tool,
            database_search,
            get_current_time,

            # Mock data
            mock_time_series_data,
            mock_category_data,
            mock_percentage_data,

            # Chart generation (JSON only)
            draw_bar_chart,
            draw_line_chart,
            draw_pie_chart,
        ]

        self.llm = llm.bind_tools(tools)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Bạn là AI Agent chuyên phân tích dữ liệu.

                    QUY TẮC BẮT BUỘC:

                    1. TRI THỨC
                    - Nếu câu hỏi cần kiến thức → gọi database_search

                    2. OCR
                    - Nếu người dùng đưa ảnh → gọi ocr_tool

                    3. THỜI GIAN
                    - Nếu hỏi thời gian hiện tại → gọi get_current_time

                    4. DỮ LIỆU & BIỂU ĐỒ
                    - Nếu cần vẽ biểu đồ nhưng KHÔNG có dữ liệu thật:
                      → gọi mock_*_data
                    - Sau khi có dữ liệu → gọi draw_bar_chart / draw_line_chart / draw_pie_chart
                      → Trả JSON chart, KHÔNG vẽ ảnh

                    5. OUTPUT
                    - Trả lời tiếng Việt
                    - Ngắn gọn, rõ ràng
                    - Nếu dữ liệu là giả lập → nói rõ
                    

                    *** RISK *** :  Tuyệt đối không tự vẽ biểu đồ
                    """
                    
                ),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt,
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=True,
        )

    def stream_chat(
        self, user_input: str
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Streaming chat handler (SSE compatible).

        Yields:
            {
                "type": "text",
                "content": str
            }
            or
            {
                "type": "chart",
                "chart_type": str,
                "title": str,
                "data": Dict[str, Any]   # JSON chart data
            }
        """

        chart_payload: Optional[Dict[str, Any]] = None

        for event in self.executor.stream({"input": user_input}):

            # ----------------------------------------
            # TOOL MESSAGE
            # ----------------------------------------
            if isinstance(event, ToolMessage):

                if event.name in {
                    "draw_bar_chart",
                    "draw_line_chart",
                    "draw_pie_chart",
                }:
                    # event.content contains chart JSON
                    chart_payload = event.content

                continue

            # ----------------------------------------
            # FINAL LLM OUTPUT
            # ----------------------------------------
            if "output" in event:
                yield {
                    "type": "text",
                    "content": event["output"],
                }

        # ----------------------------------------
        # SEND CHART JSON AFTER TEXT
        # ----------------------------------------
        if chart_payload:
            yield {
                "type": "chart",
                "chart_type": chart_payload.get("type"),
                "title": chart_payload.get("title"),
                "data": chart_payload.get("data"),
            }
