# TCP Ono - AI-Powered Template Processor

An AI-powered templating system that runs over TCP, allowing you to send Ono blocks and receive generated code.

## Quick Start

```bash
cd examples/tcp_server

# Install dependencies
pip install -r requirements.txt

# Start the server (auto-detects models and starts)
bash start_ono.sh

# In another terminal, send queries
echo '[?ono find process on port 8080?]' | nc localhost 8080
echo '[?ono get current time?]' | nc localhost 8080
```

## What is TCP Ono?

TCP Ono allows you to embed AI-powered code generation in your scripts using `<?ono ... ?>` or `[?ono ... ?]` blocks. The server processes these blocks using a local LLM and returns executable code.

## Supported Formats

The TCP server accepts multiple Ono block formats:

```
[?ono your query here?]
<?ono your query here?>
"?ono your query here"?
'?ono your query here'?
```

## Example Queries

```bash
echo '[?ono find process on port 8080?]' | nc localhost 8080
# Output: lsof -ti:8080

echo '[?ono get current date?]' | nc localhost 8080  
# Output: date +%Y-%m-%d

echo '[?ono list all running processes?]' | nc localhost 8080
# Output: ps aux
```

## Setup

The `start_ono.sh` script will:

1. Detect available LLM backends (ollama, sglang, llama.cpp, vllm)
2. Check for installed models
3. Download `Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF` if no models found
4. Start the TCP server on port 8080

## Files

- `ono_tcp.py` - TCP server implementation
- `ono_skill.py` - Model detection and setup helper
- `start_ono.sh` - Full setup and start script
- `model_detect.sh` - Model detection only
- `tcp_server.sh` - Start server only
- `requirements.txt` - Python dependencies

## Dependencies

- Python 3.8+
- httpx
- typer
- Ollama (or other LLM backend)

## Architecture

```
Client (nc) --> TCP Server (ono_tcp.py) --> Parser --> LLM (Ollama) --> Response
```

## Generated With

This TCP server was generated using Ono's AI-powered templating system.

## License

MIT
