import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------------------------------
    # CORS (allow API requests)
    # ---------------------------------------
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ---------------------------------------
    # Logging (file + console)
    # ---------------------------------------
    setup_logging(app)

    # ---------------------------------------
    # Register Jinja Filters
    # ---------------------------------------
    register_jinja_filters(app)

    # ---------------------------------------
    # Register Blueprints
    # ---------------------------------------
    register_blueprints(app)

    # ---------------------------------------
    # Error Handlers
    # ---------------------------------------
    register_error_handlers(app)

    # ---------------------------------------
    # Security Headers + Cache Control
    # ---------------------------------------
    @app.after_request
    def add_security_headers(response):
        # Security
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Cache control for dynamic routes
        if request.path.startswith("/video") or request.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store"
        return response

    return app


# ============================================================
# 📌 REGISTER BLUEPRINTS
# ============================================================

def register_blueprints(app):
    # Core routes
    from app.routes.main import main_bp
    from app.routes.video import video_bp
    from app.routes.related import related_bp

    # API
    from app.routes.api import api_bp

    # SEO
    from app.routes.sitemap import sitemap_bp
    from app.routes.feeds import feeds_bp
    from app.routes.robots import robots_bp

    # Register all
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(related_bp)

    app.register_blueprint(api_bp, url_prefix="/api")

    app.register_blueprint(sitemap_bp)
    app.register_blueprint(feeds_bp)
    app.register_blueprint(robots_bp)


# ============================================================
# 📌 LOGGING SETUP
# ============================================================

def setup_logging(app):
    log_level = logging.DEBUG if app.debug else logging.INFO
    app.logger.setLevel(log_level)

    # Console logging only
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    app.logger.addHandler(console_handler)

   


# ============================================================
# 📌 JINJA FILTERS
# ============================================================

def register_jinja_filters(app):
    @app.template_filter("number_format")
    def number_format(value):
        """Format numbers like 1500 -> 1.5K"""
        try:
            value = int(value)
            if value >= 1_000_000:
                return f"{value/1_000_000:.1f}M"
            if value >= 1_000:
                return f"{value/1_000:.1f}K"
            return str(value)
        except:
            return value

    @app.template_filter("datetime_format")
    def datetime_format(ts):
        """Format timestamps to readable format."""
        from datetime import datetime
        try:
            return datetime.utcfromtimestamp(ts).strftime("%d %b %Y")
        except:
            return ts


# ============================================================
# 📌 ERROR HANDLERS
# ============================================================

def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template(
            "error.html",
            error_code=404,
            error_message="The page you are looking for does not exist."
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template(
            "error.html",
            error_code=500,
            error_message="Something went wrong on our side. Please try again later."
        ), 500
