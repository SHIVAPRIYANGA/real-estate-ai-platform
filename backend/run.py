import os
from app import create_app, db
from app.models import User, Property, PropertyImage, Prediction, FraudReport, Verification, ChatHistory, Recommendation, AdminLog, Transaction

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make model instances available in shell"""
    return {
        'db': db,
        'User': User,
        'Property': Property,
        'PropertyImage': PropertyImage,
        'Prediction': Prediction,
        'FraudReport': FraudReport,
        'Verification': Verification,
        'ChatHistory': ChatHistory,
        'Recommendation': Recommendation,
        'AdminLog': AdminLog,
        'Transaction': Transaction
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', True)
    )