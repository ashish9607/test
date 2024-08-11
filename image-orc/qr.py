import qrcode
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_qr_with_text(text):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Set up font and wrapping for text
    try:
        # Using a common font
        font = ImageFont.truetype("DejaVuSans.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Text wrapping to fit in a box below the QR code
    max_width = qr_img.size[0] - 20  # 10 pixels padding on each side
    wrapped_text = textwrap.fill(text, width=40)  # 40 chars is a rough estimate
    
    # Manually calculate text size using getbbox
    lines = wrapped_text.splitlines()
    text_width = max(font.getbbox(line)[2] for line in lines)
    text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    
    # Adjust font size if text is too wide
    while text_width > max_width:
        font = ImageFont.truetype("DejaVuSans.ttf", font.size - 1)
        text_width = max(font.getbbox(line)[2] for line in lines)
        text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    
    # Create new image to place QR and text together
    total_height = qr_img.size[1] + text_height + 10  # 10 pixels padding between QR and text
    new_img = Image.new('RGB', (qr_img.size[0], total_height), "white")
    
    # Paste QR code
    new_img.paste(qr_img, (0, 0))
    
    # Draw the text
    draw = ImageDraw.Draw(new_img)
    text_x = (qr_img.size[0] - text_width) // 2
    text_y = qr_img.size[1] - 20
    for line in lines:
        draw.text((text_x, text_y), line, font=font, fill="black")
        text_y += font.getbbox(line)[3] - font.getbbox(line)[1] +5

    return new_img

# Example usage
example_text = "This is fdb dfb  segsrg gdrb bsdbf dsb"
qr_image = generate_qr_with_text(example_text)
fixed_size = (400, 440)  # width, height
resized_image = qr_image.resize(fixed_size)
resized_image.save("resized_image.jpg")
resized_image.show()
