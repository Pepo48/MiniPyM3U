from PIL import Image
Image.CUBIC = Image.BICUBIC
from tkinter import filedialog, TclError, font as tkFont
import ttkbootstrap as tb
import subprocess, os, yaml, datetime, paramiko

# TODO: Refactor: Separate the business logic from the GUI code
def send_files():
    # Open a file dialog to select the files
    file_paths = filedialog.askopenfilenames(filetypes=[('M3U files', '*.m3u')], defaultextension='.m3u')
    
    # Get the directory where app.py is located
    app_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the path to conf.yaml relative to app_dir
    conf_path = os.path.join(app_dir, 'conf.yaml')

    # Read the parameters from conf.yaml
    if os.path.exists(conf_path):
        with open(conf_path, 'r') as f:
            conf = yaml.safe_load(f)
        ssh_conf = conf.get('ssh', {})
        hostname = ssh_conf.get('host')
        username = ssh_conf.get('user')
        password = ssh_conf.get('password')
        remote_path = ssh_conf.get('remote_path')

    # Create a new SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    # Create a new SFTP client
    sftp = ssh.open_sftp()

    # Send the files
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        sftp.put(file_path, os.path.join(remote_path, filename))

    # Close the SFTP and SSH clients
    sftp.close()
    ssh.close()

def on_generate_button_click():

    # Open a file dialog to select the output file
    now = datetime.datetime.now()
    initial_file_name = f"output_{now.strftime('%Y-%m-%d-%H-%M-%S')}.m3u"
    output_file = filedialog.asksaveasfilename(initialfile=initial_file_name, filetypes=[('M3U files', '*.m3u')], defaultextension='.m3u')
    # If the dialog is closed without selecting a file, output_file will be an empty string
    if not output_file:
        return
    
    # Get the values from the views
    sources = [sources_view.item(i, 'values')[0] for i in sources_view.get_children()]
    channel_names = [channels_view.item(i, 'values')[0] for i in channels_view.get_children()]
    similarity_ratio = meter.amountusedvar.get()

    # Convert the lists to strings with quotes around each item
    files_str = ' '.join(f'"{file}"' for file in sources)
    channel_names_str = ' '.join(f'"{channel_name}"' for channel_name in channel_names)

    # Prepare the command
    command = [
        "python", "m3u.py",
        "--urls", files_str,
        "--channel-names", channel_names_str,
        "--similarity-ratio", str(similarity_ratio),
        "--output-file", output_file,
        "--debug"
    ]

    # Convert the command list to a string
    command_str = ' '.join(command)
    print(f'Executing command: {command_str}')

    # Execute the command
    subprocess.run(command_str, check=True, shell=True)

def add_file():
    file_paths = filedialog.askopenfilenames(filetypes=[('M3U files', '*.m3u')])
    for file_path in file_paths:
        if file_path:
            sources_view.insert('', 'end', values=(file_path,))

def add_url():
    url = url_entry.get()
    if url:
        sources_view.insert('', 'end', values=(url,))
        url_entry.delete(0, 'end')

def add_channel():
    channel = url_entry.get()
    if channel:
        channels_view.insert('', 'end', values=(channel,))
        url_entry.delete(0, 'end')

def delete_selected():
    # Get selected items
    selected_items_list_view = sources_view.selection()
    selected_items_channels_view = channels_view.selection()

    # Delete selected items from list_view
    for item in selected_items_list_view:
        sources_view.delete(item)

    # Delete selected items from channels_view
    for item in selected_items_channels_view:
        channels_view.delete(item)

def copy_selected():
    # Get selected items
    selected_items_sources_view = sources_view.selection()
    selected_items_channels_view = channels_view.selection()

    # Initialize an empty list to store the values
    copied_values = []

    # Get the values of the selected items from sources_view
    for item in selected_items_sources_view:
        values = sources_view.item(item, 'values')
        copied_values.append(', '.join(str(v) for v in values))

    # Get the values of the selected items from channels_view
    for item in selected_items_channels_view:
        values = channels_view.item(item, 'values')
        copied_values.append(', '.join(str(v) for v in values))

    # Join the values with a newline character and copy to clipboard
    root.clipboard_clear()
    root.clipboard_append('\n'.join(copied_values))

# Function to paste text from the clipboard
def paste_text(event):
    try:
        text = root.clipboard_get()
        # Split the text at the newline character
        text_list = text.split('\n')
        for text in text_list:
            url_entry.delete(0, 'end')
            url_entry.insert(0, text)
            if event.widget == sources_view:
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
    context_menu.add_command(label="Copy", command=copy_selected)
    context_menu.add_command(label="Paste", command=lambda: paste_text(event))  
    context_menu.post(event.x_root, event.y_root)

