import typer
from typing import Optional

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
    print(f"Input: {input}")
    print(f"Context: {context}")
    print(f"Format: {format}")
    print(f"Output: {output}")

if __name__ == "__main__":
    app()