"""
Test fixtures and configuration for Ono tests.
"""

import pytest
from pathlib import Path

TEST_MODEL = "qwen3:1.7b"
TEST_TIMEOUT = 120
TEST_LLM_URL = "http://10.0.0.221:11434/v1"
TEST_CONTEXT_STORAGE = "/tmp/ono_test_contexts"

TEST_TEMPLATES_DIR = Path(__file__).parent / "fixtures" / "test_templates"


@pytest.fixture
def temp_context_dir(tmp_path):
    """Provide a temporary directory for context storage."""
    return tmp_path / "contexts"


@pytest.fixture
def sample_ono_block():
    """Return a sample Ono block."""
    return '?ono get temp directory ?'


@pytest.fixture
def sample_ono_block_with_config():
    """Return a sample Ono block with configuration."""
    return '''?ono
model=qwen3:1.7b
temperature=0.2
get temp directory
?'''


@pytest.fixture
def sample_ono_with_nested():
    """Return text with nested Ono blocks."""
    return 'x = "?ono outer {?ono inner ?} ?"'
