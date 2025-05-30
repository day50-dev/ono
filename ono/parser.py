from typing import List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ParsedItem:
    """
    Represents a parsed item, which can be either text or an Ono block.
    """
    type: str  # 'text' or 'ono'
    content: str
    parsed: Optional[List['ParsedItem']] = None

class OnoParser:
    """
    Parses text and extracts Ono blocks.
    Handles nested Ono blocks correctly.
    """
    def __init__(self):
        """
        Initializes the OnoParser with the start and end tags for Ono blocks.
        """
        self.start_tag = '<?ono'
        self.end_tag = '?>'
    
    def parse(self, text: str) -> List[ParsedItem]:
        """
        Parses the given text and returns a list of ParsedItem objects.
        """
        result = []
        current_index = 0
        
        while current_index < len(text):
            start_index = text.find(self.start_tag, current_index)
            
            if start_index == -1:
                # No more Ono tags, add remaining text
                if current_index < len(text):
                    result.append(ParsedItem(
                        type='text',
                        content=text[current_index:]
                    ))
                break
            
            # Add text before the tag
            if start_index > current_index:
                result.append(ParsedItem(
                    type='text',
                    content=text[current_index:start_index]
                ))
            
            # Find the matching closing tag with proper nesting
            end_index, content = self._find_matching_closing_tag(text, start_index)
            
            if end_index == -1:
                # Malformed - no matching closing tag
                result.append(ParsedItem(
                    type='text',
                    content=text[start_index:]
                ))
                break
            
            # Parse the content inside the tags recursively
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
        """
        Finds the matching closing tag, handling nested tags properly.
        Returns the index of the closing tag and the content within the tags.
        """
        depth = 0
        current_index = start_index
        
        while current_index < len(text):
            next_start = text.find(self.start_tag, current_index)
            next_end = text.find(self.end_tag, current_index)
            
            if next_end == -1:
                # No closing tag found
                return -1, ''
            
            if next_start != -1 and next_start < next_end:
                # Found another opening tag before the next closing tag
                depth += 1
                current_index = next_start + len(self.start_tag)
            else:
                # Found a closing tag
                if depth == 0:
                    # This is our matching closing tag
                    content_start = start_index + len(self.start_tag)
                    content = text[content_start:next_end]
                    return next_end, content
                else:
                    # This closing tag belongs to a nested opening tag
                    depth -= 1
                    current_index = next_end + len(self.end_tag)
        
        return -1, ''
    
    def extract_ono_blocks(self, parsed_content: List[ParsedItem]) -> List[str]:
        """
        Extracts all Ono content blocks, including nested ones.
        """
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
        """
        Renders the parsed content back into a string.
        """
        result = []
        for item in parsed_content:
            if item.type == 'text':
                result.append(item.content)
            elif item.type == 'ono':
                result.append(f'<?ono {item.content} ?>')
        return ''.join(result)