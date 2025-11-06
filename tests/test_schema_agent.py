import sys
import os

sys.path.append(os.path.abspath(".."))
from src.utils.notion_core import Client
from src.agents.schema_agent import SchemaAgent

agent = SchemaAgent()

print("=== Database Schema ===")
print(agent.summarize_schema())

print("\n=== Required Fields ===")
print(agent.get_required_fields())

sample_input = {
    "Title": "AI Concept Test",
    "Duration": 40,
    "Location": "London",
    "Start Date": "2025-11-10",
}
props = agent.build_property_payload(sample_input)
print("\n=== Generated Properties ===")
print(props)
