from datetime import datetime
from app import db

class AdminLog(db.Model):
    """Admin activity log model"""
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(255), nullable=False)  # create, update, delete, verify, etc.
    resource_type = db.Column(db.String(50), nullable=False)  # user, property, fraud, etc.
    resource_id = db.Column(db.Integer, nullable=True)
    changes = db.Column(db.Text, nullable=True)  # JSON string of changes
    status = db.Column(db.String(50), default='success')  # success, failed
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'changes': self.changes,
            'status': self.status,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AdminLog {self.id}>'