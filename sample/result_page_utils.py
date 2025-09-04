
import requests

def get_final_url(shortened_url): # this function purpose is to resolve the shortened URL to its final destination
    try:
        response = requests.head(shortened_url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Error resolving URL: {e}")
        return None

# used by result page
def render_suspicious(is_suspicious) -> str:
    elements = []
    if is_suspicious & 1:
        elements.append({
            'image': 'images/reply_to.png',
            'message': 'Votre email a une adresse reply to différente du sender.'
        })
    if is_suspicious & 2:
        elements.append({
            'image': 'images/susp_urls.png',
            'message': 'Votre email contient des URLs. Ces URLs peuvent être malveillantes.'
        })
    if is_suspicious & 4:
        elements.append({
            'image': 'images/susp_attachment.png',
            'message': 'Votre email contient des pièces jointes potentiellement malveillantes.'
        })
    return elements



from flask import url_for

def render_threat_mode(analysis_data):
    """
    Prend l'analysis_data (data pour tous les emails) et renvoie une chaîne HTML 
    avec tous les blocs rendus pour le mode Threat.
    """
    rendered_html = ""

    for email_id, data in analysis_data.items():
        susp_part = ""
        if len(data['stats']['susp_render']) == 0:
            susp_part = "<p>0 : Votre email n'a pas été détecté comme suspect. Vous devriez analyser son contenu texte.</p>"
        else:
            for susp_rend in data['stats']['susp_render']:
                susp_part += f"""
                <div class="suspicious-item">
                    <img src="{ url_for('static', filename=susp_rend['image']) }" alt="suspiciousitem">
                    <span>{ susp_rend['message'] }</span>
                </div>
                """

        block_html = f"""
        <div class="email-result">
            <h3>{data['filename']}</h3>
            <p><strong>Nombre de pièces jointes :</strong> {data['stats']['attachments_count']}</p>
            <div>
                <p><strong>Email suspect :</strong> {data['stats']['is_suspicious']}</p>
                {susp_part}
            </div>
            <a href="{url_for('analysis_page.show_analysis', email_id=email_id)}">
                <button>Voir l'analyse complète</button>
            </a>
        </div>
        """
        rendered_html += block_html

    return rendered_html
def render_analyst_mode(analysis_data):
    """
    Génère un rendu HTML épuré pour le mode Analyst.
    """
    rendered_html = ""

    for email_id, data in analysis_data.items():
        headers = data['full_analysis']['headers']
        urls = data['full_analysis'].get('urls', [])
        for i in range(len(urls)):
            urls[i]=urls[i].replace('<','')

        
        attachments = data['full_analysis'].get('attachments', [])

        # Récupération des champs avec gestion d'absence
        sender_ip = headers.get('X-Sender-IP', [None])[0]
        sender_email = headers.get('From', [None])[0]
        return_path = headers.get('Return-Path', [None])[0]
        reply_to = headers.get('Reply-To', [None])[0]
        dest_email = headers.get('To', [None])[0]
        email_cc = headers.get('Cc', [None])[0]
        email_bcc = headers.get('Bcc', [None])[0]
        subject = headers.get('Subject', [None])[0]
        email_date = headers.get('Date', [None])[0]

        # Nombre d'URLs et de pièces jointes
        email_urls_count = len(urls) if urls else 0
        email_attach_count = len(attachments) if attachments else 0

        # Liens pour l'IP (AbuseIPDB et VirusTotal)
        ip_abuse_link = f"https://www.abuseipdb.com/check/{sender_ip}" if sender_ip else "#"
        ip_virustotal_link = f"https://www.virustotal.com/gui/ip-address/{sender_ip}" if sender_ip else "#"

        # Section des URLs
        urls_section = ""
        if email_urls_count > 0:
            urls_section = "<ul>"
            for u in urls:
                urls_section += f"<li>{u}</li>"
            urls_section += "</ul>"
        else:
            urls_section = "<p>Aucune URL trouvée.</p>"

        # Section des pièces jointes
        attachments_section = ""
        if email_attach_count > 0:
            attachments_section = "<table style='border-collapse: collapse; width:100%;'>"
            attachments_section += "<tr>\
                <th style='text-align:left; border-bottom:1px solid #ccc;'>Nom</th>\
                <th style='text-align:left; border-bottom:1px solid #ccc;'>Type</th>\
                <th style='text-align:left; border-bottom:1px solid #ccc;'>Taille</th>\
                <th style='text-align:left; border-bottom:1px solid #ccc;'>Hash (SHA256)</th>\
                <th style='text-align:left; border-bottom:1px solid #ccc;'>VirusTotal</th></tr>"
            for att in attachments:
                vt_hash_link = f"https://www.virustotal.com/gui/file/{att['sha256']}"
                attachments_section += f"<tr><td>{att['filename']}</td><td>{att['content_type']}</td><td>{att['size']} bytes</td><td style='font-size:0.9em;'>{att['sha256']}</td><td><a href='{vt_hash_link}' target='_blank'>Analyser</a></td></tr>"
            attachments_section += "</table>"
        else:
            attachments_section = "<p>Aucune pièce jointe trouvée.</p>"

        # Lien pour le reverse lookup
        reverse_lookup_link = f"https://mxtoolbox.com/SuperTool.aspx?action=ptr%3a{sender_ip}&run=toolpage" if sender_ip else "#"

        # Bloc HTML
        block_html = f"""
        <div class="email-result" style="border:1px solid #ddd; padding:20px; margin-bottom:20px; border-radius:5px; background:#fafafa;">
            <h2 style="margin-top:0;">{data['filename']}</h2>
            <h3 style="margin-bottom:10px;">{subject if subject else 'Pas de sujet'}</h3>
            
            <p><strong>Date :</strong> {email_date if email_date else 'N/A'}</p>
            <p><strong>Expéditeur :</strong> {sender_email if sender_email else 'N/A'} 
                {f"(Return-Path: {return_path})" if return_path else ''}</p>
            
            <p><strong>Adresse IP de l'expéditeur :</strong> {sender_ip if sender_ip else 'N/A'} 
               {f"<a href='{ip_abuse_link}' target='_blank'>[AbuseIPDB]</a>" if sender_ip else ''}
               {f"<a href='{ip_virustotal_link}' target='_blank'>[VirusTotal]</a>" if sender_ip else ''}</p>
            <p><strong>Reverse Lookup IP:</strong> {f"<a href='{reverse_lookup_link}' target='_blank'>Reverse Lookup</a>" if sender_ip else 'N/A'}</p>
            
            <p><strong>Reply-To :</strong> {reply_to if reply_to else 'N/A'}</p>
            
            <hr style="margin:20px 0;"/>
            <p><strong>Destinataires :</strong></p>
            <ul style="list-style:none; padding:0; margin:0;">
                <li><strong>To :</strong> {dest_email if dest_email else 'N/A'}</li>
                <li><strong>Cc :</strong> {email_cc if email_cc else 'N/A'}</li>
                <li><strong>Bcc :</strong> {email_bcc if email_bcc else 'N/A'}</li>
            </ul>
            
            <hr style="margin:20px 0;"/>
            <h4>URLs ( {email_urls_count} )</h4>
            {urls_section}
            <hr style="margin:20px 0;"/>
            <h4>Pièces Jointes ( {email_attach_count} )</h4>
            {attachments_section}
        </div>
        """
        rendered_html += block_html

    return rendered_html