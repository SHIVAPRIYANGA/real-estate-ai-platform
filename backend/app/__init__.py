from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os

from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment (development, testing, production)
    
    Returns:
        Flask app instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL']
    })
    limiter.init_app(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # CLI commands
    register_cli_commands(app)
    
    # Health check
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'service': 'Real Estate AI Platform',
            'version': '1.0.0'
        }, 200
    
    return app

def register_blueprints(app):
    """Register all blueprints"""
    from app.routes import auth_bp, property_bp, prediction_bp, fraud_bp, verification_bp, chatbot_bp, analytics_bp, user_bp, admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(fraud_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

def register_error_handlers(app):
    """Register error handlers"""
    from app.utils.errors import handle_400, handle_401, handle_403, handle_404, handle_500
    
    app.register_error_handler(400, handle_400)
    app.register_error_handler(401, handle_401)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)

def register_cli_commands(app):
    """Register CLI commands"""
    @app.cli.command()
    def init_db():
        """Initialize database"""
        db.create_all()
        print('Database initialized!')
    
    @app.cli.command()
    def seed_db():
        """Seed database with sample data"""
        from app.models import User, Property
        # Add seeding logic here
        print('Database seeded!')

def setup_logging(app):
    """Setup application logging"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Real Estate AI Platform startup')