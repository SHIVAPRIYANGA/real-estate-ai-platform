from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class FraudReport(db.Model):
    """Fraud detection report model"""
    __tablename__ = 'fraud_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True, unique=True)
    fraud_score = db.Column(db.Float, nullable=False)  # 0-1
    risk_level = db.Column(db.String(50), nullable=False)  # low, medium, high
    is_duplicate = db.Column(db.Boolean, default=False)
    suspicious_pricing = db.Column(db.Boolean, default=False)
    incomplete_docs = db.Column(db.Boolean, default=False)
    suspicious_owner = db.Column(db.Boolean, default=False)
    reasons = db.Column(JSON, nullable=True)  # List of reasons
    details = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'fraud_score': self.fraud_score,
            'risk_level': self.risk_level,
            'is_duplicate': self.is_duplicate,
            'suspicious_pricing': self.suspicious_pricing,
            'incomplete_docs': self.incomplete_docs,
            'suspicious_owner': self.suspicious_owner,
            'reasons': self.reasons,
            'details': self.details,
            'verified': self.verified,
            'verified_by': self.verified_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<FraudReport {self.id}>'