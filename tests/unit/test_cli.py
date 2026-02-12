"""
Unit tests for the Ono CLI.
"""

import pytest
from unittest.mock import patch, Mock
from ono import main


class TestCLI:
    def test_cli_with_input_file(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt"]):
                main()

    def test_cli_with_format_option(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt", "--format", "md"]):
                main()

    def test_cli_with_context_option(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt", "--context", "ctx.txt"]):
                main()

    def test_cli_with_backend_option(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt", "--backend", "ollama"]):
                main()

    def test_cli_with_output_option(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt", "--output", "out.md"]):
                main()

    def test_cli_with_all_options(self):
        with patch("ono.OnoParser") as mock_parser:
            mock_instance = Mock()
            mock_instance.parse.return_value = []
            mock_instance.extract_ono_blocks.return_value = []
            mock_instance.render.return_value = ""
            mock_parser.return_value = mock_instance
            
            with patch("sys.argv", ["ono", "input.txt", "--format", "md", "--context", "ctx.txt", "--backend", "ollama", "--output", "out.md"]):
                main()
