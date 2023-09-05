import re
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def convert_to_folder_name():
    input_text = text_area.get("1.0", tk.END).strip()
    server = re.search(r"Server: (http://[^\s]+)", input_text).group(1).split("//")[-1].replace(".", "").replace(":", "")
    company = re.search(r"Company: ([^\nFirmware]+)", input_text).group(1).replace(" ", "")
    firmware_version = re.search(r"Firmware Version: ([^\n]+)", input_text).group(1).replace(".", "")
    site = re.search(r"Site: ([^\nDevice]+)", input_text).group(1).replace(" ", "")
    device_serial = re.search(r"Device Serial: ([^\nVideos]+)", input_text).group(1).replace("00000000", "")

    folder_name = f"{company}_{site}_{device_serial}_{server}_{firmware_version}"
    
    try:
        os.makedirs(folder_name)
        messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        messagebox.showerror("Error", f"Folder '{folder_name}' already exists.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI code
root = tk.Tk()
root.title("Folder Name Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

text_area = tk.Text(frame, wrap=tk.WORD, width=40, height=10)
text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

button = ttk.Button(frame, text="Convert to Folder Name", command=convert_to_folder_name)
button.grid(row=1, column=0, sticky=tk.W, pady=10)

root.mainloop()
