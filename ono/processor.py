"""Processor for Ono blocks."""

import re
from typing import Optional
from ono.llm import LLMClient


class Processor:
    def __init__(self, llm: LLMClient, context=None):
        self.llm = llm
        self.context = context

    def _strip_markdown(self, text: str) -> str:
        """Strip markdown code blocks from response."""
        # Remove markdown code blocks
        text = re.sub(r'^```[a-z]*\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n```$', '', text, flags=re.MULTILINE)
        # Remove any remaining backticks
        text = text.strip('`')
        return text.strip()

    def process(self, command: str, context=None, format_hint: str = None):
        """Process a command through the LLM with prompt engineering."""
        # Determine format-specific system prompt
        if format_hint == 'bash':
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable shell/bash code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Return a single command that achieves the goal. "
                "Be extremely concise. "
                "Example: whoami, pwd, echo $HOME, etc."
            )
            user_prompt = f"Write a bash command to: {command}"
        elif format_hint == 'python':
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable Python code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Return a single expression or simple statement. "
                "Be extremely concise. "
                "Do not use print() or other side effects. "
                "Example: os.getcwd(), os.getlogin(), etc."
            )
            user_prompt = f"Write Python code to: {command}"
        else:
            system_prompt = (
                "You are a code generation assistant. "
                "Respond with ONLY executable code. "
                "Do not provide explanations, conversational text, or markdown. "
                "Be extremely concise."
            )
            user_prompt = f"Generate code to: {command}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.generate(user_prompt, messages)
        return self._strip_markdown(response)
