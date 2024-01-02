from PIL import Image
Image.CUBIC = Image.BICUBIC
from tkinter import filedialog, TclError
import ttkbootstrap as tb

def add_file():
    file_path = filedialog.askopenfilename(filetypes=[('M3U files', '*.m3u')])
    if file_path:
        list_view.insert('', 'end', values=(file_path,))

def add_url():
    url = url_entry.get()
    if url:
        list_view.insert('', 'end', values=(url,))
        url_entry.delete(0, 'end')

def add_channel():
    channel = url_entry.get()
    if channel:
        channels_view.insert('', 'end', values=(channel,))
        url_entry.delete(0, 'end')

def delete_selected():
    # Get selected items
    selected_item_list_view = list_view.selection()
    selected_item_channels_view = channels_view.selection()

    # Delete selected item from list_view
    if selected_item_list_view:
        list_view.delete(selected_item_list_view)

    # Delete selected item from channels_view
    if selected_item_channels_view:
        channels_view.delete(selected_item_channels_view)

# Function to paste text from the clipboard
def paste_text(event):
    try:
        text = root.clipboard_get()
        # Split the text at the newline character and only use the first part
        text = text.split('\n')[0]
        url_entry.delete(0, 'end')
        url_entry.insert(0, text)
        if event.widget == list_view:
            add_url()  # Call add_url if the event occurred on list_view
        elif event.widget == channels_view:
            add_channel()  # Call add_channel if the event occurred on channels_view
    except TclError:
        pass  # No text in the clipboard

# Function to show context menu
def show_context_menu(event):
    # Create a context menu
    context_menu = tb.Menu(root, tearoff=0)
    context_menu.add_command(label="Remove", command=delete_selected)
    context_menu.add_command(label="Paste Text", command=lambda: paste_text(event))  # Add paste_text command
    context_menu.post(event.x_root, event.y_root)

root = tb.Window(themename='lumen')
root.geometry('800x600')
root.title('MiniPyM3U')
root.style.configure('TButton', font=('Helvetica', 14))  # Increase font size for buttons
root.style.configure('TEntry', font=('Helvetica', 14))  # Increase font size for entry fields

# Create a context menu
context_menu = tb.Menu(root, tearoff=0)
context_menu.add_command(label="Remove", command=delete_selected)

# Entry for URL or channel
url_entry = tb.Entry(root)
url_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# Button to add URL
add_url_button = tb.Button(root, text="Add URL", command=add_url)
add_url_button.grid(row=0, column=2, padx=10, pady=10)

# Button to add channel
add_channel_button = tb.Button(root, text="Add Channel", command=add_channel)
add_channel_button.grid(row=0, column=3, padx=10, pady=10)

# Meter
meter = tb.Meter(
    metersize=125,
    padding=5,
    amountused=25,
    metertype="semi",
    interactive=True,
    subtext="similarity ratio",
)
meter.configure(amountused = 70)
meter.grid(row=1, column=0, padx=10, pady=10)

# Button to add file
add_file_button = tb.Button(root, text="Add File", command=add_file)
add_file_button.grid(row=1, column=1, padx=10, pady=10)

# Button to delete selected item
delete_button = tb.Button(root, text="Delete Selected", command=delete_selected)
delete_button.grid(row=1, column=2, columnspan=3, padx=10, pady=10)

# List view
list_view = tb.Treeview(root, columns=('Source',), show='headings')
list_view.heading('Source', text='M3U Source')
list_view.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Channels view
channels_view = tb.Treeview(root, columns=('Channels',), show='headings')
channels_view.heading('Channels', text='Channels')
channels_view.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky='nsew')

# Bind the context menu to the list_view and channels_view
list_view.bind("<Button-3>", show_context_menu)
channels_view.bind("<Button-3>", show_context_menu)
# Bind Ctrl+V to paste_text function
root.bind('<Control-v>', paste_text)
# Bind Delete to delete_selected function
root.bind('<Delete>', lambda event: delete_selected())

# Configure the row and column weights
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(2, weight=1)

root.mainloop()