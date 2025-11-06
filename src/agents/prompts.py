def parse_input_prompt(fields: dict, required_fields: list, text: str) -> str:
    """
    Returns a prompt for converting user input into structured data.
    - fields: full database schema dictionary
    - required_fields: list of required field names
    - text: raw user input
    """
    return f"""
You are an assistant that converts a user's idea into structured data.
Database Schema: {fields}
Required fields: {required_fields}
User input: {text}

Return a JSON object mapping each field in the database schema to a suggested value.
If the user did not provide enough info, leave the field empty.
"""

def suggest_enhancements_prompt(parsed_input: dict) -> str:
    """
    Returns a prompt for generating creative enhancements for a video template.
    - parsed_input: dictionary of initial field values
    """
    return f"""
You are a creative video assistant.
Given the following initial video idea data:
{parsed_input}

Suggest additional notes, shot ideas, lighting, mood, music, and editing notes.
Return as JSON where keys are sections of the template (e.g., Shot List, Mood/Atmosphere, Lighting, Soundtrack, Editing Notes, etc.)
"""