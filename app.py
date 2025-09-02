from flask import Flask

import os




# Pages
from sample.root_page import root_page_bp
from sample.analysis_page import analysis_page_bp
from sample.result_page import result_page_bp
from sample.download_page import download_page_bp

# Utils of pages
#from sample.root_page_utils import *
#from sample.analysis_page_utils import *
#from sample.result_page_utils import *
#from sample.download_page_utils import *

# Config
from config import UPLOAD_FOLDER
from config import MAX_CONTENT_LENGTH
from config import SECRET_KEY








app = Flask(__name__)
# Enregistrement des blueprints
app.register_blueprint(root_page_bp)
app.register_blueprint(analysis_page_bp)
app.register_blueprint(result_page_bp)
app.register_blueprint(download_page_bp)



app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Check if upload folder exists

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=5000, debug=False) 
    app.run(host='0.0.0.0', port=5000)
