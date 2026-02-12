"""Processor for Ono blocks."""

from typing import Optional
from ono.llm import LLMClient


class Processor:
    def __init__(self, llm: LLMClient, context=None):
        self.llm = llm
        self.context = context

    def process(self, command: str, context=None, format_hint: str = None):
        """Process a command through the LLM with prompt engineering."""
        # Determine format from hint
        if format_hint == 'bash' or format_hint is None:
            # Default to bash-like commands for shell files
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable shell/bash code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Return a single command that achieves the goal. "
                "Be extremely concise."
            )
        elif format_hint == 'python':
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable Python code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Return a single expression or statement. "
                "Be extremely concise."
            )
        else:
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Be extremely concise."
            )
        
        user_prompt = f"Generate {format_hint or 'code'} to: {command}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.llm.generate(user_prompt, messages)
