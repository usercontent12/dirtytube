from flask import Blueprint, request, jsonify
from app.utils.db import db
from app.utils.r2 import get_thumbnail_url


related_bp = Blueprint('related_bp', __name__)

@related_bp.route('/related/<uuid>')
def related_videos(uuid):
    """Return paginated random related videos"""
    try:
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 6))  # front-end loads 6 each time
    except:
        offset = 0
        limit = 6

    videos = db.get_random_videos(uuid, limit=limit, offset=offset)

    # Add URLs for thumbnails
    for v in videos:
        v['thumbnail_url'] = get_thumbnail_url(v.get('thumbnail'))
        v['video_page'] = f"/video/{v.get('uuid')}"

    return jsonify({
        "success": True,
        "videos": videos
    })
