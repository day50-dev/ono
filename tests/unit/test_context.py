"""
Unit tests for the Ono context manager.
"""

import pytest
import tempfile
import os
from ono.context import ContextManager


class TestContextManager:
    """Test context manager functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ContextManager(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_init_context_manager(self):
        """Test initializing context manager."""
        assert os.path.exists(self.temp_dir)

    def test_get_context(self):
        """Test getting context."""
        ctx = self.manager.get_context("test")
        assert ctx is not None
        assert hasattr(ctx, 'messages')

    def test_get_context_creates_dir(self):
        """Test that getting context creates directory."""
        ctx_path = os.path.join(self.temp_dir, "test")
        self.manager.get_context("test")
        assert os.path.exists(ctx_path)

    def test_update_context(self):
        """Test updating context."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        self.manager.update_context("test", messages)
        
        # Verify directory was created
        ctx_path = os.path.join(self.temp_dir, "test")
        assert os.path.exists(ctx_path)

    def test_cleanup_context(self):
        """Test cleaning up context."""
        self.manager.update_context("test", [])
        ctx_path = os.path.join(self.temp_dir, "test")
        assert os.path.exists(ctx_path)
        
        self.manager.cleanup_context("test")
        assert not os.path.exists(ctx_path)
