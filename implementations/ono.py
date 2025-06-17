#!/usr/bin/env python3
import sys
import re
from pprint import pprint

with open(sys.argv[1]) as f:
    text = f.read()

def delimiters_match(open, close):
    map = {'"': '"', "'": "'", 
           '{': '}', '[': ']',
           '<': '>' }

    if open[0] in map:
        if close[-1] == map[open[0]]:
            return True

def find_blocks(text):
    tokenList = []

    for match in re.finditer(r'(["\'{<])\?ono\b|(\?["\'}>\]])' , text):
        if match.group(1):  # Opening: "?ono, {?ono, etc.
            tokenList.append([match.start(), 'open', match.group(0)])
        else:  # Closing: ?", ?}, etc.
            tokenList.append([match.start(), 'close', match.group(0)])
    return tokenList

def find_ranges(tokenList):
    stack = []
    rangeList = []

    for offset, token_type, token in tokenList:
        if token_type == 'open':
            stack.append((offset, token))
        elif token_type == 'close' and stack:
            start_offset, opener = stack.pop()
            if delimiters_match(opener, token):
                rangeList.append((start_offset, start_offset + len(opener), offset, offset + len(token)))
    return rangeList

def parse_ranges(rangeList, text):
    onoList = []
    for r in rangeList:
        ono = {'pos': r, 'orig': text[r[0]:r[3]], 'kv': {}, 'prompt': []}

        inner = text[r[1]:r[2]]

        for line in inner.split('\n'):
            iskv = re.match(r'^\s*([^\s]+)\s*=\s*([^\s]+)\s*$', line)
            if iskv:
                key, value = iskv.groups()
                ono['kv'][key] = value.strip('"\'')
            else:
                ono['prompt'].append(line)

        ono['prompt'] = "\n".join(ono['prompt']).strip()
        onoList.append(ono)
    return onoList

blockList = find_blocks(text)
rangeList = find_ranges(blockList)
onoList = parse_ranges(rangeList, text)


if len(onoList) == 0:
    print(f"Nothing found for {text}")

for ono in onoList:
    pprint(ono)
