# Ono Architecture & Technical Overview

## System Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────────┐
│  Source File    │    │     Ono      │    │  LLM API    │    │  Output File   │
│  (.ono)         │───▶│   Processor  │───▶│  Endpoint   │───▶│  + Metadata    │
│                 │    │              │    │             │    │                │
└─────────────────┘    └──────────────┘    └─────────────┘    └────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Context    │
                       │   Storage    │
                       └──────────────┘
```

## Core Components

### 1. Parser Engine (`ono/parser.py`)

The parser engine is responsible for extracting and analyzing `<?ono ... ?>` blocks from source files.

**Key Responsibilities:**
- Recursive parsing of nested ono blocks
- Configuration parameter extraction and validation
- Preservation of file structure and non-ono content
- Error handling for malformed syntax

**Data Structures:**
```python
@dataclass
class OnoBlock:
    content: str              # The actual request text
    config: Dict[str, Any]    # Parsed configuration parameters
    start_pos: int           # Character position in source
    end_pos: int             # End position in source
    block_id: str            # Unique identifier for tracking

@dataclass
class ParsedFile:
    blocks: List[OnoBlock]   # All ono blocks found
    template: str            # Original file with placeholders
    metadata: FileMetadata   # Source file information
```

**Configuration Types:**
- **Pass-through**: `model="gpt-4"`, `temperature=0.2` → sent directly to LLM
- **Ono-specific**: `@context="path"`, `@execution="once"` → processed by ono

### 2. Context Management (`ono/context.py`)

Handles conversation context persistence and routing across ono block executions.

**Context Path System:**
```
@context="new"                    # Fresh context
@context="preserve_previous"      # Linear continuation  
@context="preserve_previous/analysis"          # Named branch
@context="preserve_previous/analysis/testing"  # Nested branch
```

**Implementation:**
```python
class ContextManager:
    def __init__(self, storage_path: str):
        self.storage = ContextStorage(storage_path)
    
    def get_context(self, path: str) -> Context:
        """Retrieve context for given path, creating if necessary"""
        
    def update_context(self, path: str, messages: List[Dict]):
        """Update context with new conversation messages"""
        
    def fork_context(self, source_path: str, target_path: str):
        """Create new context branch from existing context"""
```

**Storage Format:**
```yaml
# ~/.ono/contexts/project_hash/context.yaml
contexts:
  "preserve_previous":
    created_at: "2025-01-29T10:30:00Z"
    messages:
      - role: "user"
        content: "analyze this codebase"
      - role: "assistant" 
        content: "This appears to be a Python web application..."
    
  "preserve_previous/analysis":
    parent: "preserve_previous"
    created_at: "2025-01-29T10:35:00Z"
    messages:
      - role: "user"
        content: "generate tests based on the analysis"
```

### 3. Two-Pass Processor (`ono/processor.py`)

Implements the two-pass processing model for optimal results.

**Pass 1: Concept Pass**
- Receives full file context + ono block content
- Focuses on semantic understanding and appropriate responses
- Generates conceptually correct but potentially format-agnostic output

**Pass 2: Syntax Pass**
- Takes Pass 1 output + target format specification
- Applies language-specific formatting, escaping, and syntax rules
- Validates output with format-specific tools when available

```python
class TwoPassProcessor:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.validators = self._load_validators()
    
    def process_block(self, block: OnoBlock, file_context: str, 
                     target_format: str) -> ProcessedBlock:
        # Pass 1: Concept
        concept_result = self._concept_pass(block, file_context)
        
        # Pass 2: Syntax
        final_result = self._syntax_pass(concept_result, target_format)
        
        # Optional: Validation
        if target_format in self.validators:
            self._validate_output(final_result, target_format)
            
        return final_result
