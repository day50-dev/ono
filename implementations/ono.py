#!/usr/bin/env python3
import sys
import re

tokens = []
stack = []
rangeList = []

with open(sys.argv[1]) as f:
    text = f.read()

def delimiters_match(open, close):
    map = {'"': '"', 
           "'": "'", 
           '{': '}', 
           '[': ']',
           '<': '>'
           }

    if open in map:
        if close == map[open]:
            return True

for match in re.finditer(r'(["\'{<])\?ono\b|(\?["\'}>\]])' , text):
    if match.group(1):  # Opening: "?ono, {?ono, etc.
        tokens.append([match.start(), 'open', match.group(0)])
    else:  # Closing: ?", ?}, etc.
        tokens.append([match.start(), 'close', match.group(0)])

print(tokens)
for offset, token_type, token in tokens:
    if token_type == 'open':
        stack.append((offset, token))
    elif token_type == 'close' and stack:
        start_offset, opener = stack.pop()
        if delimiters_match(opener, token):
            rangeList.append((start_offset, offset + len(token)))

if len(rangeList) == 0:
    print(f"Nothing found for {text}")

for ra in rangeList:
    print(ra)
