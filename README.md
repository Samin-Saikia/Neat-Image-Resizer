# Neat-Image-Resizer
A modern, clean, and beginner-friendly Tkinter GUI application that lets you upload an image, resize it, compress it, preview the output, and download the optimized version — all in one sleek interface.

This project uses Tkinter + Pillow (PIL) and is perfect for students, developers, content creators, and anyone who wants to reduce image size without losing too much quality.
# Features
✔ Easy Upload

Select images using a file dialog (PNG, JPG, JPEG, BMP, GIF, TIFF supported).

✔ Live Image Preview

The app shows the image inside a preview card with auto aspect-ratio scaling.

✔ Adjustable Quality

Use a slider to set JPEG quality (10–95) to control compression strength.

✔ Adjustable Max Width

Reduce width while keeping the aspect ratio or skip resizing entirely.

✔ Smart Format Handling

PNG transparency automatically preserved.

JPEG output auto-flattens transparent layers to avoid errors.

✔ Save Anywhere

Choose custom filename, format, and location for your optimized image.

✔ File Info Display

Shows image size, mode, and resolution.

✔ Clean & Creative UI

Dark aesthetic with a modern card layout, powered by Tkinter's ttk themes.
# Installation
1️⃣ Clone this repository
git clone https://github.com/Samin-Saikia/neat-image-resizer.git
cd neat-image-resizer

2️⃣ Install required dependencies

Make sure you have Python 3.7+ installed.

pip install pillow


Tkinter comes pre-installed with Python on Windows/Linux.
Mac users may need:

brew install python-tk

▶️ Running the Application

Just run:

python image_resizer_gui.py

The GUI will open instantly.

# Project Structure
Neat-Image-Resizer/
│
├── main.py     # Main GUI application
├── README.md 

# How It Works (Short Explanation)

1/ The app uses Pillow to load and process images.

2/ Tkinter handles the visual interface.

3/ Images are resized using high-quality Image.LANCZOS.

4/ Quality slider controls JPEG compression.

5/ A live preview shows the output before saving.

6/ Saving logic adapts to PNG/JPEG formats automatically.

# Use Cases

1/ Compressing images for websites

2/ Reducing size for email uploads

3/ Preparing graphics for apps

4/ Shrinking large photos

5/ Resizing memes/logos without quality loss

# Contributing

Pull requests are welcome!
If you want new features like batch resizing, drag-and-drop upload, or a progress bar, feel free to open an issue.

# Author

Samin Saikia
Class 11 • Science Stream
Aspiring jee, Aspiring B.Tech Student
Learning Python, JS, Flask & Machine Learning
