from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()


def get_notion_client():
    return Client(auth=os.getenv("NOTION_API_KEY"))


def get_notion_database_id():
    NOTION_DATABASE_ID = (
        os.getenv("NOTION_DB_LINK").split("www.notion.so/")[1].split("?")[0]
    )
    return NOTION_DATABASE_ID


def get_notion_database(client, database_id):
    return client.databases.retrieve(database_id=database_id)


def get_notion_database_schema(client, database_id):
    db = get_notion_database(client, database_id)["data_sources"][0]["id"]
    properties = client.data_sources.retrieve(data_source_id=db)["properties"]
    return properties


def get_notion_template_id():
    NOTION_TEMPLATE_ID = (
        os.getenv("NOTION_TEMPLATE_LINK")
        .split("www.notion.so/")[1]
        .split("?")[0]
        .split("-")[-1]
    )
    return NOTION_TEMPLATE_ID