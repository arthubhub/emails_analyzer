from flask import Blueprint, request, render_template
from flask import session, redirect, url_for
import os
import uuid
import shutil

# import the process_uploaded_file function from the sample.root_page_utils.py file
from sample.root_page_utils import process_uploaded_file
# import the UPLOAD_FOLDER variable from the config.py file
from config import UPLOAD_FOLDER


root_page_bp = Blueprint('root_page', __name__)

@root_page_bp.route('/', methods=['GET', 'POST'])
def upload_files():
    """This function manage the eml file downloaded by the users."""
    if request.method == 'POST':
        # Variables de la session et des fichiers
        session_id = str(uuid.uuid4())
        session_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
        os.makedirs(session_upload_folder, exist_ok=True)
        files = request.files.getlist('files')
        email_ids = {}
        # Traiter chaque fichier
        for file in files:
            process_uploaded_file(file, email_ids, session_upload_folder)
        shutil.rmtree(session_upload_folder)
        # Trier les emails par niveau de suspicion
        sorted_email_ids = sorted(email_ids, key=lambda email_id: email_ids[email_id], reverse=True)
        session['email_ids'] = sorted_email_ids
        return redirect(url_for('result_page_bp.results'))
    
    return render_template('upload.html')
