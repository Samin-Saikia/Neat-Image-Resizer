import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError

# ---------------------------
# Config / constants
# ---------------------------
APP_TITLE = "Neat Image Resizer"
WINDOW_SIZE = "900x560"
BG_COLOR = "#0f1724"         # deep background
CARD_BG = "#0b1220"          # card background
ACCENT = "#3b82f6"           # accent blue
TEXT = "#e6eef6"             # light text
CARD_PAD = 14

# ---------------------------
# Helper functions
# ---------------------------
def human_filesize(num_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def safe_open_image(path):
    """Open image with PIL and return Image object or raise."""
    return Image.open(path)

# ---------------------------
# Main App class
# ---------------------------
class ImageResizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        # State
        self.src_path = None
        self.src_img = None         # PIL Image
        self.preview_imgtk = None   # PhotoImage ref
        self.output_img = None      # PIL Image after processing

        self._create_styles()
        self._build_ui()

    def _create_styles(self):
        style = ttk.Style(self)
        style.theme_use('default')

        style.configure('Card.TFrame', background=CARD_BG)
        style.configure('Accent.TButton', background=ACCENT, foreground='white')
        style.map('Accent.TButton',
                  foreground=[('active', 'white')],
                  background=[('active', '#2563eb')])
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT)
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), foreground=TEXT, background=BG_COLOR)
        style.configure('Sub.TLabel', font=('Helvetica', 10), foreground=TEXT, background=BG_COLOR)
        style.configure('Small.TLabel', font=('Helvetica', 9), foreground='#bcd4ff', background=BG_COLOR)
        style.configure('Control.TButton', font=('Helvetica', 10), foreground=TEXT, background='#223047')
        style.configure('TScale', background=BG_COLOR)

    def _build_ui(self):
        # Header
        header = ttk.Frame(self, style='Card.TFrame', padding=(CARD_PAD))
        header.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.16)

        ttk.Label(header, text="Neat Image Resizer", style='Header.TLabel').pack(anchor='w')
        ttk.Label(header, text="Upload → Adjust → Save. Minimal quality loss, big size savings.", style='Sub.TLabel').pack(anchor='w', pady=(6,0))

        # Left: Preview Card
        preview_card = ttk.Frame(self, style='Card.TFrame', padding=(CARD_PAD))
        preview_card.place(relx=0.02, rely=0.2, relwidth=0.57, relheight=0.76)

        self.preview_canvas = tk.Canvas(preview_card, bg='#071023', highlightthickness=0)
        self.preview_canvas.pack(fill='both', expand=True)

        # Right: Controls Card
        controls_card = ttk.Frame(self, style='Card.TFrame', padding=(CARD_PAD))
        controls_card.place(relx=0.61, rely=0.2, relwidth=0.37, relheight=0.76)

        # Controls elements
        ttk.Label(controls_card, text="Controls", style='Header.TLabel').pack(anchor='w', pady=(0,8))

        # File info area
        self.file_name_label = ttk.Label(controls_card, text="No file loaded", style='Small.TLabel')
        self.file_name_label.pack(anchor='w')

        self.file_size_label = ttk.Label(controls_card, text="", style='Small.TLabel')
        self.file_size_label.pack(anchor='w', pady=(0,8))

        # Upload & Reset buttons
        btn_frame = ttk.Frame(controls_card, style='Card.TFrame')
        btn_frame.pack(fill='x', pady=(6,8))

        upload_btn = ttk.Button(btn_frame, text="Upload Image", style='Accent.TButton', command=self.load_image)
        upload_btn.pack(side='left', expand=True, fill='x', padx=(0,6))

        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_all)
        reset_btn.pack(side='left', expand=True, fill='x', padx=(6,0))

        # Sliders: quality & max width
        ttk.Label(controls_card, text="JPEG Quality", style='Small.TLabel').pack(anchor='w', pady=(8,0))
        self.quality_var = tk.IntVar(value=70)
        self.quality_scale = ttk.Scale(controls_card, from_=10, to=95, variable=self.quality_var, orient='horizontal')
        self.quality_scale.pack(fill='x')

        ttk.Label(controls_card, text="Max width (px) — resizing is optional", style='Small.TLabel').pack(anchor='w', pady=(8,0))
        self.width_var = tk.IntVar(value=1200)
        self.width_scale = ttk.Scale(controls_card, from_=200, to=4000, variable=self.width_var, orient='horizontal')
        self.width_scale.pack(fill='x')

        # Buttons: preview reduce and save
        action_frame = ttk.Frame(controls_card, style='Card.TFrame')
        action_frame.pack(fill='x', pady=(12,0))

        preview_btn = ttk.Button(action_frame, text="Preview Reduction", command=self.preview_reduce)
        preview_btn.pack(fill='x', pady=(0,6))

        reduce_btn = ttk.Button(action_frame, text="Reduce & Save As...", style='Accent.TButton', command=self.reduce_and_save)
        reduce_btn.pack(fill='x')

        # Small tips area
        tips = ttk.Label(controls_card, text="Tip: For PNG with transparency, saving as JPEG will remove transparency.\nUse PNG if you need transparency preserved.", style='Small.TLabel', wraplength=220)
        tips.pack(anchor='w', pady=(12,0))

        # Footer: credits
        footer = ttk.Label(self, text="Made with Pillow & Tkinter — Samin's helper", style='Sub.TLabel')
        footer.place(relx=0.02, rely=0.96)

    # ---------------------------
    # Actions
    # ---------------------------
    def load_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            ("All files", "*.*")
        ]
        path = filedialog.askopenfilename(title="Select an image", filetypes=filetypes)
        if not path:
            return
        try:
            img = safe_open_image(path)
        except UnidentifiedImageError:
            messagebox.showerror("Invalid image", "Couldn't open file as an image.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")
            return

        self.src_path = path
        self.src_img = img.copy()
        self.output_img = None
        self._update_file_info()
        self._show_preview(self.src_img)

    def _update_file_info(self):
        if not self.src_path:
            self.file_name_label.config(text="No file loaded")
            self.file_size_label.config(text="")
            return
        name = os.path.basename(self.src_path)
        size = os.path.getsize(self.src_path)
        self.file_name_label.config(text=f"File: {name}")
        self.file_size_label.config(text=f"Size: {human_filesize(size)} | Mode: {self.src_img.mode} | {self.src_img.size[0]}×{self.src_img.size[1]}")

    def _show_preview(self, pil_img):
        # Fit into preview canvas while preserving aspect ratio
        canvas_w = int(self.preview_canvas.winfo_width() or 480)
        canvas_h = int(self.preview_canvas.winfo_height() or 360)

        # If canvas size is 1 (not yet rendered), fallback to default
        if canvas_w < 10: canvas_w = 560
        if canvas_h < 10: canvas_h = 420

        img_w, img_h = pil_img.size
        scale = min(canvas_w/img_w, canvas_h/img_h, 1.0)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = pil_img.resize((new_w, new_h), Image.LANCZOS)
        self.preview_imgtk = ImageTk.PhotoImage(resized)

        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(canvas_w//2, canvas_h//2, image=self.preview_imgtk, anchor='center')

    def preview_reduce(self):
        if not self.src_img:
            messagebox.showinfo("No image", "Please upload an image first.")
            return
        quality = int(self.quality_var.get())
        max_width = int(self.width_var.get())

        img = self.src_img.copy()

        # Resize if needed
        if img.width > max_width:
            new_h = int((max_width / img.width) * img.height)
            img = img.resize((max_width, new_h), Image.LANCZOS)

        # For preview keep the format same; just show what final will look like visually at current quality.
        # (can't show exact file size without saving, but we give an estimate)
        self.output_img = img
        self._show_preview(self.output_img)

        # Estimate: save to temporary in memory to estimate size
        from io import BytesIO
        buf = BytesIO()
        save_kwargs = {}
        # If image is RGBA, preview saving as PNG to preserve transparency; JPEG would drop alpha.
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            img.save(buf, format='PNG', optimize=True)
        else:
            rgb = img.convert("RGB")
            rgb.save(buf, format='JPEG', quality=quality, optimize=True)
        size_bytes = buf.tell()
        messagebox.showinfo("Preview ready", f"Preview generated.\nEstimated size after save: {human_filesize(size_bytes)}")

    def reduce_and_save(self):
        if not self.src_img:
            messagebox.showinfo("No image", "Please upload an image first.")
            return

        # Ask where to save
        initial = os.path.splitext(os.path.basename(self.src_path))[0] if self.src_path else "resized"
        save_path = filedialog.asksaveasfilename(
            title="Save reduced image as...",
            defaultextension=".jpg",
            initialfile=f"{initial}_resized",
            filetypes=[("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png"), ("All files", "*.*")]
        )
        if not save_path:
            return

        quality = int(self.quality_var.get())
        max_width = int(self.width_var.get())

        img = self.src_img.copy()

        # If user chose PNG extension but original was JPEG that's okay — we will handle.
        ext = os.path.splitext(save_path)[1].lower()

        # Resize if necessary
        if img.width > max_width:
            new_h = int((max_width / img.width) * img.height)
            img = img.resize((max_width, new_h), Image.LANCZOS)

        # Decide save params depending on format
        try:
            if ext in ('.jpg', '.jpeg'):
                # JPEG requires RGB and discards alpha
                if img.mode in ("RGBA", "LA"):
                    # composite over white background before saving to JPEG
                    bg = Image.new("RGB", img.size, (255,255,255))
                    bg.paste(img, mask=img.split()[-1])  # paste with alpha as mask
                    final = bg
                else:
                    final = img.convert("RGB")
                final.save(save_path, format='JPEG', quality=quality, optimize=True)
            elif ext == '.png':
                # For PNG we preserve alpha if any and use optimize
                if img.mode in ("RGBA", "LA", "P"):
                    final = img
                else:
                    final = img.convert("RGBA")
                final.save(save_path, format='PNG', optimize=True)
            else:
                # Attempt to infer from extension; fallback to JPEG
                if img.mode in ("RGBA", "LA"):
                    bg = Image.new("RGB", img.size, (255,255,255))
                    bg.paste(img, mask=img.split()[-1])
                    final = bg
                else:
                    final = img.convert("RGB")
                final.save(save_path, quality=quality, optimize=True)
        except Exception as e:
            messagebox.showerror("Save failed", f"Couldn't save image:\n{e}")
            return

        final_size = os.path.getsize(save_path)
        messagebox.showinfo("Saved", f"Image saved to:\n{save_path}\nSize: {human_filesize(final_size)}")
        # update state
        self.src_path = save_path
        self.src_img = Image.open(save_path)
        self._update_file_info()
        self._show_preview(self.src_img)

    def reset_all(self):
        self.src_path = None
        self.src_img = None
        self.preview_imgtk = None
        self.output_img = None
        self.preview_canvas.delete("all")
        self.file_name_label.config(text="No file loaded")
        self.file_size_label.config(text="")

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app = ImageResizerApp()
    app.mainloop()
