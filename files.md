# Ono Project Structure & File Layout

## Repository Structure

```
ono/
├── README.md
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
│
├── ono/                          # Main package
│   ├── __init__.py
│   ├── __main__.py              # Entry point for `python -m ono`
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # Configuration management
│   ├── parser.py                # Parse <?ono ... ?> blocks
│   ├── processor.py             # Two-pass processing engine
│   ├── context.py               # Context management and routing
│   ├── llm.py                   # LLM API interface
│   ├── metadata.py              # Build metadata generation
│   ├── formatter.py             # Output formatting and escaping
│   ├── validator.py             # Format-specific validation
│   └── exceptions.py            # Custom exceptions
│
├── ono/templates/               # Built-in template helpers
│   ├── __init__.py
│   ├── common.py                # Common template functions
│   └── formatters/              # Format-specific helpers
│       ├── __init__.py
│       ├── bash.py
│       ├── python.py
│       ├── json.py
│       └── dockerfile.py
│
├── ono/demo/                    # Demo server (optional)
│   ├── __init__.py
│   ├── server.py                # TCP server for `nc` demo
│   └── sandbox.py               # Sandboxed execution
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── test_parser.py
│   ├── test_processor.py
│   ├── test_context.py
│   ├── test_llm.py
│   ├── test_metadata.py
│   ├── test_cli.py
│   ├── integration/             # Integration tests
│   │   ├── test_end_to_end.py
│   │   └── test_formats.py
│   └── fixtures/                # Test data
│       ├── templates/
│       └── expected_outputs/
│
├── examples/                    # Example templates
│   ├── basic/
│   │   ├── hello.ono.sh
│   │   ├── config.ono.json
│   │   └── deploy.ono.py
│   ├── advanced/
│   │   ├── multi_context.ono
│   │   └── cross_platform.ono
│   └── real_world/
│       ├── docker_setup.ono.dockerfile
│       ├── ci_pipeline.ono.yml
│       └── terraform.ono.tf
│
├── docs/                        # Documentation
│   ├── README.md
│   ├── installation.md
│   ├── syntax.md
│   ├── context_management.md
│   ├── configuration.md
│   └── api_reference.md
│
└── scripts/                     # Development scripts
    ├── build.sh
    ├── test.sh
    ├── lint.sh
    └── release.sh
```

## Core Module Purposes

### `ono/cli.py`
**Purpose**: Command-line interface and argument parsing
**Key Functions**:
- `main()` - Entry point
- `process_file()` - Main processing command
- `show_info()` - Display build metadata
- `manage_contexts()` - Context management commands

**Responsibilities**:
- Parse command line arguments
- Handle file I/O operations
- Progress reporting for long operations
- Error reporting and user feedback

### `ono/parser.py`
**Purpose**: Parse `<?ono ... ?>` blocks from source files
**Key Classes**:
- `OnoParser` - Main parsing engine
- `OnoBlock` - Represents parsed ono block
- `ParsedFile` - Complete file with blocks extracted

**Responsibilities**:
- Recursive parsing of nested blocks
- Configuration parameter extraction
- Syntax validation and error reporting
- Preserve file structure around blocks

### `ono/processor.py`
**Purpose**: Two-pass processing engine
**Key Classes**:
- `TwoPassProcessor` - Main processing orchestrator
- `ConceptPass` - Semantic understanding pass
- `SyntaxPass` - Format-specific syntax pass

**Responsibilities**:
- Coordinate two-pass processing
- Manage LLM interactions
- Handle context injection
- Process multiple blocks in sequence

### `ono/context.py`
**Purpose**: Context management and routing
**Key Classes**:
- `ContextManager` - Main context interface
- `Context` - Individual context storage
- `ContextPath` - Path parsing and navigation

**Responsibilities**:
- Context storage and retrieval
- Path-based routing (preserve_previous/path1)
- Context branching and forking
- Persistence across ono runs

### `ono/llm.py`
**Purpose**: LLM API interface and request handling
**Key Classes**:
- `LLMClient` - API client
- `LLMRequest` - Request formatting
- `LLMResponse` - Response parsing

**Responsibilities**:
- Abstract OpenAI-compatible APIs
- Transparent parameter passing
- Error handling and retries
- Rate limiting and timeout handling

### `ono/metadata.py`
**Purpose**: Build metadata generation and formatting
**Key Classes**:
- `BuildMetadata` - Metadata collection
- `MetadataFormatter` - Format-specific output
- `BlockExecution` - Per-block tracking

**Responsibilities**:
- Generate unique build IDs
- Track processing details
- Format metadata for different output types
- Handle @n@ field insertion

