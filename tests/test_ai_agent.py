import sys
import os

sys.path.append(os.path.abspath(".."))
from src.agents.ai_agent import LLMHelper
from src.agents.schema_agent import SchemaAgent

ai = LLMHelper()
Schema = SchemaAgent()

user_input = "I've got an idea for a new video. A moody night street scene, inspired by Blade Runner. I'll film it in London. I'll film this on the 10th of November and hope to publish it by the end of the month."
parsed = ai.parse_user_input(user_input, Schema.schema, Schema.get_required_fields())
assert isinstance(parsed, dict)
print("parse_user_input output:", parsed)

""" enhancements = ai.suggest_enhancements(parsed)
assert isinstance(enhancements, dict)
print("suggest_enhancements output:", enhancements) """