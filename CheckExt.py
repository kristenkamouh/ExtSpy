
import tkinter
import tkinter as tk
from tkinter import filedialog
import os
import imghdr


def get_file_type(file_path):

    file_type = imghdr.what(file_path)
    with open(file_path, 'rb') as file:
            file_signature = file.read(4)  # Read the first 4 bytes of the file

    if file_signature == b'%PDF':
            return "PDF"
    else:
        return file_type


def browse_folder():
    folder_path = filedialog.askdirectory()
    output_file = "file_types.txt"

    with open(output_file, "w") as f:
        for root, dirs, files in os.walk(folder_path):
            # absolute_path = os.path.abspath(root)  # Get the absolute path of the subfolder
            # subfolder_name = os.path.basename(root) # Get the name of the subfolder
            # f.write(f"{os.path.join(absolute_path)}\n")

            for file in files:
                file_path = os.path.join(root, file)
                file_type = get_file_type(file_path)
                absolute_path = os.path.abspath(file_path)
                f.write(f"{absolute_path},{file_type}\n")


    result_label.config(text="\nOutput found in file_types.txt")


window = tk.Tk()
window.title('Ext Checker')
window.geometry('250x100')

tkinter.Label(window, text='').pack()

browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack()

result_label = tk.Label(window, text='')
result_label.pack()

window.mainloop()
