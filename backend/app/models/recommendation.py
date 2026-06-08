from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Recommendation(db.Model):
    """Property recommendation model"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recommended_properties = db.Column(JSON, nullable=True)  # List of property IDs
    recommendation_score = db.Column(db.Float, nullable=False)  # 0-100
    reasoning = db.Column(db.Text, nullable=True)
    criteria = db.Column(JSON, nullable=True)  # Budget, location, type, etc.
    match_percentage = db.Column(db.Float, nullable=True)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    clicked = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommended_properties': self.recommended_properties,
            'recommendation_score': self.recommendation_score,
            'reasoning': self.reasoning,
            'criteria': self.criteria,
            'match_percentage': self.match_percentage,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'clicked': self.clicked
        }
    
    def __repr__(self):
        return f'<Recommendation {self.id}>'