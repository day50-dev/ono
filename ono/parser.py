"""Ono parser module."""

from typing import List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ParsedItem:
    type: str
    content: str
    parsed: Optional[List['ParsedItem']] = None

class OnoParser:
    def __init__(self):
        self.start_tag = '<?ono'
        self.end_tag = '?>'
    
    def parse(self, text: str) -> List[ParsedItem]:
        result = []
        current_index = 0
        
        while current_index < len(text):
            start_index = text.find(self.start_tag, current_index)
            
            if start_index == -1:
                if current_index < len(text):
                    result.append(ParsedItem(
                        type='text',
                        content=text[current_index:]
                    ))
                break
            
            if start_index > current_index:
                result.append(ParsedItem(
                    type='text',
                    content=text[current_index:start_index]
                ))
            
            end_index, content = self._find_matching_closing_tag(text, start_index)
            
            if end_index == -1:
                result.append(ParsedItem(
                    type='text',
                    content=text[start_index:]
                ))
                break
            
            inner_content = content.strip()
            parsed_inner = self.parse(inner_content)
            
            result.append(ParsedItem(
                type='ono',
                content=inner_content,
                parsed=parsed_inner
            ))
            
            current_index = end_index + len(self.end_tag)
        
        return result
    
    def _find_matching_closing_tag(self, text: str, start_index: int) -> Tuple[int, str]:
        depth = 0
        current_index = start_index + len(self.start_tag)
        
        while current_index < len(text):
            next_start = text.find(self.start_tag, current_index)
            next_end = text.find(self.end_tag, current_index)
            
            if next_end == -1:
                return -1, ''
            
            if next_start != -1 and next_start < next_end:
                depth += 1
                current_index = next_start + len(self.start_tag)
            else:
                if depth == 0:
                    content_start = start_index + len(self.start_tag)
                    content = text[content_start:next_end]
                    return next_end, content
                else:
                    depth -= 1
                    current_index = next_end + len(self.end_tag)
        
        return -1, ''
    
    def extract_ono_blocks(self, parsed_content: List[ParsedItem]) -> List[str]:
        ono_blocks = []
        
        def extract_recursive(items: List[ParsedItem]):
            for item in items:
                if item.type == 'ono':
                    ono_blocks.append(item.content)
                    if item.parsed:
                        extract_recursive(item.parsed)
        
        extract_recursive(parsed_content)
        return ono_blocks
    
    def render(self, parsed_content: List[ParsedItem]) -> str:
        result = []
        for item in parsed_content:
            if item.type == 'text':
                result.append(item.content)
            elif item.type == 'ono':
                result.append(f'<?ono {item.content} ?>')
        return ''.join(result)
