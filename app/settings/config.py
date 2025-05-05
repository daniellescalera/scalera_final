from builtins import bool, int, str
from pathlib import Path
from pydantic import Field, AnyUrl, DirectoryPath
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_login_attempts: int = Field(default=3, description="Maximum allowed login attempts")

    # Server configuration
    server_base_url: AnyUrl = Field(default='http://localhost', description="Base URL of the server")
    server_download_folder: str = Field(default='downloads', description="Folder for storing downloaded files")

    # Security and authentication configuration
    secret_key: str = Field(default="secret-key", description="Secret key for encryption")
    algorithm: str = Field(default="HS256", description="Algorithm used for encryption")
    admin_user: str = Field(default='admin', description="Default admin username")
    admin_password: str = Field(default='secret', description="Default admin password")
    debug: bool = Field(default=False, description="Debug mode outputs errors and sqlalchemy queries")
    jwt_secret_key: str = Field(default="a_very_secret_key", description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=15, description="Access token expiration time (minutes)")
    refresh_token_expire_minutes: int = Field(default=1440, description="Refresh token expiration time (minutes)")

    # Database configuration
    database_url: str = Field(
        default='postgresql+asyncpg://user:password@localhost/myappdb',
        description="URL for connecting to the database"
    )
    DATABASE_URL: str = Field(default_factory=lambda: Settings().database_url)

    postgres_user: str = Field(default='user', description="PostgreSQL username")
    postgres_password: str = Field(default='password', description="PostgreSQL password")
    postgres_server: str = Field(default='localhost', description="PostgreSQL server address")
    postgres_port: str = Field(default='5432', description="PostgreSQL port")
    postgres_db: str = Field(default='myappdb', description="PostgreSQL database name")

    # Discord configuration
    discord_bot_token: str = Field(default='NONE', description="Discord bot token")
    discord_channel_id: int = Field(default=1234567890, description="Default Discord channel ID")

    # OpenAI Key
    openai_api_key: str = Field(default='NONE', description="OpenAI API key")

    # Email settings
    send_real_mail: bool = Field(default=False, description="Use real mail or mock")
    smtp_server: str = Field(default='smtp.mailtrap.io', description="SMTP server for sending emails")
    smtp_port: int = Field(default=2525, description="SMTP port")
    smtp_username: str = Field(default='your-mailtrap-username', description="SMTP username")
    smtp_password: str = Field(default='your-mailtrap-password', description="SMTP password")

   
    from pydantic import computed_field  # <-- ADD THIS at the top of config.py

    @computed_field
    @property
    def sync_database_url(self) -> str:
        return self.database_url.replace("postgresql+asyncpg", "postgresql")


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings
settings = Settings()

def get_settings() -> Settings:
    return settings
