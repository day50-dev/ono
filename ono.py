#!/usr/bin/env python3
"""Ono - AI-powered templating language processor."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import ono_cli directly from the module file
import importlib.util
spec = importlib.util.spec_from_file_location("ono_cli_module", os.path.join(os.path.dirname(__file__), "ono_cli.py"))
ono_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ono_cli)

if __name__ == "__main__":
    sys.exit(ono_cli.app())
