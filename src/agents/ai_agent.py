import os
import openai
import json
from dotenv import load_dotenv
from .prompts import fill_database_fields_prompt,fill_markdown_template_prompt

load_dotenv()

class LLMHelper:
    """
    AI wrapper for structured field inference and template enhancement.
    """

    def __init__(self, model_name="gpt-4", temperature=0.7, purpose=None):
        self.model_name = model_name
        self.temperature = temperature
        self.purpose = purpose or "general purpose AI assistant"
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def set_purpose(self, purpose: str):
        """Update the agent's purpose dynamically (e.g. 'video production assistant')."""
        self.purpose = purpose

    def fill_db_fields(self, text: str, fields: dict, required_fields: list) -> dict:
        """
        Converts raw user text into structured key-value suggestions for database fields.
        """
        prompt = fill_database_fields_prompt(
            purpose=self.purpose,
            text=text,
            fields=fields,
            required_fields=required_fields,
        )

        try:
            print('Processing DB fields...')
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            content = response.choices[0].message.content.strip()
            content = content.replace("None", "null").replace("'", '"')
            parsed = json.loads(content)
            return parsed

        except json.JSONDecodeError:
            print("⚠️ Warning: Model returned invalid JSON. Returning empty dict.")
            return {}
        except Exception as e:
            print(f"❌ Error in fill_db_fields: {e}")
            return {}

    def fill_markdown_template(self, text: str, template: str) -> str:
        """
        Fills in a markdown template using user-provided text.
        Returns the completed markdown string.
        """
        prompt = fill_markdown_template_prompt(
            purpose=self.purpose,
            template=template,
            text=text,
        )

        try:
            print('Filling in markdown template...')
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            content = response.choices[0].message.content.strip()
            return content  

        except Exception as e:
            print(f"❌ Error in fill_markdown_template: {e}")
            return template  