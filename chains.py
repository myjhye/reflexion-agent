from dotenv import load_dotenv
load_dotenv()  # .env 파일에서 환경변수 로드
import datetime

from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from cool_classes import SimpleAnswer, FinalAnswer

# GPT-4 모델 초기화
llm = ChatOpenAI(model="gpt-4")
parser = JsonOutputToolsParser(return_id=True)

# 검색어 생성용 프롬프트 템플릿
query_generator_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a research assistant.
            Current time: {time}

            Your task: Generate 1-3 effective search queries to research the user's question.
            Make the search queries specific and focused to get the most relevant information.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Generate search queries using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

# 최종 답변 생성용 프롬프트 템플릿  
answer_generator_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher.
            Current time: {time}

            Your task: Write a comprehensive answer based on the search results provided.
            - Include specific details and facts from the search results
            - Add numerical citations [1], [2], etc. for verification
            - Create a References section with source URLs
            - Keep the answer informative but concise""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Write your final answer using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

# 검색어 생성 체인
query_generator = query_generator_template | llm.bind_tools(
    tools=[SimpleAnswer], tool_choice="SimpleAnswer"
)

# 최종 답변 생성 체인
answer_generator = answer_generator_template | llm.bind_tools(
    tools=[FinalAnswer], tool_choice="FinalAnswer"
)