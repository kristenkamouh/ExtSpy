import tkinter as tk
from tkinter import PhotoImage, filedialog, messagebox, ttk
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

# Set up the main application window
window = tk.Tk()
window.title('Extension Checker')
window.geometry('300x150')

# Change the background color of the window
window.configure(bg='#8a99db')  # Light blue color

# Set the window icon
base_path = os.path.dirname(__file__)
logo = PhotoImage(file=os.path.join(base_path, "./extension-cord.png"))
window.iconphoto(False, logo)

# Set up the label
tk.Label(window, text='Select a folder to scan for file types:', bg='#8a99db').pack(pady=10)

# Set up the browse button with a different color
browse_button = tk.Button(window, text="Browse", command=browse_folder, bg='#f1f2a2', fg='black') 
browse_button.pack(pady=5)

# Set up the progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', length=250, mode='determinate')
progress_bar.pack(pady=5)

# Set up the result label
result_label = tk.Label(window, text='', bg='#8a99db')
result_label.pack(pady=5)

# Start the application loop
window.mainloop()
