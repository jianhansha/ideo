import os
import json
import openai
from dotenv import load_dotenv
from typing import Dict, List
from .prompts import fill_database_fields_prompt, fill_markdown_template_prompt
from src.utils.notion_core import NotionCore

load_dotenv()

class LLMHelper:
    """
    AI wrapper for structured field inference and template enhancement.
    """

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7, purpose: str = None):
        self.notion = NotionCore()
        self.model_name = model_name
        self.temperature = temperature
        self.purpose = purpose or os.getenv("AGENT_PURPOSE", "general purpose AI assistant")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        openai.api_key = api_key

    def _call_openai(self, prompt: str) -> str:
        """Helper method to call OpenAI chat completion."""
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return ""

    def fill_db_fields(self, text: str, fields: Dict[str, str], required_fields: List[str]) -> Dict:
        """
        Converts raw user text into structured key-value suggestions for database fields.
        """
        prompt = fill_database_fields_prompt(
            purpose=self.purpose,
            text=text,
            fields=fields,
            required_fields=required_fields,
        )
        print("Processing DB fields...")
        content = self._call_openai(prompt)
        if not content:
            return {}

        # Normalize and parse JSON
        try:
            content = content.replace("None", "null").replace("'", '"')
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            print("⚠️ Warning: Model returned invalid JSON. Returning empty dict.")
            return {}

    def fill_markdown_template(self, text: str) -> str:
        """
        Fills in a markdown template using user-provided text.
        Returns the completed markdown string.
        """
        template = self.notion.template_markdown
        prompt = fill_markdown_template_prompt(
            purpose=self.purpose,
            template=template,
            text=text,
        )
        print("Filling in markdown template...")
        content = self._call_openai(prompt)
        return content or template