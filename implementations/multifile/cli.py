import typer
from typing import Optional
from ono.parser import OnoParser
from ono.processor import TwoPassProcessor
from ono.config import OnoConfig

app = typer.Typer()

@app.command()
def main(
    input: str = typer.Argument(..., help="Directory, file, or list from globs like *.ono"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="File that establishes context"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Destination format, inferred from the file extension"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="A place to put the output of the program"),
):
    """
    Ono is a universal templating preprocessor that uses AI to solve those annoying
    cross-platform, language-specific problems you don't want to think about.
    """

    config = OnoConfig()
    processor = TwoPassProcessor()
    parser = OnoParser()

    try:
        with open(input, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {input}")
        return

    processed_text = processor.process(text)

    if output:
        try:
            with open(output, "w") as f:
                f.write(processed_text)
            print(f"Output written to: {output}")
        except Exception as e:
            print(f"Error writing to output file: {e}")
    else:
        print(processed_text)

if __name__ == "__main__":
    app()