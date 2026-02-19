"""Command-line interface for Ono."""

import typer
from typing import Optional
from .processor import Processor
from .llm import LLMClient
import sys
import os

app = typer.Typer()

def process_file(input_path: str, output_path: Optional[str] = None):
    """Process an Ono template file."""
    try:
        with open(input_path, 'r') as f:
            content = f.read()
        
        api_url = os.environ.get('ONO_API_URL', 'http://localhost:11434/v1')
        model = os.environ.get('ONO_MODEL', 'Qwen3-Coder-Next-Q4_K_M.gguf')
        
        llm = LLMClient(api_url=api_url, model=model)
        processor = Processor(llm)
        
        result = processor.process(content)
        
        if output_path is not None:
            with open(output_path, 'w') as f:
                f.write(result)
            print(f"Output written to {output_path}", file=sys.stderr)
        else:
            print(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

@app.command()
def process(
    input: str = typer.Argument(..., help="Input Ono file"),
    output: str = typer.Option(None, "-o", "--output", help="Output file path")
):
    """Process an Ono template file."""
    process_file(input, output)

@app.command()
def demo():
    """Show a demo of Ono functionality."""
    typer.echo("Ono - Universal AI-Powered Preprocessor")
    typer.echo("Set ONO_API_URL environment variable to use Ono.")
    typer.echo("Example: export ONO_API_URL=http://localhost:8000/v1")

def main():
    """Main entry point."""
    app()
