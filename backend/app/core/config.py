"""
Application configuration using Pydantic settings.

Loads configuration from environment variables and .env file.
"""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden via environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Application
    environment: str = Field(default="development", description="Environment (development, production)")
    port: int = Field(default=7676, description="Application port")
    debug: bool = Field(default=True, description="Debug mode")

    # API
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    project_name: str = Field(default="X-UAV API", description="Project name")

    # Database - PostgreSQL
    database_url: str = Field(
        default="postgresql://xuav:development@localhost:5432/xuav",
        description="PostgreSQL connection URL"
    )

    # Database - ArangoDB
    graph_db_url: str = Field(default="http://localhost:8529", description="ArangoDB URL")
    graph_db_name: str = Field(default="xuav", description="ArangoDB database name")
    graph_db_username: str = Field(default="root", description="ArangoDB username")
    graph_db_password: str = Field(default="development", description="ArangoDB password")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL")

    # Ollama LLM
    ollama_url: str = Field(default="http://localhost:11434", description="Ollama service URL")
    ollama_model: str = Field(default="qwen2.5:3b", description="Ollama model name")

    # MCP Server
    mcp_server_path: str = Field(default="/app/mcp_server.py", description="MCP server path")

    # Security
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")

    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:7676", "http://localhost:8000"],
        description="Allowed CORS origins"
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


# Global settings instance
settings = Settings()
