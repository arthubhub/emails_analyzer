from flask import Blueprint, send_file
from flask import Response
import os

# import the UPLOAD_FOLDER variable from the config.py file
from config import UPLOAD_FOLDER

download_page_bp = Blueprint('download_page_bp', __name__)

@download_page_bp.route('/download/<email_id>/attachments.zip')
def download_attachment_zip(email_id: str) -> Response:
    """Permet de télécharger l'archive ZIP des pièces jointes."""
    attachment_dir = os.path.join(UPLOAD_FOLDER, email_id)
    zip_path = os.path.join(attachment_dir, f"{email_id}_attachments.zip")
    
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name=f"{email_id}_attachments.zip")
    else:
        return "Archive introuvable.", 404