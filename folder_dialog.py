from tkinter import filedialog

def select_folder(location, callback=None):
    """Select a folder and return the path"""
    folder_selected = filedialog.askdirectory(initialdir=location) # Open the folder selection dialog
    # print(f'Folder Selected: {folder_selected}')
    if callback is not None:
        callback()
