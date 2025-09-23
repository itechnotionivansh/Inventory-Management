# app/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_APP = os.getenv("FLASK_APP", "run.py")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    DEBUG = os.getenv("FLASK_ENV") == "development"

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("ACCESS_TOKEN_EXPIRES", 900)))  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("REFRESH_TOKEN_EXPIRES", 2592000)))  # 30 days
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Rate limiting
    RATELIMIT_DEFAULT = os.getenv("RATE_LIMIT_DEFAULT", "100 per hour")
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "memory://")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}