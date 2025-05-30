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

Ono uses the familiar `<?ono ... ?>` syntax (inspired by PHP) that can be embedded in any file format. The AI understands your intent and generates the right output for your target language and platform.

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
@context="preserve_previous/analysis"
@execution="once"
@scope="global"
model="claude-3-5-sonnet"
temperature=0.1
system="You are an expert system administrator"

determine the best package manager for this system
?>
```

## Context Management

Ono includes powerful context management for complex workflows:

**Basic context preservation:**
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

**Context branching with paths:**
```bash
# Establish baseline
<?ono 
@context="preserve_previous/setup"
analyze this API design
?>

# Fork for different tasks
<?ono 
@context="preserve_previous/setup/testing"
create comprehensive test suite
?>

<?ono 
@context="preserve_previous/setup/docs"  
write API documentation
?>

# Continue testing branch
<?ono 
@context="preserve_previous/setup/testing"
add performance benchmarks
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

## Execution Modes

ono automatically detects whether your request needs agent capabilities or just model completion:

**Agent mode** (system inspection, file access, tool calling):
```bash
platform=<?ono 
detect the operating system and check what package managers are installed
?>
```

**Model mode** (pure text generation using established context):
```bash
install_cmd=<?ono 
@context="preserve_previous"
generate the appropriate install command using the detected package manager
?>
```

You can also force a specific mode:
```bash
<?ono 
@mode="agent"
inspect the current directory structure
?>

<?ono 
@mode="model"
@context="preserve_previous" 
create a README based on the directory structure above
?>
```

## Context-Aware Cross-Compilation

For production deployments, ono supports two-phase execution:

**Phase 1: Analyze context requirements**
```bash
ono --analyze deploy.sh.ono > context.yaml
```

**Phase 2: Generate with specific context**  
```bash
# Local development
ono --format bash --context auto deploy.sh.ono > deploy.sh

# Production deployment  
ono --format bash --context prod-context.yaml deploy.sh.ono > deploy-prod.sh
```

Where `prod-context.yaml` specifies the target environment:
```yaml
username: "appuser" 
operating_system: "ubuntu-22.04"
temp_directory: "/var/tmp"
package_manager: "apt"
python_executable_path: "/usr/bin/python3.11"
```

This enables true "cross-compilation" - generate scripts for environments you don't have direct access to.

## Installation & Setup

```bash
pip install ono-preprocessor
ono init
```

The setup wizard will ask you to choose an AI agent backend:

```
Welcome to ono! 

Which agent would you like to use?
1. Aider (recommended for code tasks) [default]
2. Open Interpreter (general system tasks) 
3. LangChain (enterprise/custom workflows)
4. CrewAI (multi-agent workflows)

Choice [1]: 
```

ono will automatically install and configure your chosen agent. That's it - you're ready to go!

## Agent Backend

ono works by sending requests to AI agents that handle the complexity of model selection, tool calling, and system interaction. The agent manages:
- LLM connections and API keys
- Model routing and fallbacks  
- Tool calling and system access
- Security and sandboxing

You don't need to configure LLM backends directly - your chosen agent handles all of that.

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

The name comes from PHP with the straight lines removed: php → ono. Just like how Ono takes PHP's templating concept and makes it more fluid for the AI age.

Plus, it captures that "oh no, this is complicated" moment when you realize you need AI to figure it out instead of spending 30 minutes on Stack Overflow.

## License

MIT

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
