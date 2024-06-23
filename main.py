import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for the progress bars
import os
from pdf import Pdf

def process_pdf(DIR, pdf_path):
    p = Pdf(DIR, pdf_path)
    p_count = p.get_pages_count()
    pp_count = 0

    p_bar_2["maximum"] = p_count
    p_bar_2["value"] = 0
    p_count_l.config(text=f'{pp_count} pages processed from {p_count} pages')
    root.update_idletasks()  # Update GUI

    for _ in p.to_csv():
        pp_count += 10
        p_bar_2["value"] = pp_count
        p_count_l.config(text=f'{pp_count} pages processed from {p_count} pages')
        root.update_idletasks()  # Update GUI

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

def process_files():
    folder = folder_entry.get()
    if not os.path.exists(folder):
        messagebox.showerror("Error", "Folder doesn't exist")
    elif not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path")
    else:
        pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
        if messagebox.askyesno("Confirmation", f"{len(pdf_files)} pdf files found. Do you want to process?"):
            fp_count = 0
            p_bar_1["maximum"] = len(pdf_files)
            p_bar_1["value"] = 0
            f_count_l.config(text=f'{fp_count} files processed from {len(pdf_files)} files')
            root.update_idletasks()  # Update GUI

            for pdf_path in pdf_files:
                process_pdf(folder, pdf_path)
                fp_count += 1
                p_bar_1["value"] = fp_count
                f_count_l.config(text=f'{fp_count} files processed from {len(pdf_files)} files')
                root.update_idletasks()  # Update GUI

# Initialize the main window
root = tk.Tk()
root.title("PDF Data Extractor")

# Input Folder Label and Entry
input_label = tk.Label(root, text="Input Folder", width=15, anchor='w')
input_label.grid(row=0, column=0, padx=10, pady=5)

folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Process Button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=1, column=1, pady=10)

# Horizontal Line
line = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
line.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)

# Status Labels and Progress Bars
f_count_l = tk.Label(root, text="0 files processed from 0 files")
f_count_l.grid(row=3, column=0, columnspan=3, pady=5)

p_bar_1 = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
p_bar_1.grid(row=4, column=0, columnspan=3, pady=5)

p_count_l = tk.Label(root, text="0 pages processed from 0 pages")
p_count_l.grid(row=5, column=0, columnspan=3, pady=5)

p_bar_2 = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
p_bar_2.grid(row=6, column=0, columnspan=3, pady=5)

# Run the application
root.mainloop()
