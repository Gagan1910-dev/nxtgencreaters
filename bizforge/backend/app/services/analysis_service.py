import httpx
from app.core.config import settings

class AnalysisService:
    async def analyze_sentiment(self, text: str) -> str:
        if not settings.HF_API_KEY:
            return "Sentiment Analysis (Simulation): Positive. Add HF_API_KEY for real analysis."

        API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {settings.HF_API_KEY}"},
                    json={"inputs": text}, 
                    timeout=10.0
                )
                data = response.json()
                # HF returns [[{'label': 'POSITIVE', 'score': 0.99}...]]
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    top_result = data[0][0] # Get valid top result
                    return f"Detected Sentiment: {top_result['label']} ({round(top_result['score']*100, 1)}%)"
                return "Sentiment analysis inconclusive."

        except Exception as e:
            print(f"Analysis Service Error: {e}")
            return "Sentiment analysis currently unavailable."

    async def summarize_description(self, text: str) -> str:
        if not settings.GROQ_API_KEY:
             return f"Summary (Simulation): {text[:50]}... (Add GROQ_API_KEY for real summary)"
        
        prompt = f"Summarize this brand description into a concise 2-sentence elevator pitch: '{text}'"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                     headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.5
                    },
                    timeout=30.0
                )
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Summarization Error: {e}")
            return "Summarization failed."

analysis_service = AnalysisService()
