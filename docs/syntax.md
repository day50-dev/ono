# Syntax

Ono uses the `<?ono ... ?>` syntax to embed Ono blocks in any file format.

## Inline Requests

```
<?ono get users temp directory ?>
```

## Block Syntax with Configuration

```
<?ono
model="claude-3-5-sonnet"
temperature=0.1

get users temp directory, ensuring it follows XDG standards on Linux
?>
```

## Parameters

Ono supports two types of parameters:

- Pass-through parameters (sent directly to the LLM): `model="gpt-4"`, `temperature=0.2`
- Ono-specific parameters (prefixed with `@`): `@context="preserve"`, `@execution="once"`