from typing import List, Dict, Any
from ono.parser import OnoParser
from ono.llm import LLMClient
from ono.config import OnoConfig

class TwoPassProcessor:
    """
    A two-pass processing engine for Ono blocks.

    This class handles the processing of Ono blocks in two passes:
    1. Concept Pass: Focuses on semantic understanding and context injection.
    2. Syntax Pass: Focuses on format-specific syntax generation.
    """

    def __init__(self):
        """
        Initializes the TwoPassProcessor.
        """
        self.config = OnoConfig()
        self.llm_client = LLMClient()
        self.parser = OnoParser()

    def process(self, text: str) -> str:
        """
        Processes the input text, extracting Ono blocks, sending them to the LLM,
        and replacing them with the processed content.

        Args:
            text: The input text to process.

        Returns:
            The processed text.
        """
        parsed_content = self.parser.parse(text)
        ono_blocks = self.parser.extract_ono_blocks(parsed_content)

        processed_blocks = []
        for block in ono_blocks:
            try:
                response = self.llm_client.generate_text(block)
                processed_blocks.append(response)
            except Exception as e:
                print(f"Error processing block: {e}")
                return text  # Return original text in case of error

        # Replace Ono blocks with processed content
        output_text = text
        for i, block in enumerate(ono_blocks):
            output_text = output_text.replace(f"<?ono {block} ?>", processed_blocks[i])

        return output_text