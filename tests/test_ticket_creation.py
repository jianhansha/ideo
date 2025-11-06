import sys
import os

sys.path.append(os.path.abspath(".."))
import src.utils.notion_utils as notion_client


notion = notion_client.get_notion_client()
database_id = notion_client.get_notion_database_id()
#template_id = notion_client.get_notion_template_id()
template_path = "../tools/Video Project Template.md"

user_inputs = {
    "Title": "Moody Night Street Scene",
    "Caption": "Inspired by Blade Runner aesthetics. Add slow dolly motion.",
    "Category": ["Lifestyle"],
    "Duration": 10,
    "Start Date": "2025-11-01",
    "End Date": "2025-11-10",
    "Status": "Idea",
    "Location": "New York",
    "Complexity": "Medium",
    "Song": "Song 1",
}

response = create_notion_ticket(notion, database_id, template_path, user_inputs)
print("New Ticket Created: " + response)
