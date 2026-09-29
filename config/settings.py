import os

class Settings:
    """
    Runtime configuration for the Job Market Research Agent.
    Values should be loaded from environment variables to avoid hardcoded secrets.
    """
    
    # Using environment variables for configuration
    EXTERNAL_DATA_API_KEY = os.environ.get("EXTERNAL_DATA_API_KEY", "")
    
    # Other potential settings
    DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "USD")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

settings = Settings()
