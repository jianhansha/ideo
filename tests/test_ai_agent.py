import sys
import os

sys.path.append(os.path.abspath(".."))
from src.agents.ai_agent import LLMHelper
from src.agents.schema_agent import SchemaAgent

ai = LLMHelper()
Schema = SchemaAgent()


user_input = "I've got an idea for a new video. A moody night street scene, inspired by Blade Runner. I'll film it in London. I'll film this on the 10th of November and hope to publish it by the end of the month."

parsed_fields = ai.fill_db_fields(user_input, Schema.schema, Schema.get_required_fields())
assert isinstance(parsed_fields, dict)
print("parse_user_input output:")
for key,value in parsed_fields.items():
    if isinstance(value, dict):
        val = None
        for x, y in value.items():
            if x not in ("id", "name"):
                val = y
        print(f"{key}: {val}")
    else:
        print(f"{key}: {value}")

filled_markdown = ai.fill_markdown_template(user_input)
print(filled_markdown)