class OnoError(Exception):
    """
    Base class for all Ono exceptions.
    """
    pass

class ConfigError(OnoError):
    """
    Raised when there is an error with the Ono configuration.
    """
    pass

class LLMError(OnoError):
    """
    Raised when there is an error with the LLM API.
    """
    pass

class ValidationError(OnoError):
    """
    Raised when there is a validation error.
    """
    pass