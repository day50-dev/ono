"""
This module contains template helpers for Dockerfile format.
"""

def escape_string(text: str) -> str:
    """
    Escapes a string for use in Dockerfile.
    """
    # TODO: Implement Dockerfile-specific string escaping
    return text.replace("\\", "\\\\").replace("\"", "\\\"")