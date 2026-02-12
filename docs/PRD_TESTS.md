# PRD: Test-Driven Development for Ono

## Executive Summary

This document outlines the Test-Driven Development (TDD) approach for implementing the Ono language processor. The Ono processor transforms template files containing special `<?ono ... ?>` blocks into executable code by leveraging an OpenAI-compatible LLM API.

## Architecture Overview

```
Source File (.ono.ext) → Parser → Concept Pass → Syntax Pass → Output File (.ext)
                              ↓           ↓              ↓
                         Context Mgr → LLM API → Validator
```

## Core Components to Implement

### 1. Parser Engine
**File**: `ono/parser.py` or inline in main module

**Responsibilities**:
- Extract Ono blocks using configurable delimiters
- Handle nested Ono blocks
- Parse configuration parameters (key=value and @ directives)
- Preserve file structure and non-Ono content

**Test Categories**:
- Basic tag extraction
- Multiple delimiters (default: `"?`, `'?`, `{"`, `{"`, `[?`, `<?`)
- Nested Ono blocks
- Configuration parameter parsing
- Malformed block handling

### 2. Context Management
**File**: `ono/context.py`

**Responsibilities**:
- Store and retrieve conversation contexts
- Support context paths (`new`, `preserve_previous`, `preserve_previous/branch`)
- Create context branches (forks)
- Persist contexts to storage

**Test Categories**:
- Create new context
- Retrieve existing context
- Fork context with path
- Context persistence
- Context cleanup

### 3. LLM Interface
**File**: `ono/llm.py`

**Responsibilities**:
- Connect to OpenAI-compatible API (default: http://10.0.0.221:11434)
- Pass through unknown parameters
- Handle request/response with proper timeout
- Support streaming (optional)

**Test Categories**:
- Connection to LLM endpoint
- Parameter passing (model, temperature, max_tokens)
- Pass-through of unknown parameters
- Timeout handling
- Error handling (rate limiting, API errors)

### 4. Two-Pass Processor
**File**: `ono/processor.py`

**Responsibilities**:
- Pass 1: Concept generation (semantic understanding)
- Pass 2: Syntax adaptation (format-specific output)
- Function lifting for complex logic
- Output validation
- Metadata generation

**Test Categories**:
- Simple block processing
- Complex block with function lifting
- Multiple block file processing
- Validation with external tools
- Metadata generation (inline, file, none)

### 5. CLI Interface
**File**: Main `ono.py`

**Responsibilities**:
- Parse command-line arguments
- Process single or multiple files
- Output to stdout or file
- Context management commands
- Info and validation commands

**Test Categories**:
- Basic file processing
- Format inference
- Output routing (stdout, file)
- Context commands
- Metadata control

## Test Priorities

### Level 1: Parser (Highest Priority)
1. Parse simple Ono block with default delimiter
2. Parse multiple Ono blocks in same file
3. Parse nested Ono blocks
4. Parse configuration parameters
5. Parse default delimiters (`"?`, `'?`, `{"`, `{"`, `[?`, `<?`)
6. Handle malformed blocks gracefully

### Level 2: LLM Integration
1. Connect to http://10.0.0.221:11434
2. Send basic completion request
3. Pass model parameter (qwen3:1.7b for quick tests)
4. Pass temperature parameter
5. Handle response parsing
6. Timeout handling (2 minutes max per request)

### Level 3: Concept Pass (with LLM)
1. Simple variable substitution
2. Context preservation across blocks
3. Configuration parameter handling

### Level 4: Syntax Pass
1. Bash output generation (quoting, escaping)
2. Python output generation (string literals)
3. JSON output generation (proper escaping)
4. Function lifting for complex logic

### Level 5: Full End-to-End
1. Process simple template file
2. Process complex template with multiple blocks
3. Context persistence across files
4. Metadata generation and validation

## Implementation Order

### Phase 1: Foundation (Week 1)
- [ ] Write parser tests
- [ ] Implement parser
- [ ] Write LLM interface tests
- [ ] Implement LLM interface

### Phase 2: Processing (Week 2)
- [ ] Write concept pass tests
- [ ] Implement concept pass
- [ ] Write syntax pass tests
- [ ] Implement syntax pass

### Phase 3: Integration (Week 3)
- [ ] Write context management tests
- [ ] Implement context management
- [ ] Write end-to-end tests
- [ ] Integrate all components

### Phase 4: CLI (Week 4)
- [ ] Write CLI tests
- [ ] Implement CLI commands
- [ ] Add validation and info commands

## Test Framework Recommendation

**pytest** - Most appropriate choice because:
- Rich assertion system with detailed error messages
- Excellent for integration tests with fixtures
- Support for parameterized tests
- Good mocking library (pytest-mock)
- Works well with async operations
- Strong ecosystem (pytest-asyncio for async tests)
- Timeboxing support with markers

## Key Test Scenarios

### Parser Tests
```python
def test_parse_simple_block():
    """Parse basic Ono block with default delimiter"""
    result = parser.parse('x = "?ono get temp dir ?"')
    assert len(result.ono_blocks) == 1
    assert result.ono_blocks[0].content == "get temp dir"

def test_parse_multiple_delimiters():
    """Test all default delimiter pairs"""
    test_cases = [
        ('"?ono test ?"', "test"),
        ("'?ono test ?'", "test"),
        ('{"ono test ?}', "test"),
        ('[?ono test ?]', "test"),
        ('<?ono test ?>', "test"),
        ('?ono test ?', "test"),
    ]
```

### LLM Tests
```python
def test_connect_to_ollama():
    """Verify connection to Ollama endpoint"""
    llm = LLMClient("http://10.0.0.221:11434/v1", None)
    response = llm.complete([{"role": "user", "content": "hi"}], model="qwen3:1.7b")
    assert response.content is not None

def test_pass_through_parameters():
    """Verify unknown parameters pass through to API"""
    llm = LLMClient(...)
    llm.complete(..., extra_param="value")  # extra_param should reach API
```

### Processor Tests
```python
def test_simple_substitution():
    """Test simple variable replacement"""
    result = processor.process_block(block, context, "bash")
    assert result.output.strip() == '/tmp'

def test_function_lifting():
    """Test complex logic extraction"""
    block = OnoBlock(content="create backup with error handling", ...)
    result = processor.process_block(block, context, "python")
    assert "_ono_fn_" in result.output  # Function extracted
```

## Configuration

### Default Configuration
- **LLM API URL**: http://10.0.0.221:11434/v1
- **Default Model**: qwen3:1.7b (fast for tests)
- **Context Storage**: ~/.ono/contexts
- **Timeout**: 120 seconds per block

### Test Configuration
```python
# Test-specific model for quick validation
TEST_MODEL = "qwen3:1.7b"
TEST_TIMEOUT = 120  # seconds
TEST_CONTEXT_STORAGE = "/tmp/ono_test_contexts"
```

## Success Criteria

1. All parser tests pass
2. All LLM integration tests pass
3. All processor tests pass
4. End-to-end tests process real template files successfully
5. Output matches expected format (bash, python, json, etc.)
6. Performance acceptable (< 2 minutes per block processing)

## Notes

- Start with parser tests that don't require LLM (pure parsing logic)
- Use pytest fixtures for reusable test data
- Mock LLM calls where possible for unit tests
- Keep integration tests separate (mark with @pytest.mark.integration)
- All tests should clean up after themselves (temp files, contexts)
