import os
from typing import Optional, Dict, Any
from openai import OpenAI

from src.utils.prompts import get_professional_prompt

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OpenAI API key not found.")
            
        self.client = OpenAI(api_key=self.api_key)

    def get_professional_response(self, casual_text: str) -> str:
        prompt = self._build_prompt(casual_text)

        try:
            response = self.client.chat.completions.create(model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ],
            temperature=0.7,
            max_tokens=150)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return None

    def _build_prompt(self, casual_text: str) -> Dict[str, str]:
        system_prompt = get_professional_prompt()
        user_prompt = f"Transform this casual text into professional workplace language: '{casual_text}'"

        return {
            "system": system_prompt,
            "user": user_prompt
        }