# Function to clear the selection in the Treeviews
def deselect(event, sources_treeview, channels_treeview):
    # Get the item under the cursor
    item = sources_treeview.identify('item', event.x, event.y)
    # If the item is empty, clear the selection in both treeviews
    if not item:
        sources_treeview.selection_remove(sources_treeview.selection())
        channels_treeview.selection_remove(channels_treeview.selection())

def select_all(event):
    # Get the widget that currently has focus
    active_treeview = root.focus_get()
    # If the active widget is one of the Treeviews, select all items
    if active_treeview in [sources_view, channels_view]:
        active_treeview.selection_set(active_treeview.get_children())

def load_channels():
    # Get the directory where app.py is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the path to conf.yaml relative to app_dir
    conf_path = os.path.join(app_dir, 'conf.yaml')

    # Load the configuration from conf.yaml if it exists
    if os.path.exists(conf_path):
        with open(conf_path, 'r') as f:
            conf = yaml.safe_load(f)
            channels = conf.get('channels', [])
            for channel in channels:
                channels_view.insert('', 'end', values=(channel,))

root = tb.Window(themename='lumen')  # Change the theme
root.geometry('800x600')
root.title('MiniPyM3U')

# Change the default font size
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=13)

# Create frames
frame1 = tb.Frame(root)
frame1.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
frame2 = tb.Frame(root)
frame2.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
frame3 = tb.Frame(root)
frame3.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

# Button to add URL
add_url_button = tb.Button(frame1, text="Add URL", command=add_url)
add_url_button.grid(row=0, column=0, padx=10, pady=10)  # Placed in the first column

# Entry for URL or channel
url_entry = tb.Entry(frame1)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')  # Placed in the second column

# Button to add channel
add_channel_button = tb.Button(frame1, text="Add Channel", command=add_channel)
add_channel_button.grid(row=0, column=2, padx=10, pady=10)  # Placed in the third column

# Button to add file
add_file_button = tb.Button(frame2, text="Add File", command=add_file)
add_file_button.grid(row=0, column=0, padx=10, pady=10)  # Placed in the first column

# Meter
meter = tb.Meter(
    frame2,
    metersize=125,
    padding=5,
    amountused=25,
    metertype="semi",
    interactive=True,
    subtext="similarity ratio",
)
meter.configure(amountused = 95)
meter.grid(row=0, column=1, padx=10, pady=10, sticky='ew')  # Placed in the second column

# Button to delete selected item
delete_button = tb.Button(frame2, text="Delete Selected", command=delete_selected)
delete_button.grid(row=0, column=2, padx=10, pady=10)  # Placed in the third column

# List view
sources_view = tb.Treeview(frame3, columns=('Source',), show='headings')
sources_view.heading('Source', text='M3U Source')
sources_view.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Channels view
channels_view = tb.Treeview(frame3, columns=('Channels',), show='headings')
channels_view.heading('Channels', text='Channels')
channels_view.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Load the configuration from conf.yaml if it exists
load_channels()

# Generate M3U Playlist button
generate_button = tb.Button(root, text="Generate M3U Playlist", command=on_generate_button_click)
generate_button.grid(row=3, column=0, padx=10, pady=10)

# Send files button
send_files_button = tb.Button(root, text="Send Files", command=send_files)
send_files_button.grid(row=4, column=0, padx=10, pady=10)

# Bind the context menu to the list_view and channels_view
sources_view.bind("<Button-3>", show_context_menu)
channels_view.bind("<Button-3>", show_context_menu)
# Bind the deselect function to the Treeviews
sources_view.bind('<Button-1>', lambda event: deselect(event, sources_view, channels_view))
channels_view.bind('<Button-1>', lambda event: deselect(event, channels_view, sources_view))
# Bind Ctrl+V to paste_text function
root.bind('<Control-v>', paste_text)
# Bind Delete to delete_selected function
root.bind('<Delete>', lambda event: delete_selected())
# Bind Ctrl+C to copy_selected function
root.bind('<Control-c>', lambda event: copy_selected())
# Bind Ctrl+A to select_all function
root.bind('<Control-a>', select_all)

# Configure the row and column weights for the root window
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

# Configure the row and column weights for the frames
frame1.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame3.grid_columnconfigure(0, weight=1)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_rowconfigure(0, weight=1)

# Configure the row and column weights for the list views
sources_view.column('#0', stretch=tb.YES)
channels_view.column('#0', stretch=tb.YES)

root.mainloop()