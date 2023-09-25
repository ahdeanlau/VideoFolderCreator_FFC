import re
import os
import tkinter as tk
import _tkinter
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

def remove_first_8_chars_serial(serial_number):
    return serial_number[8:]

def simplify_server_name(server_name):
    """Simplify the server name. The cases are explicitly stated below. Welcome to add new cases if needed"""
    if server_name.isdigit():
        return "Other"
    elif re.search(r"footfall",server_name):
        return "FFC"
    else:
        return server_name

def get_folder_name():
    """Get the folder name from the input text from the text_area"""
    input_text = text_area.get("1.0", tk.END).strip()
    server = simplify_server_name(re.search(r"Server: ([^\n]+)", input_text).group(1).split("//")[-1].replace(".com","").replace(".", "").replace(":", "").replace("/", ""))
    company = re.search(r"Company: ([^\n]+)", input_text).group(1).replace(" ", "")
    firmware_version = re.search(r"Firmware Version: ([^\n]+)", input_text).group(1).replace(".", "")
    site = re.search(r"Site: ([^\n]+)", input_text).group(1).replace(" ", "")
    device_serial = remove_first_8_chars_serial(re.search(r"Device Serial: ([^\n]+)", input_text).group(1))

    # Create the folder name
    folder_name = f"{company}_{site}_{device_serial}_{server}_{firmware_version}"

    return folder_name

def create_folder():
    # Create the folder name
    folder_name = get_folder_name()

    # Show the synthesized folder name
    folder_name_label = tk.Label(frame, text=folder_name)
    folder_name_label.grid(row=5, column=0, sticky=tk.W)

    # Get the base directory
    base_directory = file_path_entry.get()

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

# GUI Method ---------------------------------------------------------------

def on_entry_click(event, message):
    """Function that gets called whenever entry is clicked."""
    if event.widget.get().strip() == message:
        event.widget.delete(0, tk.END)  # delete all the text in the entry
        event.widget.config(fg='black')  # change text color to black

def on_focusout(event, message):
    """Function that gets called when focus is moved out of entry field."""
    if not event.widget.get():
        event.widget.insert(0, message)
        event.widget.config(fg='grey')

def on_text_focus_in(message):
    if text_area.get("1.0", tk.END).strip() == message:
        text_area.delete("1.0", tk.END)  # delete all the text in the text widget
        text_area.config(fg='black')  # change text color to black

def on_text_focus_out(message):
    content = text_area.get("1.0", tk.END).strip()
    if not content:
        text_area.insert("1.0", message)
        text_area.config(fg='grey')

# GUI code-----------------------------------------------------------------
root = tk.Tk()
root.title("Folder Name Converter")

style = ttk.Style()

# Set global background color
style.configure('.', background='white')

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# To define directory location
file_path_label = ttk.Label(frame, text="Folder Path:")
file_path_label.grid(row=1, column=0, sticky=tk.W)

file_path_entry = tk.Entry(frame, width=40)
file_path_entry.insert(0, 'Enter file path here...')
file_path_entry.config(fg='grey')
instruction='Enter file path here...'
file_path_entry.bind('<FocusIn>', lambda event: on_entry_click(event, instruction))
file_path_entry.bind('<FocusOut>', lambda event: on_focusout(event, instruction))
file_path_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

button = ttk.Button(frame, text="Browse", command = get_directory_location)
button.grid(row=1, column=0, sticky=tk.E, pady=1)

# To insert video folder name information from Verification Tracker
sample_format = """Server: http://footfallcounter.com
Company: SOJAO
Firmware Version: 4.6.0
Company Serial: 15F010245232
Site: Joo Chiat Road
Device: Maindoor
Ceiling Height: 4.15
Device Serial: 1000000099acabaa
Videos Upload Time: 00:00 - 23:55
Local Date Time:"""

text_area = tk.Text(frame, wrap=tk.WORD, width=40, height=10)
text_area.insert("1.0", sample_format)
text_area.config(fg='grey')
text_area.bind('<FocusIn>', lambda event: on_text_focus_in(sample_format))
text_area.bind('<FocusOut>', lambda event: on_text_focus_out(sample_format))
text_area.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# To create video folder
button = ttk.Button(frame, text="Create Video Folder", command = create_folder)
button.grid(row=6, column=0, sticky=tk.W, pady=10)


root.mainloop()

