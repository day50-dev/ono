# Ono Language Specification v0.1

## 1. Introduction

Ono is a universal AI-powered templating language designed to embed intelligent content generation within any text-based file format. The language uses natural language requests to generate contextually appropriate content while maintaining syntactic validity in the host language.

## 2. Design Principles

1. **Universal Compatibility**: Ono blocks can be embedded in any text format
2. **Syntactic Preservation**: Host files remain syntactically valid during editing
3. **Contextual Intelligence**: AI understands both the request and surrounding context
4. **Minimal Syntax**: Simple, readable syntax with flexible delimiters
5. **Reproducible Builds**: Complete metadata tracking for debugging and reproduction

## 3. Basic Syntax

### 3.1 Ono Blocks

An Ono block consists of:
- Optional opening delimiter
- The keyword `?ono`
- Natural language content
- Closing delimiter matching the opening delimiter + `?`

**Basic Pattern:**
```
[delimiter]?ono <content> ?[delimiter]
```

### 3.2 Default Delimiters

The following delimiters are automatically recognized:

| Opening | Closing | Example |
|---------|---------|---------|
| `"` | `?"` | `"?ono get temp directory ?"` |
| `'` | `?'` | `'?ono get username ?'` |
| `{` | `?}` | `{?ono get api key ?}` |
| `[` | `?]` | `[?ono get project name ?]` |
| `<` | `?>` | `<?ono get database host ?>` |
| (none) | `?` | `?ono get current time ?` |

### 3.3 Examples

```python
# Python example
database_url = "?ono get database connection string ?"
port = "?ono get default database port for postgresql ?"
```

```bash
# Bash example
temp_dir="?ono get users temp directory ?"
current_user=?ono get current username ?
```

```json
{
  "host": "?ono get database host from environment ?",
  "timeout": "?ono calculate appropriate timeout for this service ?"
}
```

## 4. Variable Substitution

### 4.1 Substitution Syntax

Ono supports intelligent variable substitution within ono blocks using universal syntax that translates to target language conventions:

**Variable Access:**
```
$variable_name
```

**Function Calls:**
```
$function_name($arg1, $arg2)
```

**Expression Evaluation:**
```
$(expression)
```

### 4.2 Substitution Examples

**Universal Template:**
```bash
result="?ono process data from $input_file using $processor_func($config_param) with timeout $(base_timeout + 10) ?"
```

**Bash Output:**
```bash
result=$(process_data "$input_file" "$(processor_func "$config_param")" "$((base_timeout + 10))")
```

**Python Output:**
```python
result = process_data(input_file, processor_func(config_param), base_timeout + 10)
```

**JavaScript Output:**
```javascript
result = processData(inputFile, processorFunc(configParam), baseTimeout + 10);
```

### 4.3 Parsing Rules

The substitution parser uses a stack-based approach:

- `$identifier` → Variable substitution
- `$identifier(` → Function call (parser pushes stack for arguments)
- `$(` → Expression stanza (parser pushes stack for expression evaluation)
- `)` → Pop parser stack

**Complex Example:**
```
"?ono create backup using $backup_tool($source_dir, $dest_calc($base_path, $project_name), $(retention_days * 24)) ?"
```

Parsed as:
- `$backup_tool` → function call with three arguments:
  - `$source_dir` → variable
  - `$dest_calc($base_path, $project_name)` → nested function call
  - `$(retention_days * 24)` → expression evaluation

### 4.1 Block-Level Configuration

Configuration parameters can be included within Ono blocks using key=value syntax:

```
"?ono 
model=claude-3-5-sonnet
temperature=0.2
@context=preserve_previous

get database configuration for production environment
?"
```

## 5. Configuration Syntax

**Pass-through Parameters** (sent directly to LLM):
- `model=<string>` - LLM model to use
- `temperature=<float>` - Response randomness (0.0-2.0)
- `max_tokens=<integer>` - Maximum response length
- Any other parameter supported by the LLM API

**Ono-Specific Parameters** (prefixed with `@`):
- `@context=<string>` - Context management directive  
- `@execution=<string>` - Execution control directive
- `@meta=<string>` - Metadata handling directive
- `@type=<string>` - Block type (model, agent, meta, source)

### 5.3 File-Level Configuration

Global settings for a file can be specified in comments at the top:

```python
#!/usr/bin/env python
# @ono.delimiters = 🐊, 🦋
# @ono.model = gpt-4
# @ono.context = deployment
# @ono.execution = once

database_url = 🐊?ono get database connection 🦋
```

