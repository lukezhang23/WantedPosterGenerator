# Wanted Poster Generator

## Overview
This project was a personal project for the youth group event "Underground Church." It generates "Wanted Posters" after being given a CSV of names of descriptions, and a folder with images.

## Dependencies
This project requires the following Python packages:

### Python Packages
- `reportlab` – For generating PDFs  
- `pillow_heif` – To handle HEIF image formats  
- `csv` – For reading and writing CSV files (built-in)  
- `shutil` – For file operations (built-in)  
- `subprocess` – To execute shell commands (built-in)  
- `os` – For interacting with the filesystem (built-in)  
- `tkinter` – For GUI interactions (built-in)  
- `Pillow` – For image processing  

### Installation
To install required external libraries, run:
```sh
pip install reportlab pillow_heif pillow
```

## Fonts
This project uses a custom font: **Go 2 Old Western**.  

### Download
1. Download the font file from https://www.dafont.com/go-2-old-western.font.  
2. Place the downloaded folder in the project directory (filename of .ttf file should be "go_2_old_western/Go2OldWestern-Regular.ttf").  
3. The script will register the font automatically when generating PDFs.

## Using the Program
The usability for this program is quite limited/specific since this software was built just for one-time use. However, I will still add documentation on how to use it.

1. Add a Descriptions.csv file to the directory, a template that you can export to a CSV is found in DescriptionsTemplate.xlsx
2. Add the headshot images you want to use into a "Headshots" folder in the directory. These images should be in HEIC format. Images in JPG format will probably work but may run into bugs. Images should have a 4:3 aspect ratio.
3. Run the Python Program, a GUI will pop up for the user to assign names (from Descriptions.csv) to images.
4. The program will create a "wanted_poster.pdf" file which is a PDF of all the generated wanted posters. It will also move all HEIC photos in the "Headshots" folder to the "HeadshotsArchive" folder. (JPG images may be deleted in Headshots and not restored in HeadshotsArchive)
