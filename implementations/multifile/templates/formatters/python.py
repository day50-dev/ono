"""
This module contains template helpers for Python format.
"""

def escape_string(text: str) -> str:
    """
    Escapes a string for use in Python.
    """
    # TODO: Implement Python-specific string escaping
    return text.replace("\\", "\\\\").replace("\"", "\\\"")