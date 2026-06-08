from flask import Blueprint, request, jsonify
from app import db
from app.models import FraudReport, Property

fraud_bp = Blueprint('fraud', __name__, url_prefix='/api/v1/fraud')

@fraud_bp.route('/detect/<int:property_id>', methods=['POST'])
def detect_fraud(property_id):
    try:
        prop = Property.query.get_or_404(property_id)
        
        # Simulate fraud detection
        fraud_score = 0.35
        risk_level = 'low'
        reasons = []
        
        # Check for suspicious patterns
        if prop.price < 50000:
            fraud_score += 0.15
            reasons.append('Unusually low price compared to market')
        
        if prop.price > 10000000:
            fraud_score += 0.1
            reasons.append('Unusually high price')
        
        if not prop.description or len(prop.description) < 50:
            fraud_score += 0.1
            reasons.append('Incomplete property description')
        
        if len(prop.images) == 0:
            fraud_score += 0.15
            reasons.append('No property images provided')
        
        # Determine risk level
        if fraud_score > 0.7:
            risk_level = 'high'
        elif fraud_score > 0.4:
            risk_level = 'medium'
        
        # Check for existing report
        existing_report = FraudReport.query.filter_by(property_id=property_id).first()
        if existing_report:
            existing_report.fraud_score = fraud_score
            existing_report.risk_level = risk_level
            existing_report.reasons = reasons
            db.session.commit()
            return jsonify(existing_report.to_dict()), 200
        
        fraud_report = FraudReport(
            property_id=property_id,
            fraud_score=fraud_score,
            risk_level=risk_level,
            reasons=reasons
        )
        
        db.session.add(fraud_report)
        db.session.commit()
        
        return jsonify(fraud_report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fraud_bp.route('<int:property_id>', methods=['GET'])
def get_fraud_report(property_id):
    try:
        report = FraudReport.query.filter_by(property_id=property_id).first()
        if not report:
            return jsonify({'error': 'No fraud report found'}), 404
        return jsonify(report.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fraud_bp.route('high-risk', methods=['GET'])
def get_high_risk_properties():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        reports = FraudReport.query.filter_by(risk_level='high').paginate(page=page, per_page=per_page)
        
        return jsonify({
            'data': [report.to_dict() for report in reports.items],
            'pagination': {'page': page, 'per_page': per_page, 'total': reports.total}
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
