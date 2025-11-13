import os
import sys

sys.path.append(os.path.abspath(".."))
import src.utils.notion_core as NC
from src.utils.notion_utils import create_notion_ticket

fields = {
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

response = create_notion_ticket(fields,NC.NotionCore().template_markdown)
print("New Ticket Created: " + response)
