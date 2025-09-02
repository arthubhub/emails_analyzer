from flask import  url_for
from markupsafe import escape




# Les fonctions suivantes sont des sous-fonctions de render_analysis_html
# used by analysis/id page
def render_analysis_html(analysis, email_id):
    """Main function to generate the complete HTML for email analysis."""
    # JavaScript for toggling visibility of sections
    html_output = render_toggle_script()

    # Render each main section of the email analysis
    html_output += render_headers_section(analysis)
    html_output += render_structure_section(analysis)
    html_output += render_urls_section(analysis)
    html_output += render_external_content_section(analysis)
    html_output += render_attachments_section(analysis, email_id)
    html_output += render_text_section(analysis)
    html_output += render_html_section(analysis)
    
    return html_output


# used by analysis/id page
def render_toggle_script() -> str:
    """Returns JavaScript code for toggling section visibility."""
    return '''
    <script>
        function toggleVisibility(id) {
            var section = document.getElementById(id);
            section.classList.toggle('open');
            var content = section.querySelector('.section-content');

            // Utilisez getComputedStyle pour vérifier le style réel
            if (getComputedStyle(content).display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        }
    </script>

    '''


# used by analysis/id page
def render_headers_section(analysis) -> str:
    """Generates HTML for the headers section, with subcategories."""
    html = '<div id="section_headers" class="section">'
    html += '<h2 onclick="toggleVisibility(\'section_headers\')">En-têtes</h2>'
    html += '<div class="section-content">'

    header_categories = {
        'Relais et adresses IP': ['Received', 'X-Originating-IP', 'X-Sender-IP'],
        'Authentification et filtrage': [
            'Authentication-Results', 'Received-SPF', 'DKIM-Signature', 'DomainKey-Signature',
            'ARC-Authentication-Results', 'ARC-Message-Signature', 'ARC-Seal'],
        'Expéditeur et destinataire': ['From', 'To', 'Reply-To', 'Cc', 'Bcc'],
        'Sujet et date': ['Subject', 'Date'],
        'Anti-spam et sécurité': [
            'X-Spam-Status', 'X-Spam-Score', 'X-Spam-Flag', 'X-Virus-Scanned', 
            'X-Microsoft-Antispam', 'X-MS-Exchange-Organization-SCL', 'X-MS-Exchange-Organization-PCL', 
            'X-MS-Exchange-Organization-AuthAs'],
        'Autres métadonnées': ['Message-ID', 'Content-Type', 'MIME-Version', 'List-Unsubscribe', 'Feedback-ID', 'Content-Transfer-Encoding']
    }

    for category, headers_list in header_categories.items():
        html += render_header_category(analysis, category, headers_list)

    html += render_other_headers(analysis, header_categories)
    html += '</div></div>'
    return html


# used by analysis/id page
def render_header_category(analysis, category: str, headers_list: list) -> str:
    """Renders a specific header category and its content."""
    category_id = f'section_{category.replace(" ", "_")}'
    html = f'<div id="{category_id}" class="section">'
    html += f'<h3 onclick="toggleVisibility(\'{category_id}\')">{escape(category)}</h3>'
    html += '<div class="section-content"><ul>'
    for header in headers_list:
        if header == "X-Sender-IP":
            values = analysis.get('headers', {}).get(header, [])
            for value in values:
                html += f'\
                    <li><strong>{escape(header)}</strong>: {escape(value)}\
                        <a href="https://www.virustotal.com/gui/ip-address/{value}" target="_blank" rel="noopener noreferrer">\
                            <button>See on VT</button>\
                        </a>\
                        <a href="https://www.talosintelligence.com/reputation_center/lookup?search={value}" target="_blank" rel="noopener noreferrer">\
                            <button>See on TalosIntelligence</button>\
                        </a>\
                    </li>'

        else :
            values = analysis.get('headers', {}).get(header, [])
            for value in values:
                html += f'<li><strong>{escape(header)}</strong>: {escape(value)}</li>'

    html += '</ul></div></div>'
    return html


# used by analysis/id page
def render_other_headers(analysis, header_categories: dict) -> str:
    """Renders any headers not included in the predefined categories."""
    other_headers = set(analysis.get('headers', {}).keys()) - set(sum(header_categories.values(), []))
    if not other_headers:
        return ''

    html = '<div class="section">'
    html += '<h3 onclick="toggleVisibility(\'section_Other_Headers\')">Autres en-têtes</h3>'
    html += '<div id="section_Other_Headers" class="section-content"><ul>'
    for header in other_headers:
        values = analysis.get('headers', {}).get(header, [])
        for value in values:
            html += f'<li><strong>{escape(header)}</strong>: {escape(value)}</li>'
    html += '</ul></div></div>'
    return html


# used by analysis/id page
def render_structure_section(analysis) -> str:
    """Generates HTML for the structure section."""
    html = '<div id="section_structure" class="section">'
    html += '<h2 onclick="toggleVisibility(\'section_structure\')">Structure</h2>'
    html += '<div class="section-content">'
    html += render_structure(analysis.get('structure', {}))
    html += '</div></div>'
    return html


