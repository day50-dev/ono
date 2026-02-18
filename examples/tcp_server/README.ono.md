# TCP Ono - AI-Powered Template Processor

## Quick Start

Start the TCP server:

```bash
<?ono find a way to start the TCP server on port 8080 and return the command ?>
```

Then send queries:

```bash
echo '[?ono find process on port 8080?]' | nc localhost 8080
echo '[?ono get current date in format YYYY-MM-DD?]' | nc localhost 8080
```

## What is TCP Ono?

TCP Ono is an AI-powered templating system that runs over TCP. You send `<?ono ... ?>` blocks and get back generated code.

## Setup

The setup process will:
1. Detect available LLM backends (ollama/sglang/llama.cpp/vllm)
2. Check for models
3. Download `Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF` if needed
4. Start the TCP server

## Files

- `tcp_server.ono.sh` - TCP server script
- `model_detect.ono.sh` - Model detection script
- `start_ono.ono.sh` - Full setup script

## Example Queries

```
[?ono find and safely terminate process on port 8080?]
[?ono list all running processes with memory usage?]
[?ono get system uptime?]
```
