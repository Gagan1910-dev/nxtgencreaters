import httpx
import json
from app.core.config import settings
from app.models.schemas import BrandIdentity

class BrandingService:
    async def generate_brand_identity(self, idea: str, industry: str, tone: str) -> list[BrandIdentity]:
        if not settings.GROQ_API_KEY:
             # Fallback to mock if no key
             return self._mock_generation(idea, industry, tone)

        prompt = f"""
        Act as a professional branding agency.
        Generate 3 unique brand names and taglines for a business with this description: "{idea}".
        Industry: {industry}.
        Tone: {tone}.

        IMPORTANT: Brand names must be:
        - Simple and easy to understand
        - Clear and memorable
        - Use common English words or simple combinations
        - Avoid complex jargon or made-up words
        - Clearly convey the brand's purpose or values

        Return ONLY a JSON array with objects containing "name", "tagline", and an "score" (integer 1-100 indicating naming strength).
        Example: [{{"name": "X", "tagline": "Y", "score": 90}}]
        Do not output any markdown code blocks, just the raw JSON.
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
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Clean content if it has markdown ticks
                content = content.replace("```json", "").replace("```", "").strip()
                
                parsed = json.loads(content)
                return [BrandIdentity(**item) for item in parsed]

        except Exception as e:
            print(f"Branding Service Error: {e}")
            return self._mock_generation(idea, industry, tone)

    def _mock_generation(self, idea, industry, tone):
        # Fallback simulation
        return [
            BrandIdentity(name="SimuBrand", tagline="Simulation Mode Active", score=85),
            BrandIdentity(name="MockForge", tagline="Please add API Keys", score=88),
            BrandIdentity(name="DemoCo", tagline="Real AI Coming Soon", score=90)
        ]

branding_service = BrandingService()
