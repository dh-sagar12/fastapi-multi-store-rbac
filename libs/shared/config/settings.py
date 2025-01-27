from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Stage(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

class Settings(BaseSettings):
    # Use SettingsConfigDict to configure environment variable loading
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore"
    )

    # Application Configuration
    APP_ENV: AppEnvironment
    STAGE: Stage
    LOG_LEVEL: str
    
    # Database Configuration
    POSTGRES_WRITE_HOST: str
    POSTGRES_READ_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    
    # Redis Configuration
    REDIS_URL: str
    REDIS_PORT: int
    
    # Authentication Service
    AUTH_URL: str
    
    # JWT Configuration
    ACCESS_TOKEN_EXPIRES_AT: int
    REFRESH_TOKEN_EXPIRES_AT: int
    JWT_ALGORITHM: str
    JWT_SECRET: str

    @property
    def POSTGRES_WRITE_URL(self) -> str:
        """Generate PostgreSQL write connection URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_WRITE_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_READ_URL(self) -> str:
        """Generate PostgreSQL read connection URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_READ_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_CONNECTION_URL(self) -> str:
        """Generate Redis connection URL"""
        return f"redis://{self.REDIS_URL}:{self.REDIS_PORT}"

# Initialize settings
try:
    settings = Settings()
except Exception as e:
    print("Error loading settings. Please check your environment variables:")
    print(str(e))
    raise