```

### 4. LLM Interface (`ono/llm.py`)

Abstraction layer over OpenAI-compatible APIs with transparent parameter passing.

**Design Principles:**
- **Transparent proxying**: Unknown parameters pass through unchanged
- **Minimal validation**: Only validate ono-specific parameters
- **Provider agnostic**: Works with any OpenAI-compatible endpoint

```python
class LLMClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def complete(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """Send completion request, passing through all unknown parameters"""
        
        # Extract ono-specific parameters
        ono_params = self._extract_ono_params(kwargs)
        
        # Pass everything else through to the API
        api_params = {k: v for k, v in kwargs.items() 
                     if not k.startswith('@')}
        
        response = self._make_request(messages, **api_params)
        return LLMResponse(response, ono_params)
```

### 5. Build Metadata (`ono/metadata.py`)

Tracks build information for reproducibility and debugging.

**Metadata Types:**
- **Inline comments**: For languages that support comments
- **Structured fields**: `@n@` field for JSON/YAML/TOML
- **Separate files**: `.ono-meta` files when inline not possible
- **None**: Clean output with no metadata

```python
@dataclass
class BuildMetadata:
    build_id: str                    # Unique build identifier
    timestamp: datetime              # Build time
    ono_version: str                # Ono version used
    source_files: List[str]         # Input files
    target_format: str              # Output format
    blocks: List[BlockExecution]    # Per-block details
    total_tokens: int               # Total token usage
    execution_time: float           # Total processing time

@dataclass  
class BlockExecution:
    block_id: str
    content: str                    # Original request
    resolved_value: str             # Final output
    model: str                     # Model used
    tokens_used: int               # Token count
    execution_time: float          # Processing time
    context_path: str              # Context used
```

**Output Formats:**
```bash
# Inline comments (bash/python/etc)
# ONO_BUILD_INFO_START
# build_id: abc123
# timestamp: 2025-01-29T10:30:00Z
# blocks: [{id: 1, resolved: "/tmp", tokens: 42}]
# ONO_BUILD_INFO_END
```

```json
// Structured field (JSON/YAML)
{
  "@n@": {
    "build_id": "abc123",
    "timestamp": "2025-01-29T10:30:00Z",
    "source": "config.json.ono"
  },
  "actual": "data"
}
```

### 6. CLI Interface (`ono/cli.py`)

Command-line interface for ono operations.

**Core Commands:**
```bash
# Basic processing
ono --format bash script.sh.ono > script.sh

# Metadata control
ono --format json --meta file config.json.ono > config.json
ono --format python --meta none clean.py.ono > clean.py

# Context management  
ono --context new fresh.sh.ono > fresh.sh
ono contexts list                    # Show available contexts
ono contexts clean                   # Clean up old contexts

# Build information
ono info script.sh                   # Show build metadata
ono validate --format python test.py.ono  # Validate without processing
```

## Configuration System

### Global Configuration (`~/.ono/config.yaml`)
```yaml
llm:
  api_url: "http://localhost:8000/v1"
  api_key: "${ONO_API_KEY}"
  default_model: "claude-3-5-sonnet"
  timeout: 30

defaults:
  meta_style: "inline"               # inline, file, none
  context_storage: "~/.ono/contexts"
  temp_cleanup: true

formats:
  bash:
    validator: "shellcheck"
  python:
    validator: "python -m py_compile"
  json:
    validator: "jq ."

demo:
  server_url: "demo.onolang.com:8080"
```

### Project Configuration (`.ono/config.yaml`)
```yaml
# Project-specific overrides
llm:
  default_model: "gpt-4"
  
context:
  default_path: "project_main"
  auto_cleanup: false

formats:
  dockerfile:
    validator: "hadolint"
```

## Processing Flow

### 1. File Processing Pipeline
```python
def process_file(source_path: str, target_format: str, 
                meta_style: str = "inline") -> ProcessedFile:
    
    # 1. Parse source file
    parsed = parser.parse_file(source_path)
    
    # 2. Load file context for semantic understanding
    file_context = _load_file_context(source_path)
    
    # 3. Process each ono block
    results = []
    for block in parsed.blocks:
        # Get or create context
        context = context_manager.get_context(block.context_path)
        
        # Two-pass processing
        result = processor.process_block(block, file_context, target_format)
        
        # Update context with conversation
        context_manager.update_context(block.context_path, result.messages)
        
        results.append(result)
    
    # 4. Generate output with metadata
    output = template_engine.render(parsed.template, results)
    metadata = build_metadata.generate(parsed, results)
    
    return ProcessedFile(output, metadata)
```

### 2. Context Resolution
```python
def resolve_context_path(path: str, current_contexts: Dict) -> Context:
    if path == "new":
        return Context.create_new()
    
    elif path == "preserve_previous":
        return current_contexts.get_latest()
    
    elif path.startswith("preserve_previous/"):
        # Parse path: preserve_previous/analysis/testing
        parts = path.split("/")[1:]  # ["analysis", "testing"]
        
        # Navigate context tree
        context = current_contexts.get_latest()
        for part in parts:
            context = context.get_or_create_child(part)
        
        return context
    
    else:
        raise ValueError(f"Invalid context path: {path}")
```

## Error Handling & Recovery

### 1. Parse Errors
- Malformed ono blocks → Clear error messages with line numbers
- Unmatched delimiters → Suggest corrections
- Invalid configuration → Show valid parameter options

### 2. LLM API Errors
- Rate limiting → Exponential backoff retry
- API downtime → Graceful failure with cached results when possible
- Invalid responses → Fallback to simpler prompts

### 3. Context Errors
- Missing contexts → Auto-create with warning
- Corrupted context files → Recovery from backups
- Path resolution failures → Clear error messages

## Performance Considerations

### 1. Caching Strategy
- **Block-level caching**: Identical blocks with same context → reuse results
- **Context caching**: Avoid reloading unchanged contexts
- **File-level caching**: Skip processing if source unchanged

### 2. Parallel Processing
- Independent ono blocks → Process in parallel
- Context dependencies → Respect ordering requirements
- I/O operations → Async file operations where possible

### 3. Memory Management
- Large files → Stream processing
- Context storage → Lazy loading
- Temporary files → Automatic cleanup

## Security Considerations

### 1. Input Validation
- Sanitize ono block content
- Validate configuration parameters
- Prevent path traversal in context storage

### 2. API Security
- Secure API key storage
- Request signing where supported
- Rate limiting on client side

### 3. Output Safety
- Validate generated code where possible
- Sandboxed execution for validation
- Clear warnings for potentially unsafe operations

## Testing Strategy

### 1. Unit Tests
- Parser edge cases (nested blocks, malformed syntax)
- Context management (path resolution, branching)
- Metadata generation (all output formats)
- Configuration handling

### 2. Integration Tests
- End-to-end file processing
- Multi-format generation
- Context persistence across runs
- Error recovery scenarios

### 3. Performance Tests
- Large file processing (>1MB templates)
- Many context paths (>100 branches)
- Concurrent processing
- Memory usage profiling

## Deployment Architecture

### 1. Local Installation
```bash
pip install ono-preprocessor
ono config init
```

### 2. Demo Server (Optional)
- Simple TCP server for `nc` integration
- Sandboxed execution environment
- Rate limiting and abuse prevention
- Minimal state (no persistent contexts)

### 3. CI/CD Integration
```yaml
# GitHub Actions example
- name: Process Ono templates  
  run: |
    ono --format bash --meta none deploy.sh.ono > deploy.sh
    chmod +x deploy.sh
```

## Future Extensibility

### 1. Plugin System
- Custom validators for new formats
- Additional context storage backends
- Custom LLM providers

### 2. Format Support
- New output formats via configuration
- Custom escape/quote rules
- Language-specific optimizations

### 3. Context Enhancements
- Context sharing between projects
- Context import/export
- Advanced context analytics