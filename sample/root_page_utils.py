from typing import Tuple
from werkzeug.utils import secure_filename
import os
import uuid
import json
import zipfile
import hashlib
from mimetypes import guess_type



# My eml_analyzer module
import sample.eml_parse as eml_parse

# Global variables
from config import ALLOWED_EXTENSIONS 
from config import UPLOAD_FOLDER
from config import DANGEROUS_EXT



# used by root page
def allowed_file(filename: str) -> bool:
    """This function checks if the extension is allowed."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# used by root page
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    print(f"[=] Calculating hash of file {file_path}")
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print("[!] Error in calculate_sha256 : File not found.")
        return 0
    except Exception as e:
        print(f"[!] Error in calculate_sha256 : An error occurred: {e}")
        return 0

# used by root page
def create_zip_for_attachments(email_id: str, attachment_dir: str) -> Tuple[str, list]:
    """This function creates a zip archive. It returns its path and the list of attachments."""
    zip_path = os.path.join(attachment_dir, f"{email_id}_attachments.zip")
    attachments = []
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(attachment_dir):
            for file in files:
                if file != f"{email_id}_attachments.zip":  # Exclure l'archive si elle existe déjà
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)  # Ajouter chaque fichier à l'archive
                    file_sha256 = calculate_sha256(file_path)
                    file_info = {
                        'filename': file,
                        'content_type': guess_type(file_path)[0] or 'application/octet-stream',
                        'size': os.path.getsize(file_path),
                        'sha256': file_sha256
                    }
                    attachments.append(file_info)
                    # supprimer le fichier après l'avoir ajouté à l'archive
                    os.remove(file_path) # TO DO : vérifier que le bon fichier est supprimé, qu'il n'est pas un lien symbolique, etc.
    return zip_path, attachments

# used by root page
def eml_process(filepath: str, attach_dir: str) -> dict:
    """Process the email file, get its attachments and returns its information."""
    mail_json_info = eml_parse.analyze(filepath, attach_dir)
    if isinstance(mail_json_info, str):
        mail_json_info = mail_json_info.encode('utf-8').strip()
        mail_json_info = json.loads(mail_json_info)
    return mail_json_info

# used by root page
def save_analysis_data(filename: str, stats: dict, analysis: dict) -> dict:
    """This function prepares the data to be saved."""
    analysis_data = {
        'filename': filename,
        'stats': stats,
        'full_analysis': analysis
    }
    return analysis_data

# used by root page
def write_analysis_data(analysis_data: dict, output_dir: str):
    """This function writes all the analysis datas into a json file."""
    analysis_file = os.path.join(output_dir, 'analysis.json')
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=True, indent=4)

# used by root page
def process_eml_file(filepath: str, output_dir: str, email_id: str) -> Tuple[dict, dict]:
    """Main function to process EML file and to returns its analysis information and its statistics."""
    # Analyse du fichier EML
    mail_json_info = eml_process(filepath, output_dir)
    
    # Création de l'archive ZIP pour les pièces jointes
    zip_path, attachments = create_zip_for_attachments(email_id, output_dir)
    
    # Mise à jour des informations avec les pièces jointes
    mail_json_info['attachments'] = attachments
    mail_json_info['zip_file'] = os.path.basename(zip_path)
    
    # Extraction des statistiques rapides
    stats = extract_quick_stats(mail_json_info)
    
    return mail_json_info, stats

# used by root page
def process_uploaded_file(file, email_ids: dict, session_upload_folder: str):
    """This function processes a file uploaded by a user."""
    secured_filename = secure_filename(file.filename)
    print(secured_filename)
    if secured_filename and allowed_file(secured_filename):
        # Enregistrer l'email
        filepath = os.path.join(session_upload_folder, secured_filename)
        file.save(filepath)
        
        # Initialiser les variables
        email_id = str(uuid.uuid4())
        email_ids[email_id] = 0  # Initialiser le niveau de suspicion
        
        output_dir = os.path.join(UPLOAD_FOLDER, email_id)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Traiter le fichier EML
            mail_json_info, stats = process_eml_file(filepath, output_dir, email_id)
            
            # Mettre à jour le niveau de suspicion
            email_ids[email_id] = stats.get("is_suspicious", 0)
            
            # Préparer et sauvegarder les données d'analyse
            analysis_data = save_analysis_data(secured_filename, stats, mail_json_info)
            write_analysis_data(analysis_data, output_dir)
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de {secured_filename}: {e}")


# used by root page
def extract_quick_stats(mail_json_info: dict) -> dict:
    """Extrait des statistiques rapides de l'analyse."""
    stats = {}
    
    # Nombre de pièces jointes
    stats['attachments_count'] = len(mail_json_info.get("attachments", []))
    
    # Déterminer si l'email est suspect
    stats['is_suspicious'] = detect_suspicious(mail_json_info)
    
    return stats

# used by root page
def detect_suspicious(mail_json_info: dict) -> int:
    """Détermine le niveau de suspicion de l'email."""
    suspicious = 0
    
    # Vérifier que les adresses de sender et de réponse sont les mêmes
    if is_return_path_mismatch(mail_json_info):
        suspicious += 1
    
    # Vérifier les URLs intégrées
    if has_embedded_urls(mail_json_info):
        suspicious += 2
    
    # Vérifier les pièces jointes dangereuses
    if has_dangerous_attachments(mail_json_info):
        suspicious += 4
    
    print("Is it suspicious ? -> ", suspicious)
    return suspicious

# Sous-fonctions de detect_suspicious

# used by root page
def is_return_path_mismatch(mail_json_info: dict) -> bool:
    """Vérifie si le Return-Path est différent du From."""
    from_header = mail_json_info.get('headers', {}).get('From', [''])[0]
    return_path_header = mail_json_info.get('headers', {}).get('Return-Path', [''])[0]
    if return_path_header not in from_header:
        return True
    return False

# used by root page
def has_embedded_urls(mail_json_info: dict) -> bool:
    """Vérifie si l'email contient des URLs intégrées."""
    urls = mail_json_info.get('urls', [])
    print("Récupération des URLs")
    return bool(urls)

# used by root page
def has_dangerous_attachments(mail_json_info: dict) -> bool:
    """Vérifie si l'email contient des pièces jointes dangereuses."""
    attachments = mail_json_info.get('attachments', [])
    print("Récupération des pièces jointes")
    for attachment in attachments:
        print("Récupération des noms de fichiers des pièces jointes")
        filename = attachment.get('filename', '')
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            print("Extension :", ext)
            if ext in DANGEROUS_EXT:
                return True
    return False