### `ono/formatter.py`
**Purpose**: Output formatting and language-specific escaping
**Key Classes**:
- `OutputFormatter` - Main formatting interface
- `LanguageFormatter` - Base class for language-specific formatters

**Responsibilities**:
- Language-specific escaping and quoting
- Template substitution
- Format validation preparation
- Clean output generation

### `ono/validator.py`
**Purpose**: Format-specific validation
**Key Classes**:
- `ValidatorRegistry` - Manage available validators
- `FormatValidator` - Base validator class

**Responsibilities**:
- Run format-specific validation tools
- Parse validation errors
- Suggest corrections
- Integration with external tools (shellcheck, etc.)

### `ono/config.py`
**Purpose**: Configuration management
**Key Classes**:
- `OnoConfig` - Main configuration object
- `ConfigLoader` - Load from files and environment

**Responsibilities**:
- Load global and project-specific config
- Environment variable handling
- Configuration validation
- Default value management

## Data Flow

### 1. File Processing Flow
```
Source File → Parser → Processor → Formatter → Output File
     ↓            ↓         ↓          ↓
  ParsedFile → OnoBlocks → Results → Formatted
                    ↓
              Context Manager
                    ↓
                LLM Client
```

### 2. Configuration Loading
```
CLI Args → Config Loader → Merged Config
    ↓           ↓              ↓
Environment → Project Config → Global Config
Variables      (.ono/config)   (~/.ono/config)
```

### 3. Context Resolution
```
@context="path" → ContextPath → ContextManager → Context Storage
                      ↓              ↓              ↓
                 Path Parser → Context Lookup → File/Memory
```

## File Formats & Storage

### Context Storage (`~/.ono/contexts/`)
```
~/.ono/
├── config.yaml                 # Global configuration
├── contexts/                   # Context storage
│   ├── project_hash1/          # Per-project contexts
│   │   ├── contexts.yaml       # Context definitions
│   │   └── messages/           # Message history
│   │       ├── preserve_previous.json
│   │       └── preserve_previous_analysis.json
│   └── project_hash2/
└── cache/                      # Processing cache
    ├── blocks/                 # Block-level cache
    └── results/                # Result cache
```

### Build Metadata Formats
```python
# Inline comments
# ONO_BUILD_INFO_START
# build_id: abc123
# timestamp: 2025-01-29T10:30:00Z
# source: deploy.sh.ono
# ONO_BUILD_INFO_END

# Structured field (@n@)
{
  "@n@": {
    "build_id": "abc123",
    "source": "config.json.ono"
  }
}

# Separate file (.ono-meta)
{
  "build_info": {
    "build_id": "abc123",
    "source": "template.ono"
  }
}
```

## Development Workflow

### 1. Setup Development Environment
```bash
git clone https://github.com/day50/ono
cd ono
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
pip install -e .
```

### 2. Run Tests
```bash
# Unit tests
python -m pytest tests/

# Integration tests  
python -m pytest tests/integration/

# Coverage
python -m pytest --cov=ono tests/
```

### 3. Development Scripts
```bash
# Lint code
./scripts/lint.sh

# Run full test suite
./scripts/test.sh

# Build package
./scripts/build.sh

# Release new version
./scripts/release.sh
```

## Entry Points

### CLI Entry Point
```python
# ono/__main__.py
from ono.cli import main

if __name__ == "__main__":
    main()
```

### Package Entry Point
```python
# setup.py
entry_points={
    'console_scripts': [
        'ono=ono.cli:main',
    ],
}
```

### API Entry Point
```python
# ono/__init__.py
from .parser import OnoParser
from .processor import TwoPassProcessor
from .context import ContextManager

__version__ = "0.1.0"
__all__ = ["OnoParser", "TwoPassProcessor", "ContextManager"]
```

## Configuration Files

### Global Config (`~/.ono/config.yaml`)
```yaml
llm:
  api_url: "http://localhost:8000/v1"
  api_key: "${ONO_API_KEY}"
  default_model: "claude-3-5-sonnet"

defaults:
  meta_style: "inline"
  context_storage: "~/.ono/contexts"
```

### Project Config (`.ono/config.yaml`)
```yaml
llm:
  default_model: "gpt-4"
  
context:
  default_path: "main"
```

### Package Config (`pyproject.toml`)
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm"]
build-backend = "setuptools.build_meta"

[project]
name = "ono-preprocessor"
dynamic = ["version"]
description = "Universal AI-powered preprocessor"
dependencies = [
    "requests>=2.28.0",
    "pyyaml>=6.0",
    "click>=8.0.0",
]

[project.scripts]
ono = "ono.cli:main"
```