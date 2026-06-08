from flask import Blueprint, request, jsonify
from app import db
from app.models import Verification, Property
import hashlib
import uuid
from datetime import datetime

verification_bp = Blueprint('verification', __name__, url_prefix='/api/v1/verifications')

@verification_bp.route('/verify/<int:property_id>', methods=['POST'])
def create_verification(property_id):
    try:
        prop = Property.query.get_or_404(property_id)
        data = request.get_json()
        
        # Simulate blockchain transaction
        transaction_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        
        existing = Verification.query.filter_by(property_id=property_id).first()
        if existing:
            return jsonify({'error': 'Property already verified'}), 409
        
        verification = Verification(
            property_id=property_id,
            transaction_hash=transaction_hash,
            block_number=int(uuid.uuid4().int % 1000000),
            owner_verified=data.get('owner_verified', False),
            documents_verified=data.get('documents_verified', False),
            verification_status='verified',
            owner_details=data.get('owner_details'),
            document_hashes=data.get('document_hashes'),
            verified_at=datetime.utcnow()
        )
        
        db.session.add(verification)
        db.session.commit()
        
        return jsonify(verification.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@verification_bp.route('<int:property_id>', methods=['GET'])
def get_verification(property_id):
    try:
        verification = Verification.query.filter_by(property_id=property_id).first()
        if not verification:
            return jsonify({'error': 'No verification found'}), 404
        return jsonify(verification.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@verification_bp.route('status/<int:property_id>', methods=['GET'])
def check_verification_status(property_id):
    try:
        verification = Verification.query.filter_by(property_id=property_id).first()
        
        if not verification:
            return jsonify({
                'property_id': property_id,
                'status': 'not_verified',
                'verified_at': None
            }), 200
        
        return jsonify({
            'property_id': property_id,
            'status': verification.verification_status,
            'owner_verified': verification.owner_verified,
            'documents_verified': verification.documents_verified,
            'transaction_hash': verification.transaction_hash,
            'block_number': verification.block_number,
            'verified_at': verification.verified_at.isoformat() if verification.verified_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@verification_bp.route('history/<int:property_id>', methods=['GET'])
def get_verification_history(property_id):
    try:
        verification = Verification.query.filter_by(property_id=property_id).first()
        
        if not verification:
            return jsonify({'data': []}), 200
        
        history = verification.verification_history or []
        
        return jsonify({
            'property_id': property_id,
            'data': history
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
