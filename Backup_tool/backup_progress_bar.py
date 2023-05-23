import shutil
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import zipfile



# Define the source and destination directories
source_dir = ''
dest_dir = ''

def select_source_dir():
    global source_dir
    source_dir = filedialog.askdirectory()
    source_label.config(text='Source directory: ' + source_dir)

def select_dest_dir():
    global dest_dir
    dest_dir = filedialog.askdirectory()
    dest_label.config(text='Destination directory: ' + dest_dir)

def backup_data():
    global stop_backup
    stop_backup = False
    backup_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    source_button.config(state=tk.DISABLED)
    dest_button.config(state=tk.DISABLED)
    backup_thread = threading.Thread(target=start_backup)
    backup_thread.start()

def start_backup():
    # Generate a timestamp for the backup file
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')

    # Create a name for the backup file
    backup_name = 'backup_{}.zip'.format(timestamp)

    # Get the total size of the source directory
    total_size = sum(os.path.getsize(os.path.join(root, file))
                     for root, dirs, files in os.walk(source_dir)
                     for file in files)

    # Initialize the count variable for progress bar
    count = 0

    # Compress the source directory into a zip file
    with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, source_dir))
                count += os.path.getsize(file_path)
                update_progress(count, total_size)

                # Check if the stop button is clicked
                if stop_backup:
                    result_label.config(text='Backup stopped.')
                    backup_button.config(state=tk.NORMAL)
                    stop_button.config(state=tk.DISABLED)
                    source_button.config(state=tk.NORMAL)
                    dest_button.config(state=tk.NORMAL)
                    return

    # Move the compressed backup file to the destination directory
    shutil.move(backup_name, dest_dir)

    if not stop_backup:
        backup_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        source_button.config(state=tk.NORMAL)
        dest_button.config(state=tk.NORMAL)
        result_label.config(text='Backup created successfully!')


def stop_program():
    global stop_backup
    stop_backup = True
    result_label.config(text='Backup stopped.')
    backup_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    source_button.config(state=tk.NORMAL)
    dest_button.config(state=tk.NORMAL)

# Create the GUI interface
root = tk.Tk()
root.title('Backup Data')

source_button = tk.Button(root, text='Select Source Directory', command=select_source_dir)
source_button.pack()

source_label = tk.Label(root, text='Source directory: ' + source_dir)
source_label.pack()

dest_button = tk.Button(root, text='Select Destination Directory', command=select_dest_dir)
dest_button.pack()

dest_label = tk.Label(root, text='Destination directory: ' + dest_dir)
dest_label.pack()

backup_button = tk.Button(root, text='Backup Data', command=backup_data)
backup_button.pack()

stop_button = tk.Button(root, text='Stop Program', command=stop_program, state=tk.DISABLED)
stop_button.pack()

result_label = tk.Label(root, text='')
result_label.pack()

progress = ttk.Progressbar(root, orient='horizontal', length=250, mode='determinate')
progress.pack()

def update_progress(count, total):
    progress['value'] = int((count / total) * 100)
    root.update_idletasks()

root.mainloop()
