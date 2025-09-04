from flask import Blueprint, render_template
from flask import render_template, session
import os
import json

# import the render_suspicious function from the analysis_page_utils.py file
from sample.result_page_utils import *
# import the UPLOAD_FOLDER variable from the config.py file
from config import UPLOAD_FOLDER

result_page_bp = Blueprint('result_page_bp', __name__)

@result_page_bp.route('/results')
def results():
    mode = session.get('mode')
    print("mode : ",mode)
    email_ids = session.get('email_ids', [])
    analysis_data = {}
    
    for email_id in email_ids:
        analysis_file = os.path.join(UPLOAD_FOLDER, email_id, 'analysis.json')
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Si on est en mode Threat, on rajoute la partie suspicieuse
                if mode == "Threat":
                    data['stats']['susp_render'] = render_suspicious(data['stats']['is_suspicious'])

                analysis_data[email_id] = data

    # Rendu en fonction du mode
    rendered_html = ""
    if mode == "Threat":
        rendered_html = render_threat_mode(analysis_data)
    elif mode == "Analyst":
        rendered_html = render_analyst_mode(analysis_data)
    else:
        rendered_html = "<p>Mode inconnu</p>"

    return render_template('results.html', rendered_html=rendered_html)

