import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image

def select_folder(prompt, entry_widget):
    folder_selected = filedialog.askdirectory(title=prompt)
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)

def crunch_images(input_folder, output_folder, quality):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")  # Ensure it's in RGB mode for JPEG
                    img.save(output_path, format='JPEG', quality=quality)
                    print(f"Compressed: {filename} -> {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def update_quality_label(val, label):
    label.config(text=f"Quality: {int(float(val))}")

def start_compression(input_entry, output_entry, quality_slider):
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    quality = int(quality_slider.get())
    
    if not input_folder:
        messagebox.showwarning("Warning", "No input folder selected.")
        return
    if not output_folder:
        messagebox.showwarning("Warning", "No output folder selected.")
        return
    
    crunch_images(input_folder, output_folder, quality)
    messagebox.showinfo("Success", "Image compression complete!")

def create_gui():
    root = tk.Tk()
    root.title("Image Cruncher")
    root.geometry("500x300")
    
    frame = ttk.Frame(root, padding=10)
    frame.pack(expand=True, fill='both')
    
    ttk.Label(frame, text="Input Folder:").pack(anchor='w')
    input_entry = ttk.Entry(frame, width=50)
    input_entry.pack()
    ttk.Button(frame, text="Browse", command=lambda: select_folder("Select folder with images to crunch", input_entry)).pack()
    
    ttk.Label(frame, text="Output Folder:").pack(anchor='w')
    output_entry = ttk.Entry(frame, width=50)
    output_entry.pack()
    ttk.Button(frame, text="Browse", command=lambda: select_folder("Select folder to save crunched images", output_entry)).pack()
    
    quality_label = ttk.Label(frame, text="Quality: 70")
    quality_label.pack(anchor='w')
    quality_slider = ttk.Scale(frame, from_=1, to=100, orient='horizontal', command=lambda val: update_quality_label(val, quality_label))
    quality_slider.set(70)
    quality_slider.pack()
    
    compress_button = ttk.Button(frame, text="Start Compression", command=lambda: start_compression(input_entry, output_entry, quality_slider))
    compress_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
