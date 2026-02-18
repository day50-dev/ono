#!/usr/bin/env python3
"""Ono template processor CLI."""

from typing import List, Optional
import sys
import os

# Import directly from the module to avoid circular dependency
from ono.parser import OnoParser
from ono.llm import LLMClient
from ono.processor import Processor
import typer

app = typer.Typer()

def get_format_from_filename(filename: str) -> Optional[str]:
    """Determine format from file extension."""
    ext = os.path.splitext(filename)[1]
    if ext == '.sh' or ext == '.bash':
        return 'bash'
    elif ext == '.py':
        return 'python'
    elif ext == '.json':
        return 'json'
    elif ext == '.yaml' or ext == '.yml':
        return 'yaml'
    elif ext == '.toml':
        return 'toml'
    elif ext == '.md':
        return 'markdown'
    return None

def process_ono_file(input_path: str, format: Optional[str] = None, output_path: Optional[str] = None):
    """Process an Ono template file."""
    with open(input_path, 'r') as f:
        content = f.read()
    
    parser = OnoParser()
    parsed = parser.parse(content)
    blocks = parser.extract_ono_blocks(parsed)
    
    if not blocks:
        result = content
    else:
        llm = LLMClient("http://localhost:11434/v1", "Qwen3-Coder-Next-Q4_K_M.gguf")
        processor = Processor(llm)
        
        # Determine format from filename or explicit option
        format_hint = format or get_format_from_filename(input_path)
        
        resolved_blocks = []
        for block in blocks:
            resolved = processor.process(block, format_hint=format_hint or 'bash')
            resolved_blocks.append(resolved)
        
        result = render_with_resolved(parsed, resolved_blocks)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(result)
    else:
        print(result)

def render_with_resolved(parsed: List, resolved_blocks: List[str]) -> str:
    result = []
    block_index = 0
    
    def render_items(items: List, depth=0) -> str:
        nonlocal block_index
        rendered = []
        for item in items:
            if item.type == 'text':
                rendered.append(item.content)
            elif item.type == 'ono':
                if block_index < len(resolved_blocks):
                    rendered.append(resolved_blocks[block_index])
                    block_index += 1
                else:
                    rendered.append(f'<?ono {item.content} ?>')
        return ''.join(rendered)
    
    return render_items(parsed)

@app.command()
def main(
    input_file: str = typer.Argument(..., help="Directory, file, or glob"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="File that establishes context"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Destination format"),
    backend: Optional[str] = typer.Option(None, "--backend", "-b", help="Backend type"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output location"),
):
    if os.path.isdir(input_file):
        for filename in os.listdir(input_file):
            if filename.endswith('.ono'):
                file_path = os.path.join(input_file, filename)
                out_path = os.path.join(output or '.', filename.replace('.ono', ''))
                process_ono_file(file_path, format, out_path)
    else:
        process_ono_file(input_file, format, output)

if __name__ == "__main__":
    app()
