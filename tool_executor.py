# 새로운 tavily 패키지 사용
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from cool_classes import SimpleAnswer, FinalAnswer

# 검색 도구 생성 (최대 5개 결과 반환)
tavily_tool = TavilySearch(max_results=5)

# 생성된 검색 쿼리들을 실행하는 함수
def run_queries(search_queries: list[str], **kwargs):
    results = []
    for query in search_queries:
        search_result = tavily_tool.invoke({"query": query})
        results.append(search_result)
    return results

# LangGraph에서 사용할 도구 노드 생성
tool_node = ToolNode(
    [
        # 검색어 생성용 도구
        StructuredTool.from_function(
            run_queries, 
            name=SimpleAnswer.__name__,
            description="Execute search queries to find information"
        ),
        # 최종 답변용 도구  
        StructuredTool.from_function(
            run_queries, 
            name=FinalAnswer.__name__,
            description="Execute search queries for final answer generation"
        ),
    ]
)