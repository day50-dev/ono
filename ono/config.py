import yaml
import os
from typing import Optional, Dict, Any

class OnoConfig:
    """
    Configuration management for Ono.
    Loads global and project-specific configurations, handles environment variables,
    and provides default values.
    """

    def __init__(self, global_config_path: Optional[str] = None, project_config_path: Optional[str] = None):
        """
        Initializes the OnoConfig with optional paths to global and project-specific
        configuration files.
        """
        self.global_config_path = global_config_path or os.path.join(os.path.expanduser("~"), ".ono", "config.yaml")
        self.project_config_path = project_config_path or os.path.join(".ono", "config.yaml")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads configuration from global and project-specific files, merging them
        with project-specific settings overriding global settings.
        """
        global_config = self._load_yaml(self.global_config_path)
        project_config = self._load_yaml(self.project_config_path)

        # Merge configurations, with project config overriding global config
        config = global_config.copy()
        config.update(project_config)
        return config

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        """
        Loads a YAML file from the given path. Returns an empty dictionary if the
        file does not exist or if there is an error loading the file.
        """
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {path} - {e}")
            return {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value for the given key. If the key is not found,
        returns the provided default value.
        """
        return self.config.get(key, default)

    def __repr__(self):
        return f"OnoConfig(config={self.config})"