sys.path.append(os.path.abspath(".."))
from .parser import md_to_blocks
from .agents.schema_agent import SchemaAgent

def create_notion_ticket(client, database_id, template_md_path, user_inputs: dict):
    """
    Creates a Notion page in the given database using:
      - schema from SchemaAgent (dynamic properties)
      - markdown template for children blocks
      - user_inputs: dict of field_name -> value
    """

    schema_agent = SchemaAgent()

    properties_payload = schema_agent.build_property_payload(user_inputs)

    with open(template_md_path, "r") as f:
        md_content = f.read()
    template_blocks = md_to_blocks(md_content)

    response = client.pages.create(
        parent={"database_id": database_id},
        properties=properties_payload,
        children=template_blocks
    )

    print("Created Notion page:", response["id"])
    return response
