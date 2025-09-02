


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