from typing import Dict, Any, Optional

class ContextManager:
    """
    Manages the context for Ono processing.

    This class provides methods for storing, retrieving, and manipulating context
    information during Ono processing.
    """

    def __init__(self):
        """
        Initializes the ContextManager.
        """
        self.contexts: Dict[str, Dict[str, Any]] = {}

    def create_context(self, context_id: str) -> None:
        """
        Creates a new context with the given ID.

        Args:
            context_id: The ID of the new context.
        """
        if context_id not in self.contexts:
            self.contexts[context_id] = {}

    def get_context(self, context_id: str) -> Dict[str, Any]:
        """
        Retrieves the context with the given ID.

        Args:
            context_id: The ID of the context to retrieve.

        Returns:
            The context as a dictionary.
        """
        if context_id not in self.contexts:
            self.create_context(context_id)
        return self.contexts[context_id]

    def update_context(self, context_id: str, data: Dict[str, Any]) -> None:
        """
        Updates the context with the given ID with the provided data.

        Args:
            context_id: The ID of the context to update.
            data: A dictionary containing the data to update the context with.
        """
        context = self.get_context(context_id)
        context.update(data)

    def clear_context(self, context_id: str) -> None:
        """
        Clears the context with the given ID.

        Args:
            context_id: The ID of the context to clear.
        """
        if context_id in self.contexts:
            self.contexts[context_id] = {}

    def delete_context(self, context_id: str) -> None:
        """
        Deletes the context with the given ID.

        Args:
            context_id: The ID of the context to delete.
        """
        if context_id in self.contexts:
            del self.contexts[context_id]