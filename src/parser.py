def md_to_blocks(md_text):
    """
    Convert markdown template into Notion-compatible blocks.
    Handles:
    - Headings (#, ##, ###)
    - Paragraphs
    - Quotes (> )
    - Bulleted lists (- )
    - Checklists (- [ ])
    - Bold (**text**) and italic (*text*)
    - Converts Production Timeline table into to_do items
    """

    def parse_annotations(text):
        annotations = {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        }

        text = text.strip()

        # Handle bold (**text**)
        if text.startswith("**") and text.endswith("**"):
            annotations["bold"] = True
            text = text[2:-2].strip()  # remove outer **

        # Handle italic (*text*)
        elif text.startswith("*") and text.endswith("*"):
            annotations["italic"] = True
            text = text[1:-1].strip()  # remove outer *

        # Remove any remaining stray asterisks at start/end
        text = text.lstrip("*").rstrip("*").strip()

        return text, annotations

    blocks = []
    for line in md_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Headings
        if line.startswith("# "):
            content, ann = parse_annotations(line[2:])
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )
        elif line.strip() == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif line.startswith("## "):
            content, ann = parse_annotations(line[3:])
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )
        elif line.startswith("### "):
            content, ann = parse_annotations(line[4:])
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )

        # Checklists / to_do
        elif line.startswith("- [ ] "):
            content, ann = parse_annotations(line[6:])
            blocks.append(
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ],
                        "checked": False,
                    },
                }
            )

        # Bulleted list items
        elif line.startswith("- "):
            content, ann = parse_annotations(line[2:])
            blocks.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )

        # Quotes
        elif line.startswith("> "):
            content, ann = parse_annotations(line[2:])
            blocks.append(
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )

        # Table simulation: detect "| Stage | Target Date | Done? |" and convert to to_do
        elif "|" in line and "Stage" in line and "Done?" in line:
            # skip table header line
            continue
        elif "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            stage = cells[0] if len(cells) > 0 else ""
            checked = "☑" in cells[2] if len(cells) > 2 else False
            if stage:
                content, ann = parse_annotations(stage)
                blocks.append(
                    {
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": content},
                                    "annotations": ann,
                                }
                            ],
                            "checked": checked,
                        },
                    }
                )

        # Paragraphs
        else:
            content, ann = parse_annotations(line)
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content},
                                "annotations": ann,
                            }
                        ]
                    },
                }
            )

    return blocks