**Supported File-Level Directives:**
- `@ono.delimiters = <open>, <close>` - Custom delimiter pair
- `@ono.model = <string>` - Default model for all blocks
- `@ono.context = <string>` - Default context path
- `@ono.execution = <string>` - Default execution mode
- `@ono.temperature = <float>` - Default temperature
- `@ono.meta = <string>` - Default metadata style

## 6. Context Management

### 6.1 Context Directives

| Directive | Behavior |
|-----------|----------|
| (no context specified) | Create fresh context for each block |
| `context=<name>` | Create or use named context |
| `context=<name>/<path>` | Create context branch (fork from parent) |

### 6.2 Context Examples

```bash
# Creates new context (default - no context specified)
system_info="?ono analyze this server environment ?"

# Creates "system" context, inherits from previous if available
services="?ono context=system identify running services on this system ?"

# Forks "system" context to create "system/monitoring" 
monitoring="?ono context=system/monitoring setup monitoring for the identified services ?"

# Another fork: "system/backup"
backup="?ono context=system/backup design backup strategy for critical services ?"
```

## 7. Execution Control

### 6.1 Execution Directives

| Directive | Behavior |
|-----------|----------|
| `@execution=always` | Execute every time (default) |
| `@execution=once` | Execute once, cache result |
| `@execution=compile` | Execute during preprocessing |
| `@execution=runtime` | Execute when target code runs |

### 6.2 Scope Directives

| Directive | Behavior |
|-----------|----------|
| `@scope=local` | Scoped to current file (default) |
| `@scope=global` | Shared across all files in project |
| `@scope=instance` | Separate execution per instance |

## 8. File Naming Convention

Ono template files use the `.ono.<extension>` naming pattern:

```
deploy.ono.sh       # Bash script template
config.ono.json     # JSON configuration template  
app.ono.py          # Python application template
Dockerfile.ono      # Dockerfile template
```

**Benefits:**
- Syntax highlighting for base language
- Clear identification of template files
- Tool integration (build systems, IDEs)

## 9. Processing Model

### 8.1 Two-Pass Processing

Ono uses a two-pass processing model:

**Pass 1: Concept Pass**
- Analyzes full file context
- Sends natural language request to LLM
- Generates semantically appropriate response
- Determines complexity level and extraction needs

**Pass 2: Syntax Pass**
- Applies target format requirements
- Handles escaping and quoting
- Extracts complex logic using function lifting
- Validates syntax when possible
- Ensures output compatibility

### 8.2 Function Lifting

When ono blocks require complex logic (loops, assignments, side effects), the solution is automatically extracted into helper functions using a preference hierarchy:

**Preference Hierarchy:**
1. **Simple substitution** - Direct string/value replacement
2. **Inline expression** - Single expression that fits naturally
3. **Nested function** - Extract complexity, keep local scope
4. **Adjacent function** - Same file, broader scope  
5. **External library** - Separate file for reusability
6. **Global function** - Last resort

**Naming Convention:**
Generated functions and variables use preprocessor-style naming:
- `_ono_fn_*` - Functions (e.g., `_ono_fn_get_backup_dir`)
- `_ono_var_*` - Variables (e.g., `_ono_var_platform_type`)
- `_ono_cls_*` - Classes (e.g., `_ono_cls_config_manager`)
- `_ono_const_*` - Constants (e.g., `_ono_const_timeout`)

**Example:**
```python
# Original ono block
backup_strategy = "?ono determine backup strategy based on platform with error handling ?"

# Generated output with function lifting
def _ono_fn_determine_backup_strategy():
    import platform
    import os
    
    system = platform.system().lower()
    if system == "windows":
        # Complex Windows backup logic
        drives = [d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(d + ":")]
        return f"robocopy /MIR source {drives[0]}:/backup"
    elif system == "darwin":
        return "rsync -av --delete source/ ~/backup/"
    else:
        return "tar -czf /tmp/backup.tar.gz source/"

backup_strategy = _ono_fn_determine_backup_strategy()
```

### 8.3 Processing Flow

```
Source File (.ono.ext) → Parser → Concept Pass → Complexity Analysis → Syntax Pass → Output File (.ext)
                             ↓           ↓              ↓              ↓
                        Context Mgr → LLM API → Function Lifting → Validator
```

## 10. Build Metadata

### 9.1 Metadata Formats

**Inline Comments** (default for comment-supporting languages):
```bash
#!/bin/bash
# ONO_BUILD_INFO_START
# build_id: 20250129-143022-abc123
# timestamp: 2025-01-29T14:30:22Z
# ono_version: 0.1.0
# source: deploy.ono.sh
# blocks: [{id: 1, resolved: "/tmp", model: "claude-3-5-sonnet"}]
# ONO_BUILD_INFO_END

temp_dir="/tmp"
```

