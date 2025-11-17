from flask import Blueprint, render_template, request
from app.utils.db import db
from app.utils.r2 import get_poster_url, get_thumbnail_url


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_videos(mode="home")

@main_bp.route('/browse')
def browse():
    return render_videos(mode="browse")

@main_bp.route('/popular')
def popular():
    return render_videos(mode="popular")


def render_videos(mode):
    page = request.args.get('page', 1, type=int)
    limit = 20

    videos = db.get_cached_videos()

    # Add URLs
    for v in videos:
        v['poster_url'] = get_poster_url(v.get('poster'))
        v['thumbnail_url'] = get_thumbnail_url(v.get('thumbnail'))

    # Sorting Logic
    if mode == "popular":
        videos = sorted(videos, key=lambda v: v.get("views", 0), reverse=True)
    elif mode == "browse":
        videos = sorted(videos, key=lambda v: v.get("created_at", 0), reverse=True)
    # home = default feed → no sorting or custom logic

    # In-memory pagination
    total = len(videos)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    paginated = videos[start:end]

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return render_template(
        'index.html',
        mode=mode,
        videos=paginated,
        page=page,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')
