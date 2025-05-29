from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ParsedItem:
    type: str  # 'text' or 'ono'
    content: str
    parsed: Optional[List['ParsedItem']] = None

class OnoParser:
    def __init__(self):
        self.start_tag = '<?ono'
        self.end_tag = '?>'
    
    def parse(self, text: str) -> List[ParsedItem]:
        """Parse text and return list of ParsedItem objects."""
        result = []
        current_index = 0
        
        while current_index < len(text):
            start_index = text.find(self.start_tag, current_index)
            
            if start_index == -1:
                # No more ono tags, add remaining text
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
        """Find the matching closing tag, handling nested tags properly."""
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
        """Extract all ono content blocks, including nested ones."""
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
        """Render parsed content back to string."""
        result = []
        for item in parsed_content:
            if item.type == 'text':
                result.append(item.content)
            elif item.type == 'ono':
                result.append(f'<?ono {item.content} ?>')
        return ''.join(result)

# Example usage
if __name__ == '__main__':
    parser = OnoParser()
    
    # Test with your example
    test_text = """blah blah blah
blah <?ono capture this <?ono but also this ?> and keep going ?> blah blah"""
    
    print("Original text:")
    print(test_text)
    print("\nParsed result:")
    
    parsed = parser.parse(test_text)
    for i, item in enumerate(parsed):
        print(f"{i}: {item.type} - '{item.content[:50]}{'...' if len(item.content) > 50 else ''}'")
        if item.parsed:
            for j, sub_item in enumerate(item.parsed):
                print(f"  {j}: {sub_item.type} - '{sub_item.content}'")
    
    print("\nExtracted ono blocks:")
    ono_blocks = parser.extract_ono_blocks(parsed)
    for i, block in enumerate(ono_blocks):
        print(f"Block {i + 1}: '{block}'")
    
    # Test with more complex nesting
    print("\n" + "="*50)
    complex_text = "Start <?ono level1 <?ono level2a ?> middle <?ono level2b <?ono level3 ?> end2b ?> end1 ?> finish"
    print("Complex nesting test:")
    print(complex_text)
    
    complex_parsed = parser.parse(complex_text)
    complex_blocks = parser.extract_ono_blocks(complex_parsed)
    print("\nExtracted blocks:")
    for i, block in enumerate(complex_blocks):
        print(f"Block {i + 1}: '{block}'")
