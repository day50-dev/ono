#!/usr/bin/env python3
from . import parser

with open(sys.argv[1]) as f:
    text = f.read()

onoList = parser.get_ono_blocks(text)

