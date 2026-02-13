"""Processor for Ono blocks."""

import re
from typing import Optional, List
from ono.llm import LLMClient
from ono.parser import OnoParser, ParsedItem


class Processor:
    def __init__(self, llm: LLMClient, context=None):
        self.llm = llm
        self.context = context

    def _strip_markdown(self, text: str) -> str:
        """Strip markdown code blocks from response."""
        text = re.sub(r'^```[a-z]*\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n```$', '', text, flags=re.MULTILINE)
        text = text.strip('`')
        return text.strip()

    def _process_ono_blocks(self, text: str) -> str:
        """Process all <?ono ... ?> blocks in text."""
        parser = OnoParser()
        parsed = parser.parse(text)
        
        def process_parsed(items: List[ParsedItem]) -> str:
            result = []
            for item in items:
                if item.type == 'text':
                    result.append(item.content)
                elif item.type == 'ono':
                    # Extract the command from <?ono ... ?>
                    ono_cmd = item.content.strip()
                    # Call the LLM directly to process this command
                    processed = self._generate_code(ono_cmd)
                    result.append(processed)
            return ''.join(result)
        
        return process_parsed(parsed)

    def _generate_code(self, command: str, format_hint: str = None) -> str:
        """Generate code for a single command."""
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

    def process(self, command: str, context=None, format_hint: str = None):
        """Process a command through the LLM with prompt engineering."""
        # If this is a file with <?ono ?> blocks, process them
        if '<?ono' in command:
            return self._process_ono_blocks(command)
        
        return self._generate_code(command, format_hint)
