# LLM A가 플레이어 발화를 분석한 결과 형식을 정의

from pydantic import BaseModel

# LLM A가 플레이어 발화를 분석한 결과 형식
class AnalysisResult(BaseModel):
    intent: str
    emotion: str
    affinity_delta: int