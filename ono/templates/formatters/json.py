"""
This module contains template helpers for JSON format.
"""

def escape_string(text: str) -> str:
    """
    Escapes a string for use in JSON.
    """
    # TODO: Implement JSON-specific string escaping
    return text.replace("\\", "\\\\").replace("\"", "\\\"")