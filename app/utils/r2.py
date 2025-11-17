from app.config import Config
import os
import hmac
import hashlib
import time
from urllib.parse import quote, urlencode
from flask import current_app   

CLOUDFLARE_WORKER_URL = os.getenv("CLOUDFLARE_WORKER_URL")
CF_SECRET_KEY = os.getenv("CF_SECRET_KEY")
CF_TOKEN_EXPIRY = int(os.getenv("CF_TOKEN_EXPIRY", 3600))  # in seconds


def get_video_url(filename, expiration=None):
    """
    Generate an expiring signed URL for Cloudflare Worker video access.
    Allows custom expiration override (in seconds).
    """
    try:
        if not filename:
            raise ValueError("Empty filename provided")

        safe_filename = quote(filename.strip())
        expiry_seconds = expiration or CF_TOKEN_EXPIRY
        expires = int(time.time()) + expiry_seconds

        data_to_sign = f"{safe_filename}:{expires}"
        signature = hmac.new(
            CF_SECRET_KEY.encode(),
            data_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()

        params = urlencode({
            "expires": expires,
            "token": signature
        })

        signed_url = f"{CLOUDFLARE_WORKER_URL}/videos/{safe_filename}?{params}"
        return signed_url

    except Exception as e:
        current_app.logger.error(f"Error signing URL for {filename}: {e}")  # FIXED
        return None


def get_thumbnail_url(filename):
    if not filename:
        return None
    return f"{filename}"


def get_poster_url(filename):
    if not filename:
        return None
    return f"{filename}"
