import tempfile
import shutil
from pathlib import Path


class Context:
    def __init__(self):
        self.messages = []


class ContextManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_context(self, path: str) -> Context:
        ctx_path = self.base_dir / path
        ctx_path.mkdir(parents=True, exist_ok=True)
        ctx = Context()
        return ctx

    def update_context(self, path: str, messages: list):
        ctx_path = self.base_dir / path
        ctx_path.mkdir(parents=True, exist_ok=True)

    def cleanup_context(self, path: str):
        ctx_path = self.base_dir / path
        if ctx_path.exists():
            shutil.rmtree(ctx_path)
