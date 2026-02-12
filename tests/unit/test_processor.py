"""
Unit tests for the Ono processor.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestProcessorBasic:
    """Test basic processor functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_llm = Mock()
        self.mock_llm.generate.return_value = "mock response"
        from ono.processor import Processor
        self.processor = Processor(self.mock_llm)

    def test_init(self):
        """Test processor initialization."""
        assert self.processor.llm == self.mock_llm

    def test_process_single_command(self):
        """Test processing single command."""
        command = "get current directory"
        self.mock_llm.generate.return_value = "pwd"
        
        result = self.processor.process(command)
        
        assert result == "pwd"

    def test_process_with_context(self):
        """Test processing command with context."""
        command = "get temp directory"
        from ono.context import Context
        context = Context()
        context.messages = []
        self.mock_llm.generate.return_value = "mktemp"
        
        result = self.processor.process(command, context)
        
        assert result == "mktemp"

    def test_process_multiple_commands(self):
        """Test processing multiple commands sequentially."""
        commands = ["get date", "get time"]
        self.mock_llm.generate.side_effect = ["date", "time"]
        
        results = []
        for cmd in commands:
            results.append(self.processor.process(cmd))
        
        assert len(results) == 2
        assert results[0] == "date"
        assert results[1] == "time"


class TestProcessorIntegration:
    """Test processor with mock LLM."""

    def test_process_command_generation(self):
        """Test generating command from natural language."""
        mock_llm = Mock()
        mock_llm.generate.return_value = "pwd"
        from ono.processor import Processor
        processor = Processor(mock_llm)
        
        result = processor.process("current directory")
        
        assert result == "pwd"

    def test_process_simple(self):
        """Test simple command processing."""
        mock_llm = Mock()
        mock_llm.generate.return_value = "pwd"
        from ono.processor import Processor
        processor = Processor(mock_llm)
        
        result = processor.process("test command")
        assert result == "pwd"
