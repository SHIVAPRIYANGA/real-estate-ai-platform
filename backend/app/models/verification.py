from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Verification(db.Model):
    """Blockchain verification model"""
    __tablename__ = 'verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True, unique=True)
    transaction_hash = db.Column(db.String(255), nullable=True, unique=True)
    block_number = db.Column(db.Integer, nullable=True)
    owner_verified = db.Column(db.Boolean, default=False)
    documents_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(50), default='pending')  # pending, verified, failed
    owner_details = db.Column(JSON, nullable=True)
    document_hashes = db.Column(JSON, nullable=True)
    verification_history = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'transaction_hash': self.transaction_hash,
            'block_number': self.block_number,
            'owner_verified': self.owner_verified,
            'documents_verified': self.documents_verified,
            'verification_status': self.verification_status,
            'owner_details': self.owner_details,
            'document_hashes': self.document_hashes,
            'verification_history': self.verification_history,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'verified_at': self.verified_at.isoformat() if self.verified_at else None
        }
    
    def __repr__(self):
        return f'<Verification {self.id}>'