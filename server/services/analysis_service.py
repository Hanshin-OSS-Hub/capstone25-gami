# 플레이어 발화를 분석하는 LLM A 로직이 들어갈 자리
#LLM A가 플레이어 발화를 분석하는 역할
#의도, 감정, 호감도 변화량 같은 구조화된 결과를 만듦
def analyze_player_text(user_text: str):
    return {
        "intent": "unknown",
        "emotion": "neutral",
        "affinity_delta": 0
    }