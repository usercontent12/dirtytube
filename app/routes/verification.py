from flask import Blueprint, send_from_directory, abort
import os
import re

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/<path:filename>')
def serve_verification_file(filename):
    f = filename.lower()

    #  Reject ANY sitemap file (sitemap.xml, sitemap-1.xml, sitemap-video.xml, etc.)
    if re.match(r"^sitemap.*\.xml$", f):
        abort(404)

    #  Reject robots.txt (has its own dedicated route)
    if f == "robots.txt":
        abort(404)

    #  Allow only files used for verification
    allowed_extensions = ('.html', '.txt', '.xml')

    if not f.endswith(allowed_extensions):
        abort(404)

    #  Directory where verification files live
    verification_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'verification'
    )

    file_path = os.path.join(verification_dir, filename)

    if os.path.isfile(file_path):
        return send_from_directory(verification_dir, filename)

    abort(404)
