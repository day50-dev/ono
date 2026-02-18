#!/bin/bash
# TCP Server for Ono - AI-powered templating language processor

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if ono_tcp.py exists
if [ ! -f "$SCRIPT_DIR/ono_tcp.py" ]; then
    echo "Error: ono_tcp.py not found at $SCRIPT_DIR/ono_tcp.py"
    exit 1
fi

echo "Starting TCP Ono server on port 8080..."
echo "Send queries like: echo '[?ono your query?]' | nc localhost 8080"
python3 "$SCRIPT_DIR/ono_tcp.py"
