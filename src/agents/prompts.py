def fill_database_fields_prompt(
    purpose: str, fields: dict, required_fields: list, text: str
) -> str:
    """
    Builds a structured prompt for mapping user input to a database schema.
    - purpose: short description of the agent's role (e.g., "video planning assistant")
    - fields: dictionary representing the full database schema
    - required_fields: list of field names that must not be left empty
    - text: raw user input to interpret
    """
    return f"""
You are an AI {purpose}.
Your task is to convert the user's free-form input into structured data according to the given database schema.

### Database Schema
{fields}

### Required Fields
{required_fields}

### User Input
{text}

### Output Rules
- Return a **strict JSON object** mapping each schema field to a suggested value.
- Do **not** include relational, dual property or nested fields that refer to other entities.
- Otherwise include **all other fields**, even if the value is empty.
- Use **null** for missing or unprovided values.
- If a field cannot be inferred reliably, leave it as null rather than guessing.
- Provide reasonable suggestions where possible based on context.
- Do **not** include Python-specific literals (like `None`, `True`, `False`).
- Output **only** the JSON object where all values in the dictionary are formatted to match the schema — no extra commentary or formatting.
    """


def fill_markdown_template_prompt(purpose: str, template: str, text: str) -> str:
    """
    Builds a structured prompt for filling a markdown template using user input.
    - purpose: short description of the agent's role (e.g., "video production assistant")
    - template: markdown template to be filled in
    - text: user input or description to interpret
    """
    return f"""
You are an AI {purpose}.
Your task is to interpret the user's input and populate the provided markdown template with relevant, structured content.

### Markdown Template
{template}

### User Input
{text}

### Output Rules
- Keep the same structure, formatting, and headings as the template.
- Fill in each section or bullet point using relevant information from the user input.
- If a section has no clear information, leave it empty (do not remove it).
- Maintain clean and readable markdown formatting.
- Do not include any text outside the completed markdown.
- Output **only** the completed markdown file content.
    """
