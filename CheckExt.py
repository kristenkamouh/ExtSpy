import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import magic 

def get_file_type(file_path):
    try:
        # Use magic to determine the MIME type
        mime_type = magic.from_file(file_path, mime=True)
        # Extract the extension from the MIME type
        if mime_type:
            file_extension = mime_type.split('/')[-1]  # Get the part after the '/'
            return file_extension
        else:
            return "Unknown"
    except Exception as e:
        return f"Error: {e}"

def browse_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return  # User canceled the folder selection
    
    output_file = filedialog.asksaveasfilename(
        defaultextension=".txt", 
        filetypes=[("Text files", "*.txt")], 
        title="Choose the name and where to save the txt file."
    )
    if not output_file:
        return  # User canceled the file save location selection
    
    try:
        total_files = sum([len(files) for _, _, files in os.walk(folder_path)])
        progress_bar['maximum'] = total_files

        with open(output_file, "w") as f:
            count = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_type = get_file_type(file_path)
                    absolute_path = os.path.abspath(file_path)
                    f.write(f"{absolute_path}, {file_type}\n")
                    count += 1
                    progress_bar['value'] = count
                    window.update_idletasks()

        result_label.config(text="Scanning Done!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

window = tk.Tk()
window.title('File Type Checker')
window.geometry('300x150')

tk.Label(window, text='Select a folder to scan for file types:').pack(pady=10)

browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

progress_bar = ttk.Progressbar(window, orient='horizontal', length=250, mode='determinate')
progress_bar.pack(pady=5)

result_label = tk.Label(window, text='')
result_label.pack(pady=5)

window.mainloop()
