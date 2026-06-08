import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://real_estate_user:secure_password@localhost:5432/real_estate_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24)))
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # API
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PREFIX = os.getenv('API_PREFIX', '/api/v1')
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))
    
    # Rate Limiting
    RATELIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 100))
    RATELIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 3600))
    
    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,pdf').split(','))
    
    # AI/ML
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', './models/')
    PREDICTION_THRESHOLD = float(os.getenv('PREDICTION_THRESHOLD', 0.7))
    FRAUD_DETECTION_THRESHOLD = float(os.getenv('FRAUD_DETECTION_THRESHOLD', 0.6))
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Blockchain
    BLOCKCHAIN_ENABLED = os.getenv('BLOCKCHAIN_ENABLED', 'True') == 'True'
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'testnet')
    
    # Analytics
    ANALYTICS_ENABLED = os.getenv('ANALYTICS_ENABLED', 'True') == 'True'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}