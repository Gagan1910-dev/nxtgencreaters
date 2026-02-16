import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import SocialContent

class ContentService:
    async def generate_social_content(self, idea: str, name: str) -> List[SocialContent]:
        if not settings.GROQ_API_KEY:
            return self._mock_social(name)

        prompt = f"""
        Generate 3 social media posts for a new brand named "{name}". 
        Business Idea: {idea}.
        Platforms: LinkedIn, Twitter, Instagram.
        Return ONLY a JSON array of objects with keys: "platform", "content", "hashtags" (list of strings).
        Do not include markdown formatting.
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                import json
                data = response.json()
                content = data["choices"][0]["message"]["content"].replace("```json", "").replace("```", "").strip()
                parsed = json.loads(content)
                return [SocialContent(**item) for item in parsed]
        except Exception as e:
            print(f"Content Service Error: {e}")
            return self._mock_social(name)

    async def generate_email(self, name: str, idea: str) -> str:
        if not settings.GROQ_API_KEY:
            return f"Welcome to {name}! (Simulation Mode)"

        prompt = f"Write a short warm welcome email for a new customer of {name}, a brand about {idea}."
        
        try:
             async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                return response.json()["choices"][0]["message"]["content"]
        except:
            return "Welcome email generation failed."

    def _mock_social(self, name):
        return [
            SocialContent(platform="Error", content="Please configure GROQ_API_KEY in .env", hashtags=["#ConfigNeeded"])
        ]

content_service = ContentService()
