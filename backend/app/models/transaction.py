from datetime import datetime
from app import db

class Transaction(db.Model):
    """Transaction model for revenue tracking"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=True, index=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # payment, refund, commission
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    payment_method = db.Column(db.String(50), nullable=True)  # credit_card, bank_transfer, wallet
    reference_id = db.Column(db.String(255), nullable=True, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'property_id': self.property_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'payment_method': self.payment_method,
            'reference_id': self.reference_id,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Transaction {self.id}>'