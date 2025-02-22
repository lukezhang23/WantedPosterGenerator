from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pillow_heif import open_heif
import csv
import shutil
import subprocess
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def setup():
    # Register the custom font
    pdfmetrics.registerFont(TTFont("OldWestern", "go_2_old_western/Go2OldWestern-Regular.ttf"))

    data_dict = {}
    with open('Descriptions.csv', 'r', newline='', encoding='utf-8') as file:
        csvreader = csv.DictReader(file)  # Read as dictionary
        for row in csvreader:
            name = row["Name"]
            description = row["Description"]
            data_dict[name] = description  # Store name as key, description as value

    #Convert Heics to Jpgs
    images = [f for f in os.listdir("Headshots") if f.lower().endswith(".heic")]
    num_pages = len(images)
    if num_pages == 0:
        print("No HEIC images found in the directory.")
        return

    for img_name in images:
        heic_path = os.path.join("Headshots", img_name)
        jpeg_path = os.path.splitext(heic_path)[0] + ".jpg"
        convert_heic_to_jpeg(heic_path, jpeg_path)

    return data_dict

def image_naming_gui(possible_names):
    """
    Opens a GUI to loop through images in the 'Headshots' folder and assign names.

    Parameters:
    possible_names (list): List of possible names for auto-suggestion.

    Returns:
    dict: A dictionary mapping image filenames to user-provided names.
    """
    folder_path = "Headshots"  # Hardcoded folder path

    # Get all image files in the folder
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]

    if not image_files:
        print("No image files found in the 'Headshots' folder.")
        return {}

    # Dictionary to store image names
    image_names_dict = {}
    current_image_index = 0

    # Function to load the next image
    def load_next_image():
        nonlocal current_image_index
        if current_image_index < len(image_files):
            image_path = image_files[current_image_index]
            img = Image.open(image_path)
            img.thumbnail((400, 400))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)

            # Update image display
            label_img.config(image=img_tk)
            label_img.image = img_tk

            # Update filename label
            label_text.config(text=f"Image: {os.path.basename(image_path)}")

            # Restore previous name if available
            name_combobox.set(image_names_dict.get(os.path.basename(image_path), ''))

        else:
            # Show the "Finish" message when all images are processed
            label_text.config(text="All images processed.")
            save_button.config(state=tk.DISABLED)
            back_button.config(state=tk.DISABLED)

    # Function to load the previous image
    def load_previous_image():
        nonlocal current_image_index
        if current_image_index > 0:
            current_image_index -= 1  # Go back one image
            load_next_image()

    # Function to save the user-inputted name and move forward
    def save_name():
        nonlocal current_image_index
        if current_image_index < len(image_files):
            image_name = os.path.basename(image_files[current_image_index])
            user_name = name_combobox.get()
            if user_name:
                image_names_dict[image_name] = user_name
            current_image_index += 1
            load_next_image()

    # Setup the main window using tkinter
    root = tk.Tk()
    root.title("Image Name Assigning")

    # Image display label
    label_img = tk.Label(root)
    label_img.pack(pady=20)

    # Label to show image name (file name)
    label_text = tk.Label(root, text="Image: ", font=("Helvetica", 12))
    label_text.pack()

    # Combobox for auto-suggest input
    name_combobox = ttk.Combobox(root, values=possible_names, font=("Helvetica", 14), width=20)
    name_combobox.pack(pady=10)

    # Button to go back to the previous image
    back_button = tk.Button(root, text="Back", command=load_previous_image, font=("Helvetica", 14))
    back_button.pack(pady=10, side=tk.LEFT, padx=20)

    # Button to save the name and load the next image
    save_button = tk.Button(root, text="Save Name", command=save_name, font=("Helvetica", 14))
    save_button.pack(pady=10, side=tk.RIGHT, padx=20)

    # Load the first image
    load_next_image()

    # Run the tkinter event loop
    root.lift()
    root.attributes('-topmost', True)
    root.after(500, lambda: root.attributes('-topmost', False))
    root.focus_force()
    root.mainloop()

    return image_names_dict  # Return the dictionary after GUI closes

