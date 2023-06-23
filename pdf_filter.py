import os
import tkinter as tk
from tkinter import ttk, filedialog
import textract


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)


def process_files():
    folder_path = folder_entry.get()
    keywords = keyword_listbox.get(0, tk.END)
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

            has_all_keywords = True
            for keyword in keywords:
                if keyword.lower() not in text.lower():
                    has_all_keywords = False
                    break

            if has_all_keywords:
                destination = os.path.join(inclusion_folder, filename)
            else:
                destination = os.path.join(exclusion_folder, filename)

            os.rename(pdf_path, destination)

    update_file_tree(inclusion_tree, inclusion_folder)
    update_file_tree(exclusion_tree, exclusion_folder)
    update_file_tree(missing_abstract_tree, missing_abstract_folder)


def view_pdf(event):
    item = event.widget.focus()
    values = event.widget.item(item, 'values')
    if values:
        file_path = values[0]
        paper_type = values[1]
        pdf_viewer['text'] = f"Viewing PDF: {file_path}\nPaper Type: {paper_type}"
    else:
        pdf_viewer['text'] = "No PDF selected"


def update_file_tree(tree, folder):
    tree.delete(*tree.get_children())
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder, filename)

            # Extract text from PDF using textract
            text = textract.process(pdf_path, method='pdfminer').decode('utf-8')

            paper_type = determine_paper_type(text)

            tree.insert('', 'end', values=(pdf_path, paper_type))


def determine_paper_type(text):
    # List of keywords to determine the paper type
    keywords = {
        'empirical': ['study', 'data', 'results'],
        'position paper': ['position', 'argue', 'opinion'],
        'blog post': ['blog', 'post'],
        'poster': ['poster', 'conference'],
        'theory': ['theory', 'conceptual'],
        'thesis/dissertation': ['thesis', 'dissertation', 'doctoral']
    }

    for paper_type, keyword_list in keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keyword_list):
            return paper_type

    return 'Unknown'


# Create the main window
window = tk.Tk()
window.title("PDF File Filter")
window.geometry("800x600")

# Folder selection
folder_label = tk.Label(window, text="Select Folder:", font=("Arial", 12))
folder_label.pack(pady=10)
folder_entry = tk.Entry(window, font=("Arial", 12))
folder_entry.pack(pady=5)
folder_button = ttk.Button(window, text="Browse", command=select_folder)
folder_button.pack(pady=5)

# Filter option
filter_var = tk.StringVar(window, "Abstract")
filter_label = tk.Label(window, text="Filter Option:", font=("Arial", 12))
filter_label.pack(pady=5)
abstract_radio = tk.Radiobutton(window, text="Abstract", variable=filter_var, value="Abstract", font=("Arial", 12))
abstract_radio.pack(pady=2)
entire_paper_radio = tk.Radiobutton(window, text="Entire Paper", variable=filter_var, value="Entire Paper",
                                   font=("Arial", 12))
entire_paper_radio.pack(pady=2)

# Keyword entry
keyword_label = tk.Label(window, text="Enter Keywords (press Enter to add):", font=("Arial", 12))
keyword_label.pack(pady=5)
keyword_frame = ttk.Frame(window)
keyword_frame.pack(pady=5)

keyword_listbox = tk.Listbox(keyword_frame, font=("Arial", 12))
keyword_listbox.pack(side="left", padx=2, pady=2)

keyword_scrollbar = tk.Scrollbar(keyword_frame, orient="vertical")
keyword_scrollbar.config(command=keyword_listbox.yview)
keyword_scrollbar.pack(side="right", fill="y")

keyword_listbox.config(yscrollcommand=keyword_scrollbar.set)

keyword_entry = ttk.Entry(window, font=("Arial", 12))
keyword_entry.pack(pady=5)


def add_keyword(event=None):
    keyword = keyword_entry.get().strip()
    if keyword:
        keyword_listbox.insert(tk.END, keyword)
        keyword_entry.delete(0, tk.END)


def remove_keyword():
    selected_index = keyword_listbox.curselection()
    if selected_index:
        keyword_listbox.delete(selected_index)


keyword_entry.bind('<Return>', add_keyword)

# Keyword buttons
keyword_button_frame = ttk.Frame(window)
keyword_button_frame.pack(pady=5)

add_button = ttk.Button(keyword_button_frame, text="Add", command=add_keyword)
add_button.pack(side="left", padx=2)

remove_button = ttk.Button(keyword_button_frame, text="Remove", command=remove_keyword)
remove_button.pack(side="left", padx=2)

# Process button
process_button = ttk.Button(window, text="Process Files", command=process_files)
process_button.pack(pady=10)

# Results
results_frame = ttk.Frame(window)
results_frame.pack(pady=10)

# File Tree Views
inclusion_label = tk.Label(results_frame, text="Inclusion Files", font=("Arial", 12))
inclusion_label.grid(row=0, column=0, padx=10)
inclusion_tree = ttk.Treeview(results_frame, columns=("File Path", "Paper Type"), show="headings", height=10)
inclusion_tree.column("File Path", width=400, anchor="w")
inclusion_tree.column("Paper Type", width=150, anchor="w")
inclusion_tree.heading("File Path", text="File Path")
inclusion_tree.heading("Paper Type", text="Paper Type")
inclusion_tree.grid(row=1, column=0, padx=10, pady=5)
inclusion_tree.bind("<<TreeviewSelect>>", view_pdf)

exclusion_label = tk.Label(results_frame, text="Exclusion Files", font=("Arial", 12))
exclusion_label.grid(row=0, column=1, padx=10)
exclusion_tree = ttk.Treeview(results_frame, columns=("File Path", "Paper Type"), show="headings", height=10)
exclusion_tree.column("File Path", width=400, anchor="w")
exclusion_tree.column("Paper Type", width=150, anchor="w")
exclusion_tree.heading("File Path", text="File Path")
exclusion_tree.heading("Paper Type", text="Paper Type")
exclusion_tree.grid(row=1, column=1, padx=10, pady=5)
exclusion_tree.bind("<<TreeviewSelect>>", view_pdf)

missing_abstract_label = tk.Label(results_frame, text="Missing Abstract Files", font=("Arial", 12))
missing_abstract_label.grid(row=0, column=2, padx=10)
missing_abstract_tree = ttk.Treeview(results_frame, columns=("File Path", "Paper Type"), show="headings", height=10)
missing_abstract_tree.column("File Path", width=400, anchor="w")
missing_abstract_tree.column("Paper Type", width=150, anchor="w")
missing_abstract_tree.heading("File Path", text="File Path")
missing_abstract_tree.heading("Paper Type", text="Paper Type")
missing_abstract_tree.grid(row=1, column=2, padx=10, pady=5)
missing_abstract_tree.bind("<<TreeviewSelect>>", view_pdf)

# PDF Viewer
pdf_viewer_frame = ttk.Frame(window)
pdf_viewer_frame.pack(pady=10)
pdf_viewer = ttk.Label(pdf_viewer_frame, text="No PDF selected", font=("Arial", 12))
pdf_viewer.pack()

window.mainloop()
