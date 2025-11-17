from flask import Blueprint, Response
from app.utils.db import db
from app.utils.r2 import get_video_url, get_thumbnail_url
from datetime import datetime
import html

feeds_bp = Blueprint("feeds", __name__)

BASE_URL = "https://dirtytube.site"  # Replace with your domain


def iso_date(ts):
    """Convert timestamp to ISO 8601."""
    try:
        if isinstance(ts, (int, float)):
            return datetime.utcfromtimestamp(ts).isoformat() + "Z"
        if isinstance(ts, str):
            return ts
    except:
        pass
    return datetime.utcnow().isoformat() + "Z"


# -----------------------------------------
# RSS 2.0 FEED
# -----------------------------------------

@feeds_bp.route("/rss.xml")
def rss_feed():
    videos = db.get_all_videos()

    xml_items = ""
    for v in videos:
        uuid = v.get("uuid")
        link = f"{BASE_URL}/video/{uuid}"
        title = html.escape(v.get("title", "Video"))
        description = html.escape(v.get("description", "Video content"))
        pub_date = iso_date(v.get("created_at") or v.get("upload_date"))
        thumbnail = get_thumbnail_url(v.get("thumbnail"))

        xml_items += f"""
    <item>
        <title>{title}</title>
        <link>{link}</link>
        <guid>{uuid}</guid>
        <pubDate>{pub_date}</pubDate>
        <description>{description}</description>
        <enclosure url="{thumbnail}" type="image/jpeg"/>
    </item>
"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>YourSite Videos</title>
    <link>{BASE_URL}</link>
    <description>Latest video uploads</description>
    <language>en</language>
{xml_items}
</channel>
</rss>
"""

    return Response(xml, mimetype="application/xml")


# -----------------------------------------
# ATOM FEED
# -----------------------------------------

@feeds_bp.route("/atom.xml")
def atom_feed():
    videos = db.get_all_videos()

    updated = iso_date(datetime.utcnow().timestamp())

    xml_entries = ""

    for v in videos:
        uuid = v.get("uuid")
        video_link = f"{BASE_URL}/video/{uuid}"
        created = iso_date(v.get("created_at") or v.get("upload_date"))
        title = html.escape(v.get("title", "Video"))
        summary = html.escape(v.get("description", "Video content"))
        thumbnail = get_thumbnail_url(v.get("thumbnail"))

        xml_entries += f"""
    <entry>
        <id>{video_link}</id>
        <title>{title}</title>
        <link href="{video_link}"/>
        <updated>{created}</updated>
        <summary>{summary}</summary>
        <content type="html">
            <![CDATA[
                <img src="{thumbnail}" alt="{title}">
            ]]>
        </content>
    </entry>
"""

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>YourSite – Latest Videos</title>
    <link href="{BASE_URL}"/>
    <updated>{updated}</updated>
    <id>{BASE_URL}/atom.xml</id>
{xml_entries}
</feed>
"""

    return Response(xml, mimetype="application/atom+xml")
