from flask import Blueprint, render_template
from flask import render_template, session
import os
import json

# import the render_suspicious function from the analysis_page_utils.py file
from sample.result_page_utils import render_suspicious
# import the UPLOAD_FOLDER variable from the config.py file
from config import UPLOAD_FOLDER

result_page_bp = Blueprint('result_page_bp', __name__)

@result_page_bp.route('/results')
def results():
    """Affiche les résultats de l'analyse pour tous les emails uploadés."""
    email_ids = session.get('email_ids', [])
    analysis_data = {}
    
    for email_id in email_ids:
        analysis_file = os.path.join(UPLOAD_FOLDER, email_id, 'analysis.json')
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis_data[email_id] = json.load(f)
                analysis_data[email_id]['stats']['susp_render'] = render_suspicious(analysis_data[email_id]['stats']['is_suspicious'])

    return render_template('results.html', email_ids=email_ids, analysis_data=analysis_data)

