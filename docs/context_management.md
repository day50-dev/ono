# Context Management

Ono includes context management for complex workflows.

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