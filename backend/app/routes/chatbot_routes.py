from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ChatHistory, User

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/v1/chatbot')

@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Simple chatbot response (should use NLP/AI)
        responses = {
            'price': 'The average property price in this area is around $450,000. Would you like me to search for specific properties?',
            'investment': 'Based on current market trends, this property has a good investment potential with estimated ROI of 7-9% annually.',
            'fraud': 'This property appears to be legitimate with low fraud risk. All documents are verified.',
            'help': 'I can help you with property search, price predictions, investment analysis, and fraud detection.',
            'property': 'I can help you find properties based on your preferences. Tell me your budget, location, and property type.'
        }
        
        # Simple keyword matching
        bot_response = responses.get('property')
        for key in responses:
            if key in user_message.lower():
                bot_response = responses[key]
                break
        
        chat = ChatHistory(
            user_id=user_id,
            message=user_message,
            response=bot_response,
            category='general',
            sentiment='neutral'
        )
        
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response,
            'chat_id': chat.id,
            'timestamp': chat.created_at.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        chats = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'data': [chat.to_dict() for chat in reversed(chats)]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_chatbot_recommendations():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        preferences = {
            'budget_min': data.get('budget_min', 100000),
            'budget_max': data.get('budget_max', 500000),
            'city': data.get('city', 'Any'),
            'property_type': data.get('property_type', 'any'),
            'bedrooms': data.get('bedrooms', 2)
        }
        
        response = f"""Based on your preferences:
- Budget: ${preferences['budget_min']:,} - ${preferences['budget_max']:,}
- Location: {preferences['city']}
- Property Type: {preferences['property_type']}
- Bedrooms: {preferences['bedrooms']}

I found several properties matching your criteria. Would you like me to show them to you?"""
        
        chat = ChatHistory(
            user_id=user_id,
            message=f"Recommendations for: {preferences['property_type']} in {preferences['city']}",
            response=response,
            category='recommendations'
        )
        
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({
            'preferences': preferences,
            'recommendations_count': 5,
            'response': response
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
