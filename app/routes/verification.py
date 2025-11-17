from flask import Blueprint, send_from_directory, abort
import os

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/<filename>')
def serve_verification_file(filename):
    # Only allow .html or .txt files
    if not (filename.endswith('.html') or filename.endswith('.txt')):
        abort(404)

    # Path to the verification folder at the project root
    verification_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'verification')
    file_path = os.path.join(verification_dir, filename)

    if os.path.isfile(file_path):
        return send_from_directory(verification_dir, filename)
    else:
        abort(404)
