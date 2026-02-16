import httpx
from app.core.config import settings

class ChatService:
    async def chat_with_branding_assistant(self, message: str, context: str = "") -> str:
        if not settings.GROQ_API_KEY:
            return "I am the AI Branding Assistant. (Simulation Mode: Configure GROQ_API_KEY to chat)"

        system_prompt = f"""
        You are an elite AI Branding Consultant for the platform 'BizForge'.
        Your goal is to help users refine their brand identity, tagline, and strategy.
        
        Context about user's brand so far: {context}
        
        **RESPONSE GUIDELINES:**
        1. **Be Structured**: Use short paragraphs, bullet points, and clear headings.
        2. **Be Actionable**: Give concrete advice, not generic fluff.
        3. **Use Formatting**: Use **bold** for key terms and headlines.
        4. **Keep it Concise**: Avoid walls of text. Optimize for readability.
        
        Example Format:
        **Observation**
        Your idea is strong because...
        
        **Suggestions**
        • Tip 1
        • Tip 2
        
        **Next Step**
        Shall we refine the tagline?
        """
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": message}
                        ],
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Chat Error: {str(e)}"

chat_service = ChatService()
