# Ono - Universal AI-Powered Preprocessor

*"Oh no, this is complicated... let AI figure it out."*

Ono is a universal templating preprocessor that uses AI to solve those annoying cross-platform, language-specific problems you don't want to think about. Write once, deploy anywhere, in any language.

## Why Ono?

Ever written a script that needs to find the user's temp directory? Congratulations, you just signed up for:
- Environment variables (`$TMPDIR`, `$TMP`, `$TEMP`)
- Platform differences (Windows vs macOS vs Linux)
- XDG standards and appdirs conventions
- Edge cases you never thought of

With Ono, you just write:

```bash
#!/bin/bash
tmp=<?ono get users temp directory ?>
touch $tmp/myfile
```

Run `ono --format bash script.sh.ono > script.sh` and get:

```bash
#!/bin/bash
tmp="/tmp"
touch /tmp/myfile
```

The same template works for Python, JavaScript, Rust, SQL, Dockerfiles, or any text format.

## How It Works

Ono uses the familiar `<?ono ... ?>` syntax (inspired by PHP) that can be embedded in any file format. AI understands your intent and generates the right output for your target language and platform.

## Basic Usage

**Simple inline requests:**
```python
# Python
temp_dir = <?ono get users temp directory ?>
config_dir = <?ono get users config directory ?>
username = <?ono get current username ?>
```

**Block syntax with configuration:**
```bash
#!/bin/bash
temp=<?ono 
model="claude-3-5-sonnet"
temperature=0.1

get users temp directory, ensuring it follows XDG standards on Linux
?>
```

## Configuration Syntax

Ono supports two types of parameters:

- **Pass-through parameters** (sent directly to the LLM): `model="gpt-4"`, `temperature=0.2`
- **Ono-specific parameters** (prefixed with `@`): `@context="preserve"`, `@execution="once"`

```bash
result=<?ono 
@context="preserve_previous"
@execution="once"
model="claude-3-5-sonnet"
temperature=0.1

determine the best package manager for this system
?>
```

## Cross-Platform & Multi-Language

The same Ono template works across languages and platforms:

**Template file (deploy.ono):**
```
# Get platform-appropriate paths
TEMP_DIR=<?ono get users temp directory ?>
CONFIG_DIR=<?ono get users config directory ?>
CURRENT_USER=<?ono get current username ?>
```

**Generate for different formats:**
```bash
ono --format bash deploy.ono > deploy.sh
ono --format powershell deploy.ono > deploy.ps1  
ono --format python deploy.ono > deploy.py
```

## Context Management

Ono includes context management for complex workflows:

```bash
# Establish context
analysis=<?ono 
@context="new"
analyze this codebase structure
?>

# Build on previous context  
tests=<?ono 
@context="preserve_previous"
generate unit tests based on the analysis above
?>
```

## Build Metadata

Ono tracks build information to enable reproducible builds:

```bash
#!/bin/bash
# ONO_BUILD_INFO_START
# build_id: 20250529-143022-abc123
# timestamp: 2025-05-29T14:30:22Z  
# ono_version: 1.2.3
# source: deploy.sh.ono
# ONO_BUILD_INFO_END

tmp="/tmp"
apt install mypackage
```

For structured data formats:

```json
{
  "@n@": {
    "build_id": "abc123",
    "source": "config.json.ono"
  },
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

Control metadata placement:

```bash
ono --format bash --meta inline deploy.sh.ono    # Inline comments (default)
ono --format json --meta file config.json.ono    # Separate .ono-meta file  
ono --format json --meta none config.json.ono    # No metadata
```

## Installation & Setup

```bash
pip install ono-preprocessor
```

Ono works with any OpenAI-compatible API endpoint:

```bash
export ONO_API_URL="http://localhost:8000/v1"  # vLLM
# or export ONO_API_URL="https://api.openai.com/v1"  # OpenAI
```

For a quick test without installation:

```bash
# Try it instantly with our demo server
cat yourfile.ono | nc demo.onolang.com 8080
```

## Examples

**Cross-platform script:**
```bash
#!/bin/bash
# Works on Windows, macOS, and Linux
PYTHON_EXEC=<?ono find python executable path ?>
VENV_DIR=<?ono get appropriate virtual environment directory ?>
$PYTHON_EXEC -m venv $VENV_DIR
```

**Docker with smart defaults:**
```dockerfile
FROM ubuntu:22.04
WORKDIR <?ono get appropriate working directory for containerized apps ?>
COPY requirements.txt .
RUN <?ono generate appropriate pip install command with security best practices ?>
```

**Configuration files:**
```yaml
# config.yaml.ono
database:
  host: <?ono get database host from environment or default to localhost ?>
  port: <?ono get appropriate database port for postgresql ?>
  ssl_mode: <?ono determine ssl requirements based on environment ?>
```

## Why "Ono"?

The name comes from PHP with the straight lines removed: **p**hp → **o**no. Just like how ono takes PHP's templating concept and makes it more fluid for the AI age.

Plus, it captures that "oh no, this is complicated" moment when you realize you need AI to figure it out instead of spending 30 minutes on Stack Overflow.

## License

MIT

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
