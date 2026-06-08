from datetime import datetime
from app import db

class Prediction(db.Model):
    """AI Price prediction model"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    predicted_price = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)  # 0-1
    model_version = db.Column(db.String(50), nullable=False)
    features_used = db.Column(db.Text, nullable=True)  # JSON string
    market_trend = db.Column(db.String(50), nullable=True)  # up, down, stable
    estimated_rental_yield = db.Column(db.Float, nullable=True)
    investment_score = db.Column(db.Float, nullable=True)  # 0-100
    risk_score = db.Column(db.Float, nullable=True)  # 0-100
    recommendation = db.Column(db.String(50), nullable=True)  # buy, hold, avoid
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'user_id': self.user_id,
            'predicted_price': self.predicted_price,
            'confidence_score': self.confidence_score,
            'model_version': self.model_version,
            'features_used': self.features_used,
            'market_trend': self.market_trend,
            'estimated_rental_yield': self.estimated_rental_yield,
            'investment_score': self.investment_score,
            'risk_score': self.risk_score,
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Prediction {self.id}>'