def convert_heic_to_jpeg(heic_path, jpeg_path):
    """Converts an HEIC image to JPEG format using pillow-heif."""
    heif_image = open_heif(heic_path)
    image = heif_image.to_pillow()
    image.save(jpeg_path, "JPEG")

def generate_wanted_pdf(filename, image_folder, file_mapping, descriptions):
    """Generates a PDF with 'WANTED' at the top of each page and inserts suspect images."""
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(".heic")]
    num_pages = len(images)

    if num_pages == 0:
        return

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 20  # Small margin on the edges
    img_size = width - (2 * margin)  # Make image width nearly full-page, keeping margins

    for img_name in images:
        heic_path = os.path.join(image_folder, img_name)
        jpeg_path = os.path.splitext(heic_path)[0] + ".jpg"
        just_name = jpeg_path.replace(image_folder + "/", "")

        # Wanted
        c.setFont("OldWestern", 160)
        c.drawCentredString(width / 2, height - 140, "WANTED")

        # $1,000,000
        c.setFont("OldWestern", 90)
        c.drawCentredString(width / 2, height - 230, "$10,000,000")

        # Hand Icons
        c.drawImage("Icons/pointy-hand-md.jpg", 50, height - 225, width=80, height=40)
        c.drawImage("Icons/pointy-hand-md-2.jpg", width - 140, height - 225, width=80, height=40)

        # Set image dimensions (example dimensions for a rectangular image)
        img_width = 500  # Adjust based on the aspect ratio you want
        img_height = 375  # Adjust based on the aspect ratio you want

        # Center the image on the page
        img_x = (width - img_width) / 2  # Center horizontally
        img_y = (height - img_height) / 2 - 40 # Center vertically

        # Draw the image
        c.drawImage(jpeg_path, img_x, img_y, width=img_width, height=img_height)

        # Name
        c.setFont("OldWestern", 90)
        c.drawCentredString(width / 2, height - 700, file_mapping[just_name])

        box_width = 500  # Width of the box
        box_height = 50  # Height of the box

        # Calculate the x position to center the box horizontally on the page
        x = (width - box_width) / 2  # Center the box on the page

        # Set the position and size for the black box
        y = 20  # y position of the box (fixed)

        # Draw a black rectangle (the box)
        c.setFillColorRGB(0, 0, 0)  # Set fill color to black
        c.rect(x, y, box_width, box_height, fill=1)  # Draw and fill the rectangle

        # Text to be inserted inside the box
        text = descriptions[file_mapping[just_name]].upper()

        # Set the font and color for the text inside the box
        c.setFont("OldWestern", 40)
        c.setFillColorRGB(1, 1, 1)  # Set text color to white

        # Calculate the width and height of the text
        text_width = c.stringWidth(text, "OldWestern", 40)
        text_height = 25  # The height of the font (fixed size)

        # Calculate positions for centering the text inside the box
        text_x = x + (box_width - text_width) / 2  # Center horizontally inside the box
        text_y = y + (box_height - text_height) / 2  # Center vertically inside the box

        # Draw the centered text inside the black box
        c.drawString(text_x, text_y, text)

        c.showPage()

    c.save()
    print(f"PDF '{filename}' with {num_pages} pages created successfully.")

def cleanup():

    # Define directories
    source_dir = "Headshots"
    archive_dir = "HeadshotsArchive"

    # Ensure archive directory exists
    os.makedirs(archive_dir, exist_ok=True)

    # Iterate through files in source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Move HEIC files to HeadshotsArchive
        if filename.lower().endswith(".heic"):
            shutil.move(file_path, os.path.join(archive_dir, filename))

        # Delete JPG files
        elif filename.lower().endswith(".jpg"):
            os.remove(file_path)

    print("JPGs moved and HEICs deleted successfully.")


if __name__ == "__main__":
    descriptions = setup()
    files_to_names = image_naming_gui(list(descriptions.keys()))
    generate_wanted_pdf("wanted_poster.pdf", "Headshots", files_to_names, descriptions)
    cleanup()

    # Open the PDF in Preview
    subprocess.run(["open", "-a", "Preview", "wanted_poster.pdf"])
