import argparse
from lark import Lark
from pathlib import Path
import os
import glob

def parse_ono_file(file_path):
    grammar_file = Path('./ono.lark')
    parser = Lark(grammar_file.read_text(), start='start')

    input_file = Path(file_path)
    try:
        tree = parser.parse(input_file.read_text())
        return tree.pretty()
    except Exception as e:
        return f"Error parsing {file_path}: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Ono files in a directory.")
    parser.add_argument("examples_dir", help="The directory containing the Ono files.")
    args = parser.parse_args()

    examples_dir = args.examples_dir

    # Get the list of ono files from the examples directory
    ono_files = glob.glob(os.path.join(examples_dir, "**/*.ono*"), recursive=True)

    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Parse each file and write the output to a file
    for file_path in ono_files:
        output_path = f"output/{Path(file_path).stem}.out"
        tree_string = parse_ono_file(file_path)
        with open(output_path, "w") as f:
            f.write(tree_string)