# used by analysis/id page
def render_structure(structure: dict) -> str:
    """Recursively renders the structure of the email."""
    html = '<ul>'
    html += f'<li><strong>Type:</strong> {escape(structure.get("type", "N/A"))}</li>'
    children = structure.get("children", [])
    if children:
        html += '<li><strong>Enfants:</strong>'
        for child in children:
            html += render_structure(child)  # Recursive call for each child
        html += '</li>'
    html += '</ul>'
    return html


# used by analysis/id page
def render_urls_section(analysis) -> str:
    """Generates HTML for the embedded URLs section."""
    urls = analysis.get('urls', [])
    html = '<div id="section_urls" class="section">'
    html += '<h2 onclick="toggleVisibility(\'section_urls\')">URLs intégrées'
    url_count=len(urls)
    if url_count:
            
            if url_count <= 5:
                img_src = url_for('static', filename=f'images/{url_count}.png')
            else:
                img_src = url_for('static', filename='images/more.png')
            html += f'<img style="display:inline-block" src="{img_src}">'
    html+='</h2>'
    html += '<div class="section-content">'


    
    if urls:
        html += '<ul>'
        for url in urls:
            html += f'<li><a href="{escape(url)}" target="_blank">{escape(url)}</a></li>'
        html += '</ul>'
    else:
        html += '<p>Aucune URL trouvée.</p>'
    html += '</div></div>'
    return html


# used by analysis/id page
def render_external_content_section(analysis) -> str:
    """Generates HTML for the external content section."""
    html = '<div id="section_external_content" class="section">'
    html += '<h2 onclick="toggleVisibility(\'section_external_content\')">Contenu externe</h2>'
    html += '<div class="section-content">'
    external_content = analysis.get('reloaded_content', [])
    if external_content:
        html += '<ul>'
        for content in external_content:
            html += f'<li>{escape(content)}</li>'
        html += '</ul>'
    else:
        html += '<p>Aucun contenu externe trouvé.</p>'
    html += '</div></div>'
    return html


# used by analysis/id page
def render_attachments_section(analysis, email_id: str) -> str:
    """Génère le HTML pour la section des pièces jointes, incluant un lien de téléchargement ZIP."""
    attachments = analysis.get('attachments', [])
    attach_count = len(attachments)
    
    if attach_count:
        if attach_count <= 5:
            img_src = url_for('static', filename=f'images/{attach_count}.png')
        else:
            img_src = url_for('static', filename='images/more.png')
        img_html = f'<img style="display:inline-block" src="{img_src}">'
    else:
        img_html = ''

    html = f'''
    <div id="section_attachments" class="section">
        <h2 onclick="toggleVisibility('section_attachments')">
            Pièces jointes {img_html}
        </h2>
        <div class="section-content">
    '''

    if attachments:
        html += '<ul>'
        for attachment in attachments:
            file_sha256 = escape(str(attachment.get("sha256", "N/A")))
            filename = escape(attachment.get("filename", "N/A"))
            content_type = escape(attachment.get("content_type", "N/A"))
            size = escape(str(attachment.get("size", "N/A")))
            html += f'''
                <li><strong>Nom :</strong> {filename}</li>
                <li><strong>Type :</strong> {content_type}</li>
                <li><strong>Taille :</strong> {size} octets</li>
                <li>
                    <strong>SHA256 :</strong> {file_sha256}
                    <a href="https://www.virustotal.com/gui/file/{file_sha256}" target="_blank" rel="noopener noreferrer">
                        <button>Voir sur VT</button>
                    </a>
                </li>
            '''
        html += '</ul>'
        zip_url = url_for('download_page_bp.download_attachment_zip', email_id=email_id)
        html += f'<p><a href="{zip_url}" download>Télécharger toutes les pièces jointes (ZIP)</a></p>'
    else:
        html += '<p>Aucune pièce jointe.</p>'
    
    html += '''
        </div>
    </div>
    '''
    return html

# used by analysis/id page
def render_text_section(analysis) -> str:
    """Génère le HTML pour la section du contenu texte brut."""
    text_content = analysis.get('text', '')
    if text_content:
        escaped_text = escape(text_content[:5000])
        html = f'''
        <div id="section_text" class="section open">
            <h2 onclick="toggleVisibility('section_text')">Texte brut</h2>
            <div class="section-content open">
                <pre>{escaped_text}...</pre>
            </div>
        </div>
        '''
    else:
        html = '''
        <div id="section_text" class="section">
            <h2 onclick="toggleVisibility('section_text')">Texte brut</h2>
            <div class="section-content">
                <p>Aucun contenu texte trouvé.</p>
            </div>
        </div>
        '''
    return html

# used by analysis/id page
def render_html_section(analysis) -> str:
    """Génère le HTML pour la section du contenu HTML."""
    html_content = analysis.get('html', '')
    if html_content:
        escaped_html = escape(html_content[:5000])
        html = f'''
        <div id="section_html" class="section open">
            <h2 onclick="toggleVisibility('section_html')">HTML</h2>
            <div class="section-content open">
                <pre>{escaped_html}...</pre>
            </div>
        </div>
        '''
    else:
        html = '''
        <div id="section_html" class="section">
            <h2 onclick="toggleVisibility('section_html')">HTML</h2>
            <div class="section-content">
                <p>Aucun contenu HTML trouvé.</p>
            </div>
        </div>
        '''
    return html
