"""Main package for Ono."""

import sys
import os
import importlib.util

module_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ono.py')
spec = importlib.util.spec_from_file_location("ono_module", module_path)
ono_module = importlib.util.module_from_spec(spec)
sys.modules['ono.ono_module'] = ono_module
spec.loader.exec_module(ono_module)

OnoParser = ono_module.OnoParser
main = ono_module.main
