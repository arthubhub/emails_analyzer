from flask import Blueprint, render_template
import os
import json

# import the render_analysis_html function from the analysis_page_utils.py file
from sample.analysis_page_utils import render_analysis_html
# import the UPLOAD_FOLDER variable from the config.py file
from config import UPLOAD_FOLDER

analysis_page_bp = Blueprint('analysis_page', __name__)

@analysis_page_bp.route('/analysis/<email_id>')
def show_analysis(email_id):
    """Affiche l'analyse détaillée pour un email spécifique."""
    analysis_dir = os.path.join(UPLOAD_FOLDER, email_id)
    analysis_file = os.path.join(analysis_dir, 'analysis.json')
    
    if os.path.exists(analysis_file):
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        analysis = analysis_data['full_analysis']
        filename = analysis_data['filename']
        formatted_analysis = render_analysis_html(analysis, email_id)
        return render_template('analysis.html', analysis=formatted_analysis, filename=filename)
    else:
        return "Analyse non trouvée.", 404