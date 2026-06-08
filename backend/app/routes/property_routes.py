from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cache
from app.models import Property, User

property_bp = Blueprint('property', __name__, url_prefix='/api/v1/properties')

@property_bp.route('', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_properties():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        query = Property.query.filter_by(status='active')
        
        if request.args.get('city'):
            query = query.filter_by(city=request.args.get('city'))
        if request.args.get('property_type'):
            query = query.filter_by(property_type=request.args.get('property_type'))
        if request.args.get('min_price'):
            query = query.filter(Property.price >= float(request.args.get('min_price')))
        if request.args.get('max_price'):
            query = query.filter(Property.price <= float(request.args.get('max_price')))
        
        paginated = query.paginate(page=page, per_page=per_page)
        return jsonify({
            'data': [prop.to_dict() for prop in paginated.items],
            'pagination': {'page': page, 'per_page': per_page, 'total': paginated.total}
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@property_bp.route('<int:property_id>', methods=['GET'])
def get_property(property_id):
    try:
        prop = Property.query.get_or_404(property_id)
        prop.views_count += 1
        db.session.commit()
        return jsonify(prop.to_dict(include_predictions=True)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@property_bp.route('', methods=['POST'])
@jwt_required()
def create_property():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required = ['title', 'price', 'address', 'city', 'bedrooms', 'bathrooms', 'area', 'property_type']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        prop = Property(
            title=data['title'],
            description=data.get('description'),
            price=float(data['price']),
            address=data['address'],
            city=data['city'],
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            bedrooms=int(data['bedrooms']),
            bathrooms=float(data['bathrooms']),
            area=float(data['area']),
            property_type=data['property_type'],
            amenities=data.get('amenities'),
            owner_id=user_id
        )
        
        db.session.add(prop)
        db.session.commit()
        return jsonify({'message': 'Property created', 'property': prop.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@property_bp.route('<int:property_id>/save', methods=['POST'])
@jwt_required()
def save_property(property_id):
    try:
        user_id = get_jwt_identity()
        prop = Property.query.get_or_404(property_id)
        user = User.query.get(user_id)
        
        if prop in user.saved_properties:
            return jsonify({'message': 'Property already saved'}), 200
        
        user.saved_properties.append(prop)
        db.session.commit()
        return jsonify({'message': 'Property saved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@property_bp.route('saved', methods=['GET'])
@jwt_required()
def get_saved_properties():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        paginated = user.saved_properties.paginate(page=page, per_page=per_page)
        return jsonify({
            'data': [prop.to_dict() for prop in paginated.items],
            'pagination': {'page': page, 'per_page': per_page, 'total': paginated.total}
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
