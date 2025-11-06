from ..utils.notion_core import (
    get_notion_client,
    get_notion_database_id,
    get_notion_database_schema,
)


class SchemaAgent:
    def __init__(self):
        self.notion = get_notion_client()
        self.database_id = get_notion_database_id()
        self.schema = get_notion_database_schema(self.notion, self.database_id)

    def summarize_schema(self):
        summary = []
        for name, details in self.schema.items():
            prop_type = details["type"]
            summary.append(f"- {name} ({prop_type})")
        return "\n".join(summary)

    def get_required_fields(self):
        required = []
        for name, details in self.schema.items():
            if details["type"] in ["title", "select"]:
                required.append(name)
        return required

    def build_property_payload(self, user_inputs: dict):
        properties = {}
        for name, details in self.schema.items():
            if name not in user_inputs:
                continue
            value = user_inputs[name]
            prop_type = details["type"]

            if prop_type == "title":
                properties[name] = {"title": [{"text": {"content": value}}]}
            elif prop_type == "rich_text":
                properties[name] = {"rich_text": [{"text": {"content": value}}]}
            elif prop_type == "select":
                properties[name] = {"select": {"name": value}}
            elif prop_type == "multi_select":
                if isinstance(value, list):
                    properties[name] = {"multi_select": [{"name": v} for v in value]}
                else:
                    properties[name] = {"multi_select": [{"name": value}]}
            elif prop_type == "date":
                properties[name] = {"date": {"start": value}}
            elif prop_type == "number":
                properties[name] = {"number": float(value)}
            elif prop_type == "checkbox":
                properties[name] = {"checkbox": bool(value)}
            elif prop_type == "url":
                properties[name] = {"url": value}
            else:
                properties[name] = {"rich_text": [{"text": {"content": str(value)}}]}

        return properties
