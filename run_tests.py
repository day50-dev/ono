#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pytest==8.3.3",
#     "pytest-asyncio==0.24.0",
#     "pytest-timeout==2.3.1",
#     "pytest-mock==3.14.0",
# ]
# ///

import pytest
import sys

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "--timeout=120", "tests/"]))
