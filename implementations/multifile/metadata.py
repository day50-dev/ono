import datetime
import uuid
from typing import Dict, Any, Optional

class BuildMetadata:
    """
    Generates and formats build metadata for Ono processing.

    This class provides methods for generating unique build IDs, tracking
    processing details, and formatting metadata for different output types.
    """

    def __init__(self):
        """
        Initializes the BuildMetadata.
        """
        self.build_id = self._generate_build_id()
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    def _generate_build_id(self) -> str:
        """
        Generates a unique build ID.
        """
        return str(uuid.uuid4())

    def get_metadata(self, source: str) -> Dict[str, Any]:
        """
        Gets the build metadata.

        Args:
            source: The source file being processed.

        Returns:
            A dictionary containing the build metadata.
        """
        return {
            "build_id": self.build_id,
            "timestamp": self.timestamp,
            "source": source,
        }

    def format_metadata(self, metadata: Dict[str, Any], format: str) -> str:
        """
        Formats the metadata for the given format.

        Args:
            metadata: The metadata to format.
            format: The format to format the metadata for.

        Returns:
            The formatted metadata as a string.
        """
        # TODO: Implement format-specific metadata formatting
        return str(metadata)