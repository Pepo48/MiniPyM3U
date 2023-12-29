import tkinter as tk
from tkinter import filedialog
from m3u import check_m3u_files

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.m3u*"), ("all files", "*.*")))
    file_label.config(text="File Selected: " + filename)
    return filename

def run_script():
    m3u_file = browse_files()
    check_m3u_files(m3u_file)
    result_label.config(text="Processing completed")

window = tk.Tk()

window.title('M3U Parser')

file_label = tk.Label(window, text = "No File Selected")
file_label.pack()

browse_button = tk.Button(window, text = "Browse Files", command = browse_files)
browse_button.pack()

run_button = tk.Button(window, text = "Run Script", command = run_script)
run_button.pack()

result_label = tk.Label(window, text = "")
result_label.pack()

window.mainloop()