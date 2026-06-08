from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Property(db.Model):
    """Property listing model"""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, index=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)  # in sq ft
    property_type = db.Column(db.String(50), nullable=False)  # apartment, house, villa, commercial
    status = db.Column(db.String(50), default='active')  # active, sold, rented, inactive
    amenities = db.Column(JSON, nullable=True)  # pool, garden, gym, etc.
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    featured = db.Column(db.Boolean, default=False)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='property', lazy=True, cascade='all, delete-orphan')
    fraud_report = db.relationship('FraudReport', backref='property', lazy=True, uselist=False, cascade='all, delete-orphan')
    verification = db.relationship('Verification', backref='property', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_predictions=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': self.area,
            'property_type': self.property_type,
            'status': self.status,
            'amenities': self.amenities,
            'owner_id': self.owner_id,
            'featured': self.featured,
            'views_count': self.views_count,
            'images': [img.to_dict() for img in self.images],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_predictions and self.predictions:
            data['predictions'] = [pred.to_dict() for pred in self.predictions[:3]]
        
        return data
    
    def __repr__(self):
        return f'<Property {self.title}>'

class PropertyImage(db.Model):
    """Property images model"""
    __tablename__ = 'property_images'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    image_url = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary,
            'uploaded_at': self.uploaded_at.isoformat()
        }
    
    def __repr__(self):
        return f'<PropertyImage {self.id}>'