import shutil
import os
import subprocess
import tkinter as tk
from urllib import request
from urllib.parse import urlparse
import base64
import webbrowser
from tkinter.scrolledtext import ScrolledText
from bs4 import BeautifulSoup
import tkinter.filedialog as filedialog

root = tk.Tk()
root.title("RetroNet Terminal REPL")
root.configure(bg='black')
root.resizable(False, False)  # Make the root window not resizable

output_text = ScrolledText(root, width=80, height=20, bg='black', fg='green')
output_text.pack()

command_entry = tk.Entry(root, width=80, bg='black', fg='green')
command_entry.pack()

browser_window = tk.Toplevel(root)
browser_window.title("TUI Browser")
browser_window.configure(bg='black')
browser_window.resizable(False, False)  # Make the browser window not resizable

browser_text = ScrolledText(browser_window, width=80, height=20, bg='black', fg='green')
browser_text.pack()

def execute_command():
    command = command_entry.get()
    output_text.insert(tk.END, f"$ {command}\n")

    parts = command.split(' ')
    cmd = parts[0]
    args = parts[1:]

    if cmd == 'ls':
        try:
            files = os.listdir(os.getcwd())
            output = '\n'.join(files)
        except OSError as e:
            output = str(e)
    elif cmd == 'pwd':
        output = os.getcwd()
    elif cmd == 'cd':
        try:
            os.chdir(args[0])
            output = ""
        except OSError as e:
            output = str(e)
    elif cmd == 'cat':
        try:
            output = subprocess.check_output(['cat'] + args).decode().strip()
        except subprocess.CalledProcessError as e:
            output = e.output.decode().strip()
    elif cmd == 'tui_browser':
        if len(args) != 1:
            output = 'Usage: tui_browser <url>'
        else:
            url = args[0]
            try:
                response = request.urlopen(url)
                content = response.read().decode()
                soup = BeautifulSoup(content, 'html.parser')
                rendered_text = soup.get_text()
                browser_text.delete('1.0', tk.END)
                browser_text.insert(tk.END, rendered_text)
                browser_text.see(tk.END)
                output = ''
            except request.URLError as e:
                output = f"Error accessing URL: {e.reason}"
    elif cmd == 'open_browser':
        if len(args) != 1:
            output = 'Usage: open_browser <url>'
        else:
            url = args[0]
            webbrowser.open(url)
            output = f"Opening web page in default browser: {url}"
    elif cmd == 'make_file':
        if len(args) != 1:
            output = 'Usage: make_file <filename>'
        else:
            filename = args[0]
            try:
                with open(filename, 'w') as file:
                    file.write('')
                output = f"File created: {filename}"
            except Exception as e:
                output = f"Error creating file: {str(e)}"
    elif cmd == 'encode_base64':
        if len(args) != 1:
            output = 'Usage: encode_base64 <text>'
        else:
            text = args[0]
            try:
                encoded_text = base64.b64encode(text.encode()).decode()
                output = f"Base64 encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding Base64: {str(e)}"
    elif cmd == 'decode_base64':
        if len(args) != 1:
            output = 'Usage: decode_base64 <encoded_string>'
        else:
            encoded_string = args[0]
            try:
                decoded_text = base64.b64decode(encoded_string).decode()
                output = f"Base64 decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding Base64: {str(e)}"
    elif cmd == 'encode_rot13':
        if len(args) != 1:
            output = 'Usage: encode_rot13 <text>'
        else:
            text = args[0]
            try:
                encoded_text = text.encode().decode('rot13')
                output = f"ROT13 encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding ROT13: {str(e)}"
    elif cmd == 'decode_rot13':
        if len(args) != 1:
            output = 'Usage: decode_rot13 <encoded_string>'
        else:
            encoded_string = args[0]
            try:
                decoded_text = encoded_string.encode().decode('rot13')
                output = f"ROT13 decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding ROT13: {str(e)}"
    elif cmd == 'encode_hex':
        if len(args) != 1:
            output = 'Usage: encode_hex <text>'
        else:
            text = args[0]
            try:
                encoded_text = text.encode().hex()
                output = f"Hex encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding Hex: {str(e)}"
    elif cmd == 'curl':
        if len(args) != 1:
            output = 'Usage: curl <url>'
        else:
            url = args[0]
            try:
                response = request.urlopen(url)
                filename = os.path.basename(urlparse(url).path)
                with open(filename, 'wb') as file:
                    shutil.copyfileobj(response, file)
                output = f"Downloaded and saved: {filename}"
            except request.URLError as e:
                output = f"Error accessing URL: {e.reason}"
    elif cmd == 'decode_hex':
        if len(args) != 1:
            output = 'Usage: decode_hex <hex_string>'
        else:
            hex_string = args[0]
            try:
                decoded_text = bytes.fromhex(hex_string).decode()
                output = f"Hex decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding Hex: {str(e)}"
    elif cmd == 'encode_rot47':
        if len(args) != 1:
            output = 'Usage: encode_rot47 <text>'
        else:
            text = args[0]
            try:
                encoded_text = ''.join(chr((ord(c) - 33 + 47) % 94 + 33) for c in text)
                output = f"ROT47 encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding ROT47: {str(e)}"
    elif cmd == 'decode_rot47':
        if len(args) != 1:
            output = 'Usage: decode_rot47 <encoded_string>'
        else:
            encoded_string = args[0]
            try:
                decoded_text = ''.join(chr((ord(c) - 33 + 47) % 94 + 33) for c in encoded_string)
                output = f"ROT47 decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding ROT47: {str(e)}"
    elif cmd == 'encode_base32':
        if len(args) != 1:
            output = 'Usage: encode_base32 <text>'
        else:
            text = args[0]
            try:
                encoded_text = base64.b32encode(text.encode()).decode()
                output = f"Base32 encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding Base32: {str(e)}"
    elif cmd == 'decode_base32':
        if len(args) != 1:
            output = 'Usage: decode_base32 <encoded_string>'
        else:
            encoded_string = args[0]
            try:
                decoded_text = base64.b32decode(encoded_string).decode()
                output = f"Base32 decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding Base32: {str(e)}"
    elif cmd == 'text_editor':
        text_editor()
        output = ''
    elif cmd == 'encode_url':
        if len(args) != 1:
            output = 'Usage: encode_url <text>'
        else:
            text = args[0]
            try:
                encoded_text = request.quote(text)
                output = f"URL encoded: {encoded_text}"
            except Exception as e:
                output = f"Error encoding URL: {str(e)}"
    elif cmd == 'decode_url':
        if len(args) != 1:
            output = 'Usage: decode_url <encoded_string>'
        else:
            encoded_string = args[0]
            try:
                decoded_text = request.unquote(encoded_string)
                output = f"URL decoded: {decoded_text}"
            except Exception as e:
                output = f"Error decoding URL: {str(e)}"
    elif cmd == 'help':
        output = '''
Available commands:
- curl: <url_of_the_file> Download a file from a url.
- ls: List files and directories
- pwd: Show current working directory
- cd <directory>: Change directory
- cat <file>: Display file contents
- tui_browser <url>: Open web page in TUI browser
- open_browser <url>: Open web page in default browser
- text_editor: Make a file and then edit it
- encode_base64 <text>: Encode text in Base64
- decode_base64 <encoded_string>: Decode Base64 encoded string
- encode_rot13 <text>: Encode text using ROT13 cipher
- decode_rot13 <encoded_string>: Decode ROT13 encoded string
- encode_hex <text>: Encode text in Hex
- decode_hex <hex_string>: Decode Hex encoded string
- encode_rot47 <text>: Encode text using ROT47 cipher
- decode_rot47 <encoded_string>: Decode ROT47 encoded string
- encode_base32 <text>: Encode text in Base32
- decode_base32 <encoded_string>: Decode Base32 encoded string
- encode_url <text>: Encode text as a URL
- decode_url <encoded_string>: Decode URL encoded string
- help: Show available commands
- exit: Exit the terminal
'''
    elif cmd == 'exit':
        root.quit()
    else:
        output = f"Unknown command: {cmd}"

    output_text.see(tk.END)  # Scroll to the end of the text widget
    output_text.insert(tk.END, output + '\n')
    command_entry.delete(0, tk.END)
def text_editor():
    filename = filedialog.asksaveasfilename()
    if filename:
        editor_window = tk.Toplevel(root)
        editor_window.title("Text Editor")
        editor_window.configure(bg='black')
        editor_window.resizable(True, True)  # Allow resizing of the editor window

        editor_text = ScrolledText(editor_window, width=80, height=20, bg='black', fg='green')
        editor_text.pack()

        def save_file():
            content = editor_text.get('1.0', tk.END)
            with open(filename, 'w') as file:
                file.write(content)
            editor_window.destroy()

        save_button = tk.Button(editor_window, text="Save", command=save_file, bg='black', fg='green')
        save_button.pack()
output_text.insert(tk.END, "1st Edition RetroNet \n")
output_text.insert(tk.END, "Type help... for help. \n")
output_text.insert(tk.END, "Visit the [REDACTED]")
output_text.insert(tk.END, "\n")
# Bind the Enter key to execute the command
root.bind('<Return>', lambda e: execute_command())

# Start the main event loop
root.mainloop()