"""
This module contains template helpers for Bash format.
"""

def escape_string(text: str) -> str:
    """
    Escapes a string for use in Bash.
    """
    # TODO: Implement Bash-specific string escaping
    return text.replace("'", "'\\''")