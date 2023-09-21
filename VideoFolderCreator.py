import re
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def get_directory_location():
    # Open the folder selection dialog and get the selected folder path
    folder_selected = filedialog.askdirectory()
    
    # Check if a folder was selected
    if folder_selected:
        # Clear the current text in the entry
        file_path_entry.delete(0, tk.END)
        
        # Populate the entry with the selected folder path
        file_path_entry.insert(0, folder_selected)


def get_folder_name():
    input_text = text_area.get("1.0", tk.END).strip()
    server = re.search(r"Server: (http://[^\s]+)", input_text).group(1).split("//")[-1].replace(".", "").replace(":", "")
    company = re.search(r"Company: ([^\nFirmware]+)", input_text).group(1).replace(" ", "")
    firmware_version = re.search(r"Firmware Version: ([^\n]+)", input_text).group(1).replace(".", "")
    site = re.search(r"Site: ([^\nDevice]+)", input_text).group(1).replace(" ", "")
    device_serial = re.search(r"Device Serial: ([^\nVideos]+)", input_text).group(1).replace("00000000", "")
    
    # Create the folder name
    folder_name = f"{company}_{site}_{device_serial}_{server}_{firmware_version}"

    return folder_name

def create_folder():
    # Get the location for the directory
    base_directory = get_directory_location()
    
    if not base_directory:  # If the user cancels the directory selection
        return

    # Create the folder name
    folder_name = get_folder_name()

    # Create the full path
    full_path = os.path.join(base_directory, folder_name)

    # Create the folder
    try:
        os.makedirs(full_path)
        messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        messagebox.showerror("Error", f"Folder '{folder_name}' already exists.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_entry_click(event):
    """Function that gets called whenever entry is clicked."""
    if file_path_entry.get() == 'Enter file path here...':
        file_path_entry.delete(0, tk.END)  # delete all the text in the entry
        file_path_entry.config(fg='white')  # change text color to white

def on_focusout(event):
    """Function that gets called when focus is moved out of entry field."""
    if not file_path_entry.get():
        file_path_entry.insert(0, 'Enter file path here...')
        file_path_entry.config(fg='grey')


# GUI code
root = tk.Tk()
root.title("Folder Name Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# To define directory location
file_path_label = ttk.Label(frame, text="Folder Path:")
file_path_label.grid(row=1, column=0, sticky=tk.W)

file_path_entry = tk.Entry(frame, width=40)
file_path_entry.insert(2, 'Enter file path here...')
file_path_entry.config(fg='grey')
file_path_entry.bind('<FocusIn>', on_entry_click)
file_path_entry.bind('<FocusOut>', on_focusout)
file_path_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

button = ttk.Button(frame, text="Browse", command = get_directory_location)
button.grid(row=1, column=0, sticky=tk.E, pady=1)

# To insert video folder name information from Verification Tracker
text_area = tk.Text(frame, wrap=tk.WORD, width=40, height=10)
text_area.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# To create video folder
button = ttk.Button(frame, text="Create Video Folder", command = create_folder)
button.grid(row=5, column=0, sticky=tk.W, pady=10)

root.mainloop()
