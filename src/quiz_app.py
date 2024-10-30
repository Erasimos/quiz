import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
selected_file = None


def new_quiz():
    global selected_file
    try:
        result = subprocess.run(['python', script_directory + '/new_quiz.py'], capture_output=True, text=True)
        new_quiz_file = os.path.abspath(os.path.normpath(result.stdout.strip()))
        selected_file = new_quiz_file
        file_label.config(text=f'Selected File: {selected_file}')
        print(new_quiz_file)
        subprocess.Popen(['notepad.exe', new_quiz_file])     
        subprocess.Popen(['explorer', f'/select,{new_quiz_file}'])
    except Exception as e:
        messagebox.showerror('Error', f'Failed to run script: {e}')

def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_label.config(text=f'Selected File: {selected_file}')

def generate_quiz():
    return
    if selected_file:
        try:
            subprocess.run(['python', 'quiz.py', selected_file])
        except Exception as e:
            messagebox.showerror('Error', f'Failed to run script with file: {e}')
    else:
        messagebox.showwarning('Warning', 'No file selected!')

root = tk.Tk()
root.title("Rasmus Quiz Tool")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

button_new_quiz = tk.Button(root, text='Create New Quiz', command=new_quiz)
button_new_quiz.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

button_select_file = tk.Button(root, text='Select File', command=select_file)
button_select_file.grid(row=2, column=0, padx=10, pady=10, sticky='sw')

file_label = tk.Label(root, text='No file selected')
file_label.grid(row=2, column=1, padx=10, pady=10, sticky='sw')

button_generate_quiz = tk.Button(root, text='Generate Quiz', command=generate_quiz)
button_generate_quiz.grid(row=3, column=0, padx=10, pady=10, sticky='sw')

root.mainloop()