**Structured Field** (for JSON/YAML/TOML):
```json
{
  "@ono": {
    "build_id": "abc123",
    "timestamp": "2025-01-29T14:30:22Z",
    "source": "config.ono.json",
    "ono_version": "0.1.0"
  },
  "database": {
    "host": "localhost"
  }
}
```

**Separate File** (when inline not possible):
```
config.json      # Generated output
config.json.ono-meta  # Metadata file
```

### 9.2 Metadata Control

Metadata generation can be controlled via CLI flags:

```bash
ono --meta inline source.ono.py    # Inline comments (default)
ono --meta file source.ono.json    # Separate .ono-meta file
ono --meta none source.ono.sh      # No metadata
```

## 11. Command Line Interface

### 10.1 Basic Processing

```bash
# Process single file
ono source.ono.py > output.py
ono --format python source.ono.py > output.py

# Process with options
ono --meta file --context new source.ono.json > output.json

# Include source debugging information
ono -g source.ono.py > output.py
```

### 10.2 Context Management

```bash
# List contexts
ono contexts list

# Clean old contexts  
ono contexts clean

# Show context details
ono contexts show preserve_previous/analysis
```

### 10.3 Information Commands

```bash
# Show build metadata
ono info output.py

# Validate without processing
ono validate source.ono.py

# Show version
ono --version
```

## 12. Configuration

### 11.1 Global Configuration

File: `~/.ono/config.yaml`

```yaml
llm:
  api_url: "http://localhost:8000/v1"
  api_key: "${ONO_API_KEY}"
  default_model: "claude-3-5-sonnet"
  timeout: 30

defaults:
  meta_style: "inline"
  context_storage: "~/.ono/contexts"
  execution: "always"

formats:
  bash:
    validator: "shellcheck"
  python: 
    validator: "python -m py_compile"
  json:
    validator: "jq ."
```

### 11.2 Project Configuration

File: `.ono/config.yaml`

```yaml
# Project-specific overrides
llm:
  default_model: "gpt-4"
  
context:
  default_path: "main"
  auto_cleanup: false

formats:
  dockerfile:
    validator: "hadolint"
```

## 13. Error Handling

### 12.1 Parse Errors

- **Unmatched delimiters**: Clear error with line number and suggestion
- **Invalid configuration**: Show valid parameter options
- **Malformed blocks**: Highlight problematic syntax

### 12.2 Processing Errors  

- **LLM API failures**: Retry with exponential backoff
- **Context errors**: Auto-create missing contexts with warnings
- **Validation failures**: Show validator output with suggestions

### 12.3 Error Examples

```
Error: Unmatched delimiter on line 15
  Found: "ono get temp dir ?'
  Expected: "ono get temp dir ?"

Error: Invalid context path 'invalid/path'
  Valid formats:
    - new
    - preserve_previous  
    - preserve_previous/branch_name

Warning: Context 'preserve_previous/analysis' not found
  Created new context branch
```

## 14. Language Integration

### 13.1 Supported Output Formats

- **Shell scripts**: bash, zsh, fish
- **Programming languages**: Python, JavaScript, Go, Rust, Java
- **Configuration**: JSON, YAML, TOML, INI
- **Infrastructure**: Dockerfile, Terraform, Kubernetes YAML
- **Documentation**: Markdown, RST, plain text

### 13.2 Format-Specific Features

**Shell Scripts:**
- Automatic quoting and escaping
- Environment variable handling
- Cross-platform path resolution

**Python:**
- String literal generation
- Import statement optimization  
- Type hint preservation

**JSON/YAML:**
- Schema validation when available
- Proper data type conversion
- Comment preservation (where supported)

## 15. Security Considerations

### 14.1 Input Validation

- Sanitize Ono block content
- Validate configuration parameters
- Prevent injection attacks in generated code

### 14.2 Output Safety

- Format-specific escaping
- Validation with external tools
- Warning for potentially unsafe operations

### 14.3 API Security

- Secure API key storage
- Request rate limiting
- Connection encryption

## 16. Future Extensions

### 15.1 Planned Features

- Plugin system for custom validators
- Template marketplace integration
- IDE/editor extensions
- CI/CD pipeline integration

### 15.2 Compatibility

This specification defines Ono Language v0.1. Future versions will maintain backward compatibility for:
- Basic syntax and delimiters
- Core configuration parameters  
- File naming conventions
- Metadata formats

---

**Specification Version**: 0.1  
**Date**: May 30, 2025  
**Status**: Draft