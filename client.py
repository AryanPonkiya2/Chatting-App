import tkinter as tk
from tkinter import messagebox

def start_chat():
    clear_screen()
    chat_frame = tk.Frame(root)
    chat_frame.pack(pady=10)

    tk.Label(chat_frame, text="Chat Room", font=("Helvetica", 16)).pack()
    tk.Text(chat_frame, height=10, width=50).pack()
    tk.Entry(chat_frame, width=50).pack(pady=5)
    tk.Button(chat_frame, text="Send", command=lambda: messagebox.showinfo("Send", "Message Sent")).pack()

def view_scores():
    clear_screen()
    scores_frame = tk.Frame(root)
    scores_frame.pack(pady=10)

    tk.Label(scores_frame, text="Scores", font=("Helvetica", 16)).pack()
    tk.Label(scores_frame, text="User1: 10").pack()
    tk.Label(scores_frame, text="User2: 8").pack()
    tk.Button(scores_frame, text="Back to Menu", command=main_menu).pack(pady=5)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def main_menu():
    clear_screen()
    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=10)

    tk.Label(menu_frame, text="Main Menu", font=("Helvetica", 16)).pack()
    tk.Button(menu_frame, text="Start Chat", command=start_chat).pack(pady=5)
    tk.Button(menu_frame, text="View Scores", command=view_scores).pack(pady=5)
    tk.Button(menu_frame, text="Exit", command=root.quit).pack(pady=5)

# Main application window
root = tk.Tk()
root.title("Chat Application")
main_menu()  # Show the main menu

root.mainloop()
