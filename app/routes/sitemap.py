from flask import Blueprint, Response, url_for
from app.utils.db import db
from datetime import datetime

sitemap_bp = Blueprint("sitemap", __name__)

BASE_URL = "https://dirtytube.site"   


def format_date(ts):
    """Convert timestamp/string to Google-friendly lastmod format."""
    try:
        if isinstance(ts, (int, float)):
            return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
        if isinstance(ts, str):
            return ts.split("T")[0]  # handle ISO-like strings
    except:
        pass
    return datetime.utcnow().strftime("%Y-%m-%d")


@sitemap_bp.route("/sitemap.xml")
def sitemap_index():
    """Main sitemap index pointing to sub-sitemaps."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <sitemap>
        <loc>{BASE_URL}/sitemap-static.xml</loc>
    </sitemap>

    <sitemap>
        <loc>{BASE_URL}/sitemap-videos.xml</loc>
    </sitemap>

</sitemapindex>
"""
    return Response(xml, mimetype="application/xml")


@sitemap_bp.route("/sitemap-static.xml")
def sitemap_static():
    """Sitemap for static + browsing pages."""
    pages = [
        {"loc": BASE_URL + "/", "priority": "1.0", "freq": "daily"},
        {"loc": BASE_URL + "/browse", "priority": "0.8", "freq": "daily"},
        {"loc": BASE_URL + "/popular", "priority": "0.8", "freq": "daily"},
        {"loc": BASE_URL + "/about", "priority": "0.5", "freq": "yearly"},
        {"loc": BASE_URL + "/contact", "priority": "0.5", "freq": "yearly"},
    ]

    xml_items = ""
    today = datetime.utcnow().strftime("%Y-%m-%d")

    for p in pages:
        xml_items += f"""
    <url>
        <loc>{p['loc']}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{p['freq']}</changefreq>
        <priority>{p['priority']}</priority>
    </url>
"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>"""

    return Response(xml, mimetype="application/xml")


@sitemap_bp.route("/sitemap-videos.xml")
def sitemap_videos():
    """Dynamic sitemap for ALL videos."""

    videos = db.get_all_videos()
    xml_items = ""

    for v in videos:
        uuid = v.get("uuid")
        created = v.get("created_at") or v.get("upload_date")
        lastmod = format_date(created)

        xml_items += f"""
    <url>
        <loc>{BASE_URL}/video/{uuid}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>"""

    return Response(xml, mimetype="application/xml")
