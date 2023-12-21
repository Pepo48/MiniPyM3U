import os
import sys
import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from m3u_parser_package.compare_m3u import shrink_m3u

def select_file():
    filename = filedialog.askopenfilename()
    return filename

def on_scrollbar_released(event):
    # get the current position of the scrollbar
    scrollbar_position = scrollbar.get()
    # if the scrollbar is at the bottom, set auto_scroll to True
    if scrollbar_position[1] == 1.0:
        auto_scroll.set(True)

def on_scrollbar_moved(event):
    auto_scroll.set(False)

def process_file():
    m3u_file_path = select_file()
    txt_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "m3u_parser_package", "resources", "sports-channels-db.txt")
    output_file_path = "output.m3u"

    def is_scrollbar_at_bottom(text_widget):
        last_visible_index = text_widget.index("@0,%d" % text_widget.winfo_height())
        total_lines = int(text_widget.index(tk.END).split('.')[0])
        return int(last_visible_index.split('.')[0]) >= total_lines

    def callback(message, tag):
        # check if the tag is "fail" and the checkbox is unchecked
        if tag == "fail" and not show_fail.get():
            return
        log.insert(tk.END, message, tag)
        if is_scrollbar_at_bottom(log):
            auto_scroll.set(True)
        if auto_scroll.get():
            log.see(tk.END)
        root.update()

    shrink_m3u(txt_file_path, m3u_file_path, output_file_path, callback)

root = tk.Tk()
auto_scroll = tk.BooleanVar(root)
auto_scroll.set(True)
show_fail = tk.BooleanVar(root)
show_fail.set(False)
log = tk.Text(root, font=("TkDefaultFont", 14))
log.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)
scrollbar.bind("<B1-Motion>", on_scrollbar_moved)
scrollbar.bind("<ButtonRelease-1>", on_scrollbar_released)
log.tag_config("success", foreground="green", font=("TkDefaultFont", 14, "bold"))
log.tag_config("fail", foreground="red", font=("TkDefaultFont", 14))
button = tk.Button(root, text="Select M3U file", command=process_file)
button.pack()
checkbox = tk.Checkbutton(root, text="Show failed matches", variable=show_fail)
checkbox.pack()
root.mainloop()