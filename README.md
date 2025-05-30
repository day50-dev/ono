# Ono - Universal AI-Powered Preprocessor

*"Oh no, this is complicated... let AI figure it out."*

Ono is a universal templating preprocessor that uses AI to solve those annoying cross-platform, language-specific problems you don't want to think about. Write once, deploy anywhere, in any language.

## Why Ono?

Ever written a script that needs to find the user's temp directory? Congratulations, you just signed up for:
- Environment variables (`$TMPDIR`, `$TMP`, `$TEMP`)
- Platform differences (Windows vs macOS vs Linux)  
- XDG standards and appdirs conventions
- Edge cases you never thought of

With Ono:

```bash
#!/bin/bash
tmp="?ono get users temp directory ?"
python_exec="?ono find python executable path ?"
config_dir="?ono get users config directory ?"

echo "Using Python: $python_exec"
echo "Config at: $config_dir"
echo "Temp files: $tmp"
```

Run `ono deploy.ono.sh > deploy.sh` and get perfect cross-platform code that just works.

## Glamorous Examples

**Smart Configuration:**
```json
{
  "database": {
    "host": "?ono get database host from environment or default to localhost ?",
    "port": "?ono get appropriate database port for postgresql ?",
    "ssl_mode": "?ono determine ssl requirements based on environment ?"
  },
  "cache": {
    "dir": "?ono get platform appropriate cache directory ?",
    "size": "?ono calculate optimal cache size for this system ?"
  }
}
```

**Intelligent Docker:**
```dockerfile  
FROM ubuntu:22.04
WORKDIR "?ono get appropriate working directory for containerized python apps ?"

# Smart package installation
RUN "?ono generate apt install command with security best practices for python development ?"

# Platform-aware Python setup
ENV PYTHON_PATH="?ono get optimal python path for containers ?"
COPY requirements.txt .
RUN "?ono generate pip install command with caching and security flags ?"
```

**Cross-Platform Scripts:**
```python
#!/usr/bin/env python3
import os

# Works everywhere
temp_dir = "?ono get users temp directory ?"
home_dir = "?ono get users home directory ?"
app_data = "?ono get appropriate application data directory ?"

# Smart defaults
database_url = "?ono construct database url with proper escaping and defaults ?"
api_timeout = "?ono calculate appropriate timeout for api calls based on environment ?"

# Platform-aware logic
backup_cmd = "?ono generate cross-platform backup command with error handling ?"
```

## How It Works

Ono uses flexible `"?ono ... ?"` syntax that works in any file format. The AI understands your intent, analyzes the surrounding context, and generates the right solution for your target platform.

**Simple requests** become direct substitutions:
```bash
user="?ono get current username ?"
# → user="john"
```

**Complex requests** get lifted into smart functions:
```python
backup_strategy = "?ono create robust backup system with retry logic ?"
# → Generates full function with error handling, platform detection, etc.
```

## Quick Start

```bash
# Install
pip install ono-preprocessor

# Set your LLM endpoint  
export ONO_API_URL="http://localhost:8000/v1"

# Process templates
ono deploy.ono.sh > deploy.sh
ono config.ono.json > config.json
ono app.ono.py > app.py

# Try it instantly (no install)
echo 'temp="?ono get temp directory ?"' | nc demo.onolang.com 8080
```

## Context Magic

Build sophisticated workflows with context management:

```python
# Establish analysis context
architecture = "?ono 
@context=preserve_previous/analysis
analyze this microservices codebase and identify key components
?"

# Branch for different tasks
tests = "?ono 
@context=preserve_previous/analysis/testing
generate comprehensive integration tests for the services above
?"

docs = "?ono 
@context=preserve_previous/analysis/docs  
write API documentation for the analyzed services
?"
```

## File Convention

Use `.ono.ext` naming to keep syntax highlighting and tool compatibility:

```
deploy.ono.sh       # → deploy.sh
config.ono.json     # → config.json  
app.ono.py          # → app.py
Dockerfile.ono      # → Dockerfile
```

## Smart Metadata

Every generated file includes build info for reproducibility:

```bash
#!/bin/bash
# ?ono
# type=meta
# build_id=20250530-143022-abc123
# source=deploy.ono.sh
# ono_version=0.1.0
# ?

temp_dir="/tmp"
```

## Why "Ono"?

The name comes from **p**hp → **o**no (removing the straight lines). Just like how ono takes PHP's templating concept and makes it fluid for the AI age.

Plus, it captures that "oh no, this is complicated" moment when you realize you need AI to figure it out instead of spending 30 minutes on Stack Overflow.

## What's Next?

- Template marketplace integration
- IDE extensions for `.ono.*` files  
- CI/CD pipeline templates
- Advanced context sharing

---

**License:** MIT  
**Docs:** [onolang.com](https://onolang.com)  
**Demo:** `nc demo.onolang.com 8080`
