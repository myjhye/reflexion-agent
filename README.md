# 🤖 Simple RAG Agent

LangGraph와 Tavily 검색 API를 활용한 1-Step RAG 시스템

사용자 질문에 대해 실시간 웹 검색을 수행하고, 검색 결과를 바탕으로 인용이 포함된 종합적인 답변을 제공하는 AI 어시스턴트입니다.

## ✨ 주요 특징

- 🔍 **실시간 웹 검색**: Tavily API를 통한 최신 정보 수집
- ⚡ **빠른 응답**: 3단계 선형 워크플로우로 효율적인 처리
- 📚 **학술적 신뢰성**: 모든 답변에 출처 인용 및 참고문헌 포함
- 🎯 **구조화된 출력**: 일관된 형식의 답변 제공
- 🛠️ **높은 안정성**: 단순한 구조로 오류 최소화

## 🏗️ 시스템 구조

```
사용자 질문 입력
    ↓
1. 검색어 생성 (GPT-4가 효과적인 키워드 추출)
    ↓  
2. 웹 검색 실행 (Tavily API로 관련 정보 수집)
    ↓
3. 최종 답변 생성 (검색 결과 종합 + 인용 추가)
    ↓
답변 출력 완료
```

## 📋 필요 조건

- Python 3.8+
- OpenAI API 키
- Tavily API 키

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/simple-rag-agent.git
cd simple-rag-agent
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

#### API 키 발급 방법:
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Tavily**: [https://tavily.com](https://tavily.com)

### 5. 실행

```bash
python main.py
```

## 📁 프로젝트 구조

```
simple-rag-agent/
├── main.py              # 메인 실행 파일 및 워크플로우 관리
├── chains.py            # GPT-4 체인 설정 (검색어 생성 + 답변 생성)
├── tool_executor.py     # Tavily 검색 도구 설정
├── cool_classes.py      # Pydantic 데이터 모델 정의
├── requirements.txt     # 필요한 패키지 목록
├── .env                 # API 키 설정 파일
└── README.md           # 프로젝트 설명서
```

## 🔧 핵심 컴포넌트

### 📝 데이터 모델 (cool_classes.py)

```python
class SimpleAnswer(BaseModel):
    search_queries: List[str]  # 생성된 검색어들

class FinalAnswer(BaseModel):
    answer: str               # 최종 답변 내용
    references: List[str]     # 참고문헌 URL 목록
```

### 🔍 검색 시스템 (tool_executor.py)

- **TavilySearch**: 웹 검색 실행
- **run_queries**: 여러 검색어를 순차적으로 처리
- **ToolNode**: LangGraph와 검색 도구 연결

### 🧠 AI 체인 (chains.py)

- **query_generator**: 사용자 질문 → 효과적인 검색어 생성
- **answer_generator**: 검색 결과 → 종합적인 최종 답변 작성

### 🎛️ 워크플로우 관리 (main.py)

- **MessageGraph**: 3단계 순차 실행 관리
- **노드 연결**: generate_queries → search → generate_answer
- **결과 출력**: 답변 + 참고문헌 형식으로 표시

## 💡 사용 예시

### 입력:
```
"2024년 서울 아파트 가격 동향과 전망을 알려줘"
```

### 출력:
```
📝 답변:
==================================================
2024년 서울의 아파트 가격 동향은 전반적으로 상승한 것으로 보입니다. 
평균적으로 아파트가격은 평당 3861만원으로, 분양가는 4409만원으로 
상승하여 추가 고점을 찍었습니다[1]. 

상반기에는 부동산 관련 규제 완화, 대출상품 금리 감소, 투자 수요 
변동 등이 영향을 미쳤다고 분석되었습니다[2]...

🔗 참고문헌:
[1] https://news.example.com/real-estate-2024
[2] https://economy.example.com/housing-trends
[3] https://research.example.com/seoul-apartments
```

## 🎯 지원하는 질문 유형

- **부동산**: "서울 아파트 가격 동향"
- **건강**: "다이어트 운동법 추천"  
- **기술**: "AI 서비스 비교분석"
- **엔터테인먼트**: "넷플릭스 인기 드라마"
- **경제**: "비트코인 가격 분석"

## ⚙️ 커스터마이징

### 질문 변경
`main.py`의 `questions` 리스트를 수정하여 다른 질문들을 테스트할 수 있습니다:

```python
questions = [
    "당신의 질문을 여기에 추가하세요",
    "두 번째 질문",
    # ...
]
```

### 검색 결과 수 조정
`tool_executor.py`에서 `max_results` 값을 변경할 수 있습니다:

```python
tavily_tool = TavilySearch(max_results=10)  # 기본값: 5
```

## 🛠️ 문제 해결

### API 키 오류
```
❌ 오류 발생: API 키가 제대로 설정되었는지 확인하세요.
```
→ `.env` 파일의 API 키를 다시 확인해주세요.

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Tavily 패키지 오류
```bash
pip install langchain-tavily
```

## 📦 필요한 패키지

```txt
langchain
langchain-openai
langchain-tavily
langgraph
pydantic
python-dotenv
```
