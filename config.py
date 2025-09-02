#this script contains GLOBAL variables
from yaml import safe_load


# Load the configuration
def load_config(filename: str = "config_template.yml") -> dict:
    with open(filename, "r") as f:
        return safe_load(f)

config = load_config("config_template.yml")

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = config["flask"]["secret_key"]
MAX_CONTENT_LENGTH = config["flask"]["max_content_length"]  # max 64 MB par upload
DANGEROUS_EXT = config["dangerous_extensions"]  # Define the dangerous extensions
ALLOWED_EXTENSIONS = {'.eml'}  # Define the valid email extensions 