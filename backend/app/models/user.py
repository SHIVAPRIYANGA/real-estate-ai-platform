from datetime import datetime
from app import db
import bcrypt

class User(db.Model):
    """User model for authentication and profiles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='user')  # user, admin, agent
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    properties = db.relationship('Property', backref='owner', lazy=True, foreign_keys='Property.owner_id')
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    chat_history = db.relationship('ChatHistory', backref='user', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)
    saved_properties = db.relationship('Property', secondary='saved_properties', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'profile_photo': self.profile_photo,
            'bio': self.bio,
            'verified': self.verified,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

# Association table for saved properties
saved_properties = db.Table(
    'saved_properties',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True),
    db.Column('saved_at', db.DateTime, default=datetime.utcnow)
)