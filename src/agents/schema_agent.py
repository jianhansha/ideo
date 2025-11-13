from typing import Dict, List, Any
from ..utils.notion_core import NotionCore

class SchemaAgent:
    """
    Handles Notion database schema operations such as summarizing fields,
    identifying required fields, and building property payloads for API requests.
    """

    def __init__(self):
        self.schema = NotionCore().database_schema

    def summarize_schema(self) -> str:
        """Returns a human-readable summary of the schema."""
        summary = [f"- {name} ({details['type']})" for name, details in self.schema.items()]
        return "\n".join(summary)

    def get_required_fields(self) -> List[str]:
        """Returns a list of required field names based on type."""
        return [name for name, details in self.schema.items() if details["type"] in ["title", "select"]]

    def _format_property(self, name: str, value: Any, prop_type: str) -> Dict:
        """Helper to format a single property for Notion API."""
        if prop_type == "title":
            return {name: {"title": [{"text": {"content": str(value)}}]}}
        if prop_type == "rich_text":
            return {name: {"rich_text": [{"text": {"content": str(value)}}]}}
        if prop_type == "select":
            return {name: {"select": {"name": str(value)}}}
        if prop_type == "multi_select":
            values = value if isinstance(value, list) else [value]
            return {name: {"multi_select": [{"name": str(v)} for v in values]}}
        if prop_type == "date":
            return {name: {"date": {"start": str(value)}}}
        if prop_type == "number":
            return {name: {"number": float(value)}}
        if prop_type == "checkbox":
            return {name: {"checkbox": bool(value)}}
        if prop_type == "url":
            return {name: {"url": str(value)}}
        # Fallback to rich_text for unknown types
        return {name: {"rich_text": [{"text": {"content": str(value)}}]}}

    def build_property_payload(self, user_inputs: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Converts user input into Notion API property payload format.
        Only includes fields present in both the schema and the user input.
        """
        properties = {}
        for name, details in self.schema.items():
            if name in user_inputs:
                properties.update(self._format_property(name, user_inputs[name], details["type"]))
        return properties