from flask import Blueprint, Response

robots_bp = Blueprint("robots", __name__)

BASE_URL = "https://dirtytube.site"  # Replace


@robots_bp.route("/robots.txt")
def robots():
    txt = f"""User-agent: *
Disallow:

Sitemap: {BASE_URL}/sitemap.xml
Sitemap: {BASE_URL}/rss.xml
Sitemap: {BASE_URL}/atom.xml
"""
    return Response(txt, mimetype="text/plain")
