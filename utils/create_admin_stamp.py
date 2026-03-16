# =============================================================================
# NEWZ - Générateur de Cachet Admin (Utilitaire)
# Fichier : utils/create_admin_stamp.py
# =============================================================================

from PIL import Image, ImageDraw, ImageFont
import os

def create_admin_stamp(output_path="assets/admin_stamp.png"):
    """
    Crée un cachet administratif 'CONFIDENTIEL' simple
    """
    # Création de l'image (fond transparent)
    size = (200, 200)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Couleurs
    border_color = (180, 0, 0, 200)  # Rouge foncé transparent
    text_color = (180, 0, 0, 255)    # Rouge foncé
    
    # Cercle extérieur
    margin = 10
    draw.ellipse(
        [margin, margin, size[0]-margin, size[1]-margin],
        outline=border_color,
        width=4
    )
    
    # Cercle intérieur
    margin_inner = 20
    draw.ellipse(
        [margin_inner, margin_inner, size[0]-margin_inner, size[1]-margin_inner],
        outline=border_color,
        width=2
    )
    
    # Texte (essai avec police par défaut)
    try:
        # Police personnalisée si disponible
        font = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_small = font
    
    # Texte principal
    text = "ADMIN"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - text_height) / 2 - 15
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    # Texte secondaire
    text2 = "CONFIDENTIEL"
    text2_bbox = draw.textbbox((0, 0), text2, font=font_small)
    text2_width = text2_bbox[2] - text2_bbox[0]
    text2_x = (size[0] - text2_width) / 2
    text2_y = (size[1] - text_height) / 2 + 20
    draw.text((text2_x, text2_y), text2, fill=text_color, font=font_small)
    
    # Sauvegarde
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, 'PNG')
    
    print(f"✅ Cachet Admin généré : {output_path}")
    return output_path

if __name__ == "__main__":
    create_admin_stamp()
