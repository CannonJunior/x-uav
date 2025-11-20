"""
Configuration management for X-UAV backend.

Loads configuration from environment variables and .env file.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        HOST: Server host address
        PORT: Server port number
        DEBUG: Debug mode flag
        RELOAD: Auto-reload flag for development
        DATABASE_PATH: Path to DuckDB database file
        ALLOWED_ORIGINS: List of allowed CORS origins
        API_V1_PREFIX: API version 1 prefix
        PROJECT_NAME: Project name for API documentation
        VERSION: API version
    """

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 7676
    DEBUG: bool = True
    RELOAD: bool = True

    # Database Configuration
    DATABASE_PATH: str = "./data_db/uavs.duckdb"

    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:7676,http://127.0.0.1:7676"

    # API Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "X-UAV API"
    VERSION: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        """
        Get allowed origins as a list.

        Returns:
            List[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def database_path_absolute(self) -> Path:
        """
        Get absolute path to database file.

        Returns:
            Path: Absolute path to database
        """
        # Reason: Convert relative path to absolute based on project structure
        base_path = Path(__file__).parent.parent
        return (base_path / self.DATABASE_PATH).resolve()


# Global settings instance
settings = Settings()
