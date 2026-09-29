import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 1234  # You can use any port between 0 and 65535
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users
clients_lock = threading.Lock()  # Lock to ensure thread-safety for active_clients
chat_history = []  # List to store all the chat messages

# # Function to listen for upcoming messages from a client
# def listen_for_messages(client, username):
#     while True:
#         try:
#             message = client.recv(2048).decode('utf-8')
#             if message:
#                 final_msg = username + '~' + message
#                 chat_history.append(final_msg)  # Save the message to chat history
#                 send_messages_to_all(final_msg)
#             else:
#                 break  # Client has disconnected
#         except Exception as e:
#             print(f"Error receiving message from {username}: {e}")
#             break

#     # Handle client disconnection
#     remove_client(client, username)



# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    log_file_path = "server_log.txt"  # Define the path for the log file
    
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = username + '~' + message
                
                # Append the message to the log file
                with open(log_file_path, 'a') as log_file:
                    log_file.write(final_msg + '\n')
                
                chat_history.append(final_msg)  # Save the message to chat history
                send_messages_to_all(final_msg)
            else:
                break  # Client has disconnected
        except Exception as e:
            print(f"Error receiving message from {username}: {e}")
            break

    # Handle client disconnection
    remove_client(client, username)


# Function to send message to a single client
def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except:
        pass  # Ignore errors when sending message to disconnected clients

# Function to send any new message to all the clients that are currently connected
def send_messages_to_all(message):
    with clients_lock:  # Ensure thread-safe access to active_clients
        for username, client in active_clients:
            send_message_to_client(client, message)

# Function to handle client connection and authentication
def client_handler(client):
    username = ''
    
    while True:
        try:
            # Server listens for the client's username
            username = client.recv(2048).decode('utf-8')
            if username and not is_username_taken(username):
                with clients_lock:  # Add client to the active_clients list in a thread-safe way
                    active_clients.append((username, client))
                prompt_message = f"SERVER~{username} has joined the chat."
                send_messages_to_all(prompt_message)
                break
            else:
                # If username is empty or taken, ask again
                client.sendall("SERVER~Invalid or duplicate username. Try again.".encode())
        except Exception as e:
            print(f"Error during username handling: {e}")
            client.close()
            return
    
    # Start listening for messages from this client
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# Function to remove client from the active_clients list
def remove_client(client, username):
    with clients_lock:
        active_clients[:] = [(user, c) for user, c in active_clients if c != client]

    # Notify other clients about the disconnection
    disconnect_message = f"SERVER~{username} has left the chat."
    send_messages_to_all(disconnect_message)
    client.close()

# Function to check if a username is already taken
def is_username_taken(username):
    with clients_lock:
        return any(user == username for user, _ in active_clients)

# Function to save the chat history to a file
def save_chat_history():
    # Define the file path where the chat history will be saved
    file_path = "chat_history.txt"
    
    try:
        with open(file_path, 'w') as f:
            for message in chat_history:
                f.write(message + "\n")
        print(f"Chat history saved to {file_path}")
    except Exception as e:
        print(f"Error saving chat history: {e}")

# Function to handle save request from the client
def handle_save_request(client):
    # When a client requests to save chat, save the history
    save_chat_history()
    client.sendall("SERVER~Chat history saved successfully.".encode())

# Main function
def main():
    # Creating the socket class object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Provide the server with an address in the form of host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}. Error: {e}")
        return

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening for client connections
    while True:
        try:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]}:{address[1]}")

            # Handle client connection in a separate thread
            threading.Thread(target=client_handler, args=(client,)).start()

        except Exception as e:
            print(f"Error accepting client connection: {e}")

if __name__ == '__main__':
    main()
