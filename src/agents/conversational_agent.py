from .schema_agent import SchemaAgent
from .ai_agent import LLMHelper
from typing import Dict

class ConversationalAgent:
    def __init__(self):
        self.schema_agent = SchemaAgent()
        self.llm = LLMHelper()
        self.final_payload = {}

    def interpret_input(self, user_input: str) -> Dict:
        """
        Parse the raw user input into initial field suggestions.
        Can use keyword matching, regex, or LLM parsing.
        """
        parsed = {}
        for field in self.schema_agent.schema:
            if field.lower() in user_input.lower():
                parsed[field] = user_input 
        return parsed

    def fill_missing_fields(self, parsed_input: Dict) -> Dict:
        """
        Check schema for required fields and ask the user for missing ones.
        """
        required = self.schema_agent.get_required_fields()
        for field in required:
            if field not in parsed_input:
                value = input(f"Please provide a value for {field}: ")
                parsed_input[field] = value
        return parsed_input

    def enhance_with_suggestions(self, parsed_input: Dict) -> Dict:
        """
        Optionally ask the LLM to suggest enhancements for template blocks.
        """
        enhanced_input = self.llm.suggest_enhancements(parsed_input)
        parsed_input.update(enhanced_input)
        return parsed_input

    def build_notion_payload(self, parsed_input: Dict) -> Dict:
        return self.schema_agent.build_property_payload(parsed_input)

    def run(self, user_input: str) -> Dict:
        parsed = self.interpret_input(user_input)
        parsed = self.fill_missing_fields(parsed)
        parsed = self.enhance_with_suggestions(parsed)
        payload = self.build_notion_payload(parsed)
        self.final_payload = payload
        return payload