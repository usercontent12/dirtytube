from flask import Blueprint, render_template, abort
from app.utils.db import db
from app.utils.r2 import get_video_url, get_poster_url, get_thumbnail_url
from app.utils.time import seconds_to_iso8601

video_bp = Blueprint('video', __name__)

 
@video_bp.route('/video/<uuid>')
def video_detail(uuid):
    """Video detail page"""
    video = db.get_video_by_uuid(uuid)
    
    if not video:
        abort(404)

    # Increment views
    db.increment_views(uuid)

    # Full URLs
    video['video_url'] = get_video_url(video['video_src'])
    video['poster_url'] = get_poster_url(video['poster'])
    video['thumbnail_url'] = get_thumbnail_url(video['thumbnail'])

    # Updated views after increment
    video['views'] = (video.get('views') or 0) + 1

    # ISO duration for schema.org
    video['duration_iso'] = seconds_to_iso8601(video.get('duration'))

    # Embed URL
    video['embed_url'] = f"https://dirtytube.site/embed/{uuid}"

    # File size (in bytes)
    video['file_size'] = video.get('file_size')  # Should exist in DB

    return render_template('video.html', video=video)
