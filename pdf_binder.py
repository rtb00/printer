#! python3

import os
import pymupdf
import tkinter as tk
from tkinter import filedialog

def remove_unwanted_pages(pdf_path, pages, output_pdf_path=None):
    doc = pymupdf.open(pdf_path)
    total_pages = doc.page_count

    newdoc = pymupdf.open()  # Neues, leeres Dokument

    for p in pages:
        if p is None:
            newdoc.new_page(width=doc[0].rect.width, height=doc[0].rect.height)
            
        elif 1 <= int(p) <= total_pages:
            newdoc.insert_pdf(doc, from_page=p-1, to_page=p-1)
        else:
            print(f"Seite {p} existiert nicht.")

    if newdoc.page_count == 0:
        doc.close()
        newdoc.close()
        return pdf_path

    if output_pdf_path is None:
        output_pdf_path = pdf_path

    newdoc.save(output_pdf_path)
    newdoc.close()
    doc.close()
    return output_pdf_path

file_path = ""
user_input = ""

def submit_text():
    global confirm_label, success_label, file_path, user_input
    user_input = entry.get()
    confirm_label.config(text=f"Eingegebener Text: {user_input}", fg="green")
    
    if not os.path.exists(file_path):
        success_label.config(text="Keine PDF-Datei ausgewählt!", fg="red")
        return

    doc = pymupdf.open(file_path)
    length = doc.page_count
    doc.close()

    seiten_str = os.popen("python3 book_pages.py " + str(length) + ' ' + user_input).read()
    
    try:
        seiten = [int(num.strip()) if num.strip().isdigit() else None for num in seiten_str.split("_")]
        output_filename = "_".join(str(s) for s in seiten) + ".pdf"
        output_pdf_path = os.path.join('./pdfs', output_filename)
        
        result_path = remove_unwanted_pages(file_path, seiten, output_pdf_path)
        success_label.config(text=f"PDF erstellt: {result_path}", fg="green")
    except ValueError:
        success_label.config(text="Fehler bei der Verarbeitung!", fg="red")

def upload_pdf():
    global file_label, file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_label.config(text=f"Ausgewählt: {os.path.basename(file_path)}")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Book Creator")
root.geometry("700x350")  # Größer gemacht für das neue Label

# Button zum Hochladen der PDF
tk.Label(root, text="").pack(pady=5)
btn_upload = tk.Button(root, text="PDF hochladen", command=upload_pdf)
btn_upload.pack(pady=10)

# Label, um den hochgeladenen Dateinamen anzuzeigen
file_label = tk.Label(root, text="Keine Datei ausgewählt")
file_label.pack(pady=0)

tk.Label(root, text="").pack(pady=10)

# Eingabefeld für den String
label = tk.Label(root, text="Welche Seiten sollen gelöscht werden (z.B. 1,13,22):").pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=10)

# Button zum Bestätigen des Textes
btn_submit = tk.Button(root, text="Bestätigen", command=submit_text)
btn_submit.pack(pady=10)

# Label, um die Bestätigung mit grünem Text anzuzeigen
confirm_label = tk.Label(root, text="")
confirm_label.pack(pady=2)

# Label für Erfolgsmeldung
success_label = tk.Label(root, text="")
success_label.pack(pady=2)

# Tkinter Loop starten
root.mainloop()


