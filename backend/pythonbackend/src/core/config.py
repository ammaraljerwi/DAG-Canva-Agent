from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CANVA_APP_ID: str
    CANVA_CLIENT_ID: str
    CANVA_CLIENT_SECRET: str
    REDIRECT_URI: str
    DATABASE_URL: str
    BUCKET_NAME: str
    BUCKET_REGION: str

    class Config:
        env_file = "../../.env"
        extra = "allow"


settings = Settings()
