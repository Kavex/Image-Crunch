import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image

# Debug flag: Set to False to hide console output
DEBUG = True

def debug_print(message):
    """Prints debug messages only if DEBUG is True."""
    if DEBUG:
        print(message)

# Function to select a single file
def select_file(entry_widget):
    file_selected = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tga;*.tiff;*.webp")])
    if file_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_selected)

# Function to select a folder and update the file list
def select_folder(entry_widget, file_listbox):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)
        if file_listbox:
            update_file_list(entry_widget, file_listbox)

# Function to update quality value from slider
def update_quality(val, entry):
    entry.delete(0, tk.END)
    entry.insert(0, str(int(float(val))))

# Function to process a single image
def crunch_image(input_path, output_folder, quality, output_format):
    try:
        with Image.open(input_path) as img:
            output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_path))[0] + '.' + output_format.lower())
            img.convert("RGB").save(output_path, format=output_format, quality=quality)
            debug_print(f"Processed: {output_path}")
    except Exception as e:
        debug_print(f"Error processing {input_path}: {e}")

# Function to process all images in a folder
def crunch_images(input_folder, output_folder, quality, output_format, file_listbox):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(("png", "jpg", "jpeg", "bmp", "gif", "tga", "tiff", "webp")):
            input_path = os.path.join(input_folder, filename)
            crunch_image(input_path, output_folder, quality, output_format)
    
    messagebox.showinfo("Success", "Image processing complete!")

# Function to update the file list in batch mode
def update_file_list(input_entry, file_listbox):
    file_listbox.delete(0, tk.END)
    folder = input_entry.get()
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(("png", "jpg", "jpeg", "bmp", "gif", "tga", "tiff", "webp")):
                file_path = os.path.join(folder, file)
                file_size = os.path.getsize(file_path) // 1024  # Convert size to KB
                file_listbox.insert(tk.END, f"{file} ({file.split('.')[-1].upper()} - {file_size} KB)")

# Function to create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Image Cruncher")
    root.geometry("700x500")
    
    # Supported output formats
    output_formats = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "TGA"]
    format_var = tk.StringVar(value="JPEG")
    
    ttk.Label(root, text="Output Format:").pack(anchor='w')
    format_dropdown = ttk.Combobox(root, textvariable=format_var, values=output_formats, state="readonly")
    format_dropdown.pack()
    
    # Create tabbed interface
    tab_control = ttk.Notebook(root)
    single_tab = ttk.Frame(tab_control)
    batch_tab = ttk.Frame(tab_control)
    tab_control.add(single_tab, text="Single Image Mode")
    tab_control.add(batch_tab, text="Batch Mode")
    tab_control.pack(expand=1, fill="both")
    
    # Single Image Mode UI
    ttk.Label(single_tab, text="Select Image:").pack(anchor='w')
    single_input = ttk.Entry(single_tab, width=50)
    single_input.pack()
    ttk.Button(single_tab, text="Browse", command=lambda: select_file(single_input)).pack()
    
    ttk.Label(single_tab, text="Output Folder:").pack(anchor='w')
    single_output = ttk.Entry(single_tab, width=50)
    single_output.pack()
    ttk.Button(single_tab, text="Browse", command=lambda: select_folder(single_output, None)).pack()
    
    ttk.Label(single_tab, text="Quality:").pack(anchor='w')
    single_quality = ttk.Entry(single_tab, width=5)
    single_quality.pack()
    single_quality.insert(0, "70")
    single_slider = ttk.Scale(single_tab, from_=1, to=100, orient='horizontal', command=lambda val: update_quality(val, single_quality))
    single_slider.set(70)
    single_slider.pack()
    
    ttk.Button(single_tab, text="Convert", command=lambda: crunch_image(single_input.get(), single_output.get(), int(single_quality.get()), format_var.get())).pack()
    
    # Batch Mode UI
    ttk.Label(batch_tab, text="Input Folder:").pack(anchor='w')
    batch_input = ttk.Entry(batch_tab, width=50)
    batch_input.pack()
    ttk.Button(batch_tab, text="Browse", command=lambda: select_folder(batch_input, file_listbox)).pack()
    
    ttk.Label(batch_tab, text="Output Folder:").pack(anchor='w')
    batch_output = ttk.Entry(batch_tab, width=50)
    batch_output.pack()
    ttk.Button(batch_tab, text="Browse", command=lambda: select_folder(batch_output, None)).pack()
    
    ttk.Label(batch_tab, text="Quality:").pack(anchor='w')
    batch_quality = ttk.Entry(batch_tab, width=5)
    batch_quality.pack()
    batch_quality.insert(0, "70")
    batch_slider = ttk.Scale(batch_tab, from_=1, to=100, orient='horizontal', command=lambda val: update_quality(val, batch_quality))
    batch_slider.set(70)
    batch_slider.pack()
    
    file_listbox = tk.Listbox(batch_tab, height=10, width=80)
    file_listbox.pack(fill='both', expand=True)
    
    ttk.Button(batch_tab, text="Start Batch Conversion", command=lambda: crunch_images(batch_input.get(), batch_output.get(), int(batch_quality.get()), format_var.get(), file_listbox)).pack()
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
