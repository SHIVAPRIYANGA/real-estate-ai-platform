from datetime import datetime
from app import db

class ChatHistory(db.Model):
    """Chat history model for chatbot"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # property, price, investment, fraud, support
    sentiment = db.Column(db.String(50), nullable=True)  # positive, negative, neutral
    helpful = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'response': self.response,
            'category': self.category,
            'sentiment': self.sentiment,
            'helpful': self.helpful,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatHistory {self.id}>'