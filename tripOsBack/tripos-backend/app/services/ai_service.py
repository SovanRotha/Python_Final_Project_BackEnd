from openai import OpenAI

from app.core.config import settings


class AIService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_response(self, message: str) -> str:
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=message,
        )

        return response.output_text