import os
import openai
import json
from dotenv import load_dotenv
from .prompts import parse_input_prompt

load_dotenv()

class LLMHelper:
    """
    AI wrapper for structured field inference and template enhancement.
    """

    def __init__(self, model_name="gpt-4", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def parse_user_input(self, text: str, fields: dict, required_fields: list) -> dict:
        """
        Convert raw user text into structured key-value suggestions for fields.
        required_fields: list of database fields to prioritize
        """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": parse_input_prompt(text=text,fields=fields,required_fields=required_fields)}],
            temperature=self.temperature,
        )
        content = response["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
        except:
            parsed = {}
        return parsed

    def suggest_enhancements(self, parsed_input: dict) -> dict:
        """
        Suggest enhancements for video template sections.
        """
        prompt = f"""
        You are a creative video assistant. 
        Given the following initial video idea data:
        {parsed_input}

        Suggest additional notes, shot ideas, lighting, mood, music, or creative enhancements.
        Return as JSON where keys are sections (Shot List, Mood/Atmosphere, Lighting, Soundtrack, Editing Notes, etc.)
        """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        content = response["choices"][0]["message"]["content"]

        import json
        try:
            enhancements = json.loads(content)
        except:
            enhancements = {}
        return enhancements# src/agents/ai_agent.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

class LLMHelper:
    """
    AI wrapper for structured field inference and template enhancement.
    """

    def __init__(self, model_name="gpt-4", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def parse_user_input(self, text: str, required_fields: list) -> dict:
        """
        Convert raw user text into structured key-value suggestions for fields.
        required_fields: list of database fields to prioritize
        """
        prompt = f"""
        You are an assistant that converts a user's video idea into structured data.
        Required fields: {required_fields}
        User input: {text}

        Return a JSON object mapping each required field to a suggested value.
        If the user did not provide enough info, leave the field empty.
        """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        content = response["choices"][0]["message"]["content"]

        # Attempt to parse JSON from LLM output
        import json
        try:
            parsed = json.loads(content)
        except:
            parsed = {}
        return parsed

    def suggest_enhancements(self, parsed_input: dict) -> dict:
        """
        Suggest enhancements for video template sections.
        """
        prompt = f"""
        You are a creative video assistant. 
        Given the following initial video idea data:
        {parsed_input}

        Suggest additional notes, shot ideas, lighting, mood, music, or creative enhancements.
        Return as JSON where keys are sections (Shot List, Mood/Atmosphere, Lighting, Soundtrack, Editing Notes, etc.)
        """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        content = response["choices"][0]["message"]["content"]

        import json
        try:
            enhancements = json.loads(content)
        except:
            enhancements = {}
        return enhancements