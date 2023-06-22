import os
import tkinter as tk
from tkinter import filedialog
import textract


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)


def process_files():
    folder_path = folder_entry.get()
    keywords = keyword_entry.get().split(',')
    filter_option = filter_var.get()
    inclusion_folder = os.path.join(folder_path, 'Inclusion')
    exclusion_folder = os.path.join(folder_path, 'Exclusion')
    missing_abstract_folder = os.path.join(folder_path, 'Missing Abstract')
    
    if not os.path.exists(inclusion_folder):
        os.makedirs(inclusion_folder)
    
    if not os.path.exists(exclusion_folder):
        os.makedirs(exclusion_folder)
    
    if not os.path.exists(missing_abstract_folder):
        os.makedirs(missing_abstract_folder)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            
            # Extract text from PDF using textract
            text = textract.process(pdf_path, method='pdfminer').decode('utf-8')
            
            if filter_option == 'Abstract':
                # Check if the PDF has an abstract
                if 'abstract' not in text.lower():
                    destination = os.path.join(missing_abstract_folder, filename)
                    os.rename(pdf_path, destination)
                    continue
            elif filter_option == 'Entire Paper':
                pass
            
            if any(keyword.lower() in text.lower() for keyword in keywords):
                destination = os.path.join(inclusion_folder, filename)
            else:
                destination = os.path.join(exclusion_folder, filename)
            
            os.rename(pdf_path, destination)
    
    inclusion_files = os.listdir(inclusion_folder)
    exclusion_files = os.listdir(exclusion_folder)
    
    inclusion_text.delete(1.0, tk.END)
    inclusion_text.insert(tk.END, 'Inclusion Files:\n')
    for file in inclusion_files:
        inclusion_text.insert(tk.END, file + '\n')
    
    exclusion_text.delete(1.0, tk.END)
    exclusion_text.insert(tk.END, 'Exclusion Files:\n')
    for file in exclusion_files:
        exclusion_text.insert(tk.END, file + '\n')


# Create the main window
window = tk.Tk()
window.title("PDF File Filter")
window.geometry("500x400")

# Folder selection
folder_label = tk.Label(window, text="Select Folder:")
folder_label.pack()
folder_entry = tk.Entry(window)
folder_entry.pack()
folder_button = tk.Button(window, text="Browse", command=select_folder)
folder_button.pack()

# Keyword entry
keyword_label = tk.Label(window, text="Enter Keywords (comma-separated):")
keyword_label.pack()
keyword_entry = tk.Entry(window)
keyword_entry.pack()

# Filter option
filter_var = tk.StringVar(window, "Abstract")
filter_label = tk.Label(window, text="Filter Option:")
filter_label.pack()
abstract_radio = tk.Radiobutton(window, text="Abstract", variable=filter_var, value="Abstract")
abstract_radio.pack()
entire_paper_radio = tk.Radiobutton(window, text="Entire Paper", variable=filter_var, value="Entire Paper")
entire_paper_radio.pack()

# Process button
process_button = tk.Button(window, text="Process Files", command=process_files)
process_button.pack()

# Results
results_frame = tk.Frame(window)
results_frame.pack()

inclusion_text = tk.Text(results_frame, height=10, width=30)
inclusion_text.pack(side=tk.LEFT)
inclusion_scrollbar = tk.Scrollbar(results_frame, command=inclusion_text.yview)
inclusion_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
inclusion_text.config(yscrollcommand=inclusion_scrollbar.set)

exclusion_text = tk.Text(results_frame, height=10, width=30)
exclusion_text.pack(side=tk.LEFT)
exclusion_scrollbar = tk.Scrollbar(results_frame, command=exclusion_text.yview)
exclusion_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
exclusion_text.config(yscrollcommand=exclusion_scrollbar.set)

# Run the GUI main loop
window.mainloop()
