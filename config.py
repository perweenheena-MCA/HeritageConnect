import os

class Config:
    SECRET_KEY = os.environ.get("HERITAGE_SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///heritageconnect.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

