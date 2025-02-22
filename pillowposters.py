from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from pillow_heif import open_heif

# Register the custom font
pdfmetrics.registerFont(TTFont("OldWestern", "go_2_old_western/Go2OldWestern-Regular.ttf"))

def convert_heic_to_jpeg(heic_path, jpeg_path):
    """Converts an HEIC image to JPEG format using pillow-heif."""
    heif_image = open_heif(heic_path)
    image = heif_image.to_pillow()
    image.save(jpeg_path, "JPEG")

def generate_wanted_pdf(filename, image_folder):
    """Generates a PDF with 'WANTED' at the top of each page and inserts suspect images."""
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(".heic")]
    num_pages = len(images)

    if num_pages == 0:
        print("No HEIC images found in the directory.")
        return

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 20  # Small margin on the edges
    img_size = width - (2 * margin)  # Make image width nearly full-page, keeping margins

    for img_name in images:
        heic_path = os.path.join(image_folder, img_name)
        jpeg_path = os.path.splitext(heic_path)[0] + ".jpg"

        convert_heic_to_jpeg(heic_path, jpeg_path)

        c.setFont("OldWestern", 175)
        c.drawCentredString(width / 2, height - 150, "WANTED")

        # Wanted for
        c.setFont("OldWestern", 100)
        c.drawCentredString(width / 2, height - 250, "$1,000,000")

        # Hand Icons
        c.drawImage("Icons/pointy-hand-md.jpg", 50, height - 245, width=90, height=45)
        c.drawImage("Icons/pointy-hand-md-2.jpg", width - 140, height - 245, width=90, height=45)

        # Set image dimensions (example dimensions for a rectangular image)
        img_width = 500  # Adjust based on the aspect ratio you want
        img_height = 375  # Adjust based on the aspect ratio you want

        # Center the image on the page
        img_x = (width - img_width) / 2  # Center horizontally
        img_y = (height - img_height) / 2 - 75 # Center vertically

        # Draw the image
        c.drawImage(jpeg_path, img_x, img_y, width=img_width, height=img_height)

        # Name
        c.setFont("OldWestern", 90)
        c.drawCentredString(width / 2, height - 750, "Brutus Buckeye")

        c.showPage()

    c.save()
    print(f"PDF '{filename}' with {num_pages} pages created successfully.")

if __name__ == "__main__":
    generate_wanted_pdf("wanted_poster.pdf", "Headshots")
    import subprocess

    # Open the PDF in Preview
    subprocess.run(["open", "-a", "Preview", "wanted_poster.pdf"])
