from flask import Blueprint, jsonify, request
from app.utils.db import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/like/<uuid>', methods=['POST'])
def like_video(uuid):
    """Increment likes for a video"""
    try:
        # Increment likes in database
        new_likes = db.increment_likes(uuid)
        
        return jsonify({
            'success': True,
            'likes': new_likes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500