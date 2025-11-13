import sys
import os
from .notion_core import NotionCore


sys.path.append(os.path.abspath(".."))
from src.agents.schema_agent import SchemaAgent


def create_notion_ticket(fields: dict, content: str):
    """
    Creates a Notion page in the given database using:
      - schema from SchemaAgent (dynamic properties)
      - markdown template for children blocks
      - user_inputs: dict of field_name -> value
    """

    schema_agent = SchemaAgent()

    properties_payload = schema_agent.build_property_payload(fields)

    notion = NotionCore()

    response = notion.client.pages.create(
        parent={"database_id": notion._get_database_id()}, properties=properties_payload
    )
    for block in notion._parse_markdown(content):
        notion.client.blocks.children.append(response["id"], children=[block])
    return response["id"]
