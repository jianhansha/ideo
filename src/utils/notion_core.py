from notion_client import Client
import os
from dotenv import load_dotenv
from notion_to_md import NotionToMarkdown
from .parser import parse_markdown_to_notion_blocks

load_dotenv()


class NotionCore:
    def __init__(self):
        self.client: Client = self._init_client()
        self.database_schema = self._get_database_schema()
        self.template_markdown = self._get_template_markdown()

    def _init_client(self) -> Client:
        """Initialize the Notion API client."""
        api_key = os.getenv("NOTION_SECRET")
        if not api_key:
            raise ValueError("NOTION_SECRET not set in environment")
        return Client(auth=api_key)

    def _get_database_id(self) -> str:
        """Extract database ID from environment variable link."""
        link = os.getenv("NOTION_DB_LINK")
        if not link:
            raise ValueError("NOTION_DB_LINK not set in environment")
        return link.split("www.notion.so/")[1].split("?")[0]

    def _get_database_schema(self):
        """Retrieve the database schema."""
        db = self.client.databases.retrieve(database_id=self._get_database_id())
        # Assuming your database has a data source at index 0
        data_source_id = db["data_sources"][0]["id"]
        properties = self.client.data_sources.retrieve(data_source_id=data_source_id)[
            "properties"
        ]
        return properties

    def _get_template_id(self) -> str:
        """Extract template ID from environment variable link."""
        link = os.getenv("NOTION_TEMPLATE_LINK")
        if not link:
            raise ValueError("NOTION_TEMPLATE_LINK not set in environment")
        return link.split("www.notion.so/")[1].split("?")[0].split("-")[-1]

    def _get_template_markdown(self):
        """Convert Notion template page to Markdown."""
        n2m = NotionToMarkdown(self.client)
        md_blocks = n2m.page_to_markdown(self._get_template_id())
        return n2m.to_markdown_string(md_blocks)["parent"]

    def _parse_markdown(self, input):
        return parse_markdown_to_notion_blocks(input)
