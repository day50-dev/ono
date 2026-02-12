"""
Unit tests for the Ono CLI.
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from ono import main


class TestCLI:
    """Test CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_with_input_file(self):
        """Test CLI with input file."""
        result = self.runner.invoke(main, ["input.txt"])
        assert result.exit_code == 0

    def test_cli_with_format_option(self):
        """Test CLI with format option."""
        result = self.runner.invoke(main, ["input.txt", "--format", "md"])
        assert result.exit_code == 0

    def test_cli_with_context_option(self):
        """Test CLI with context option."""
        result = self.runner.invoke(main, ["input.txt", "--context", "context.txt"])
        assert result.exit_code == 0

    def test_cli_with_backend_option(self):
        """Test CLI with backend option."""
        result = self.runner.invoke(main, ["input.txt", "--backend", "ollama"])
        assert result.exit_code == 0

    def test_cli_with_output_option(self):
        """Test CLI with output option."""
        result = self.runner.invoke(main, ["input.txt", "--output", "output.txt"])
        assert result.exit_code == 0

    def test_cli_with_all_options(self):
        """Test CLI with all options."""
        result = self.runner.invoke(main, [
            "input.txt",
            "--format", "md",
            "--context", "ctx.txt",
            "--backend", "ollama",
            "--output", "out.md"
        ])
        assert result.exit_code == 0


class TestCLIErrors:
    """Test CLI error handling."""

    def test_cli_missing_input(self):
        """Test CLI with missing input."""
        result = self.runner.invoke(main, [])
        assert result.exit_code != 0

    def test_cli_invalid_format(self):
        """Test CLI with invalid format."""
        result = self.runner.invoke(main, ["input.txt", "--format", "invalid"])
        assert result.exit_code == 0
