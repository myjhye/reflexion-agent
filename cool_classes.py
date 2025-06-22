from typing import List
from pydantic import BaseModel, Field

# 검색 기반 단순 답변 구조
class SimpleAnswer(BaseModel):
    search_queries: List[str] = Field(
        description="1-3 search queries to research the question."
    )

# 최종 답변 구조
class FinalAnswer(BaseModel):
    answer: str = Field(description="Comprehensive answer based on search results.")
    references: List[str] = Field(
        description="Source URLs used in the answer."
    )