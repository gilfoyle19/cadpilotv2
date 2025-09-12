from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional
from .openrouter_models import OpenRouterModel

class Settings(BaseSettings):
    # Configuration for OpenRouter
    openrouter_api_key: str = Field(..., validation_alias="OPENROUTER_API_KEY") 
    openrouter_base_url: str = Field(
        "https://openrouter.ai/api/v1",
        validation_alias="OPENROUTER_BASE_URL"
    )

    default_model: str = Field(
        OpenRouterModel.OPENAI_GPT_OSS,  # Default to Google Gemini Pro
        validation_alias="DEFAULT_MODEL"
    )

    #Application settings
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    max_iterations: int = Field(5, validation_alias="MAX_ITERATIONS")
    request_timeout: int = Field(60, validation_alias="REQUEST_TIMEOUT")

    @field_validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}.")
        return v.upper()
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Global settings instance
settings = Settings()
