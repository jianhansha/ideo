import sys
import os
from os import environ

sys.path.append(os.path.abspath(".."))

import src.utils.notion_core as notion_client

print(notion_client.NotionCore()._get_template_markdown())