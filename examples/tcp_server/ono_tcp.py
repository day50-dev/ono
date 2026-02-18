#!/usr/bin/env python3
"""TCP server for Ono - AI-powered templating language processor."""

import socket
import sys
import os
import re

# Get the ono module path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# This is: /home/chris/day50/ono/examples/tcp_server
# We need to go up 2 levels to get to /home/chris/day50/ono
ono_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if ono_root not in sys.path:
    sys.path.insert(0, ono_root)

try:
    from ono.parser import OnoParser
    from ono.llm import LLMClient
    from ono.processor import Processor
except ImportError as e:
    print(f"Error: Could not import ono modules: {e}")
    print(f"Looking for ono in: {ono_root}")
    sys.exit(1)


def normalize_ono_format(text: str) -> str:
    """Normalize ono blocks to <?ono ... ?> format."""
    text = text.replace('[?ono ', '<?ono ').replace(' ?]', ' ?>').replace('?]', ' ?>')
    text = text.replace('"?ono ', '<?ono ').replace(' "?', ' ?>').replace('"?', ' ?>')
    text = text.replace("'?ono ", '<?ono ').replace(" ?'", ' ?>').replace("?'", ' ?>')
    return text


def process_request(request: str) -> str:
    """Process an Ono request and return the result."""
    request = normalize_ono_format(request)
    
    parser = OnoParser()
    parsed = parser.parse(request)
    blocks = parser.extract_ono_blocks(parsed)
    
    if not blocks:
        return request
    
    try:
        llm = LLMClient("http://localhost:11434/v1", "Qwen3-Coder-Next-Q4_K_M.gguf")
        processor = Processor(llm)
        
        resolved_blocks = []
        for block in blocks:
            resolved = processor.process(block, format_hint='bash')
            resolved_blocks.append(resolved)
        
        result = []
        block_index = 0
        for item in parsed:
            if item.type == 'text':
                result.append(item.content)
            elif item.type == 'ono':
                if block_index < len(resolved_blocks):
                    result.append(resolved_blocks[block_index])
                    block_index += 1
                else:
                    result.append(f'<?ono {item.content} ?>')
        
        return ''.join(result)
    except Exception as e:
        return f"# LLM error: {str(e)}\n# Try: bash start_ono.sh to set up the server"


def handle_client(client_socket: socket.socket, address: tuple):
    """Handle a single client connection."""
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            
            request = data.decode('utf-8').strip()
            
            if request.lower() in ('exit', 'quit', 'q'):
                client_socket.send(b'Goodbye!\n')
                break
            
            result = process_request(request)
            client_socket.send((result + '\n').encode('utf-8'))
            
    except Exception as e:
        client_socket.send(f'Error: {str(e)}\n'.encode('utf-8'))
    finally:
        client_socket.close()


def main():
    """Start the TCP server."""
    host = '0.0.0.0'
    port = 8080
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f'Ono TCP server listening on {host}:{port}')
        print('Send Ono blocks like: [?ono find process on port 8080?] or exit')
        
        while True:
            client_socket, address = server.accept()
            print(f'Connection from {address[0]}:{address[1]}')
            handle_client(client_socket, address)
            
    except KeyboardInterrupt:
        print('\nShutting down server...')
    finally:
        server.close()


if __name__ == '__main__':
    main()
