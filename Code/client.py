# Import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime

# Constants for server connection
HOST = '127.0.0.1'
PORT = 1234

# Color and font settings for the GUI
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    """Add a message to the message box with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, f"[{timestamp}] {message}\n")
    message_box.config(state=tk.DISABLED)

def connect():
    """Connect to the chat server and send the username."""
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
        
        username = username_textbox.get()
        if username != '':
            client.sendall(username.encode())
            username_textbox.config(state=tk.DISABLED)
            username_button.config(state=tk.DISABLED)
            threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")
    except Exception as e:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}\nError: {e}")

def send_message():
    """Send a message to the chat server."""
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)  # Clear input after sending
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def save_chat():
    """Save the chat history to a text file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"),
                                                          ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                messages = message_box.get(1.0, tk.END)  # Get all text from message box
                file.write(messages)
            messagebox.showinfo("Success", "Chat saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat: {e}")

def save_chat():
    """Send request to the server to save chat history."""
    try:
        client.sendall("SAVE".encode())  # Send a save command to the server
        response = client.recv(2048).decode('utf-8')  # Wait for server response
        add_message(response)  # Display the server response (confirmation) in the chat box
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save chat: {e}")


def listen_for_messages_from_server(client):
    """Listen for messages from the server and display them."""
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split("~", 1)
                add_message(f"[{username}] {content}")
            else:
                break  # Exit loop if an empty message is received
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Main GUI setup
root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

# Frame configurations
top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# Username input section
username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame,
                            text="Join",
                            font=BUTTON_FONT,
                            bg=OCEAN_BLUE,
                            fg=WHITE,
                            command=connect)
username_button.pack(side=tk.LEFT, padx=15)

# Message input section
message_textbox = tk.Entry(bottom_frame,
                           font=FONT,
                           bg=MEDIUM_GREY,
                           fg=WHITE,
                           width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame,
                           text="Send",
                           font=BUTTON_FONT,
                           bg=OCEAN_BLUE,
                           fg=WHITE,
                           command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

# Save chat button (this is where the save functionality is integrated)
save_button = tk.Button(bottom_frame,
                        text="Save Chat",
                        font=BUTTON_FONT,
                        bg=OCEAN_BLUE,
                        fg=WHITE,
                        command=save_chat)  # This button calls save_chat function when clicked
save_button.pack(side=tk.LEFT, padx=10)

# Message display area
message_box = scrolledtext.ScrolledText(middle_frame,
                                         font=SMALL_FONT,
                                         bg=MEDIUM_GREY,
                                         fg=WHITE,
                                         width=67,
                                         height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

# Start the main loop
def main():
    root.mainloop()

if __name__ == '__main__':
    main()