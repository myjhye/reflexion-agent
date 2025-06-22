from dotenv import load_dotenv
load_dotenv()  # .env 파일에서 API 키들 로드

from langgraph.graph import END, MessageGraph
from chains import query_generator, answer_generator
from tool_executor import tool_node

# MessageGraph 빌더 생성
builder = MessageGraph()

# 3개의 노드 추가 (단순한 순차 흐름)
builder.add_node("generate_queries", query_generator)  # 검색어 생성
builder.add_node("search", tool_node)                  # 검색 실행  
builder.add_node("generate_answer", answer_generator)  # 최종 답변 생성

# 순차적 연결 (단방향)
builder.add_edge("generate_queries", "search")     # 검색어 생성 → 검색
builder.add_edge("search", "generate_answer")      # 검색 → 답변 생성
builder.add_edge("generate_answer", END)           # 답변 생성 → 종료

# 시작점 설정
builder.set_entry_point("generate_queries")

# 그래프 컴파일 (실행 가능한 상태로)
graph = builder.compile()

if __name__ == "__main__":
    # 일반인 친화적 질문 예시들
    questions = [
        "2024년 서울 아파트 가격 동향과 전망을 알려줘",
        "다이어트에 효과적인 운동법과 식단을 추천해줘", 
        "ChatGPT와 같은 AI 서비스들의 장단점을 비교해줘",
        "넷플릭스에서 요즘 인기있는 한국 드라마들을 추천해줘",
        "비트코인과 이더리움 최근 가격 변화와 원인을 설명해줘"
    ]
    
    # 첫 번째 질문으로 테스트
    question = questions[0]
    
    try:
        print(f"질문: {question}")
        print("=" * 50)
        print("🔍 검색 중...")
        
        result = graph.invoke(question)
        
        print("\n📝 답변:")
        print("=" * 50)
        final_answer = result[-1].tool_calls[0]["args"]["answer"]
        print(final_answer)
        
        # 참고문헌 출력
        if "references" in result[-1].tool_calls[0]["args"]:
            print("\n🔗 참고문헌:")
            for i, ref in enumerate(result[-1].tool_calls[0]["args"]["references"], 1):
                print(f"[{i}] {ref}")
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("API 키가 제대로 설정되었는지 확인하세요.")