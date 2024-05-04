import socket
import threading
import os
import cv2
import numpy as np

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5555))
        self.server_socket.listen()

        self.clients = []
        self.video_clients = []

    def start(self):
        print("Server is listening for connections...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.clients.append(client_socket)
            self.video_clients.append(client_socket)  # Add the client to the video client list

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Check if the data is a file request or content
                if data.startswith("FILE_REQUEST"):
                    self.handle_file_request(client_socket, data)
                elif data.startswith("FILE_CONTENT"):
                    self.handle_file_content(client_socket, data)
                else:
                    print(f"Received data: {data}")

                # Broadcast the message to all clients
                self.broadcast_message(data, client_socket)

            except:
                break

    def handle_file_request(self, client_socket, data):
        # Extract the file name from the data
        file_name = data.split(":")[1]

        # Send acknowledgment to the client
        client_socket.send("FILE_ACK".encode('utf-8'))

        # Broadcast the file request to all clients (excluding the requester)
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(f"FILE_REQUEST:{file_name}".encode('utf-8'))
                except:
                    # Remove broken connections
                    self.clients.remove(client)

    def handle_file_content(self, client_socket, data):
        # Extract the file name and content from the data
        parts = data.split(":")
        file_name = parts[1]
        file_content = parts[2]

        # Save the file content to a file
        file_path = os.path.join("received_files", file_name)
        with open(file_path, 'ab') as file:  # Use binary mode
            file.write(file_content.encode('utf-8'))

    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    # Remove broken connections
                    self.clients.remove(client)

        # Broadcast video frames to all video clients
        self.broadcast_video(sender_socket)

    def broadcast_video(self, sender_socket):
        try:
            _, frame = sender_socket.recv(4096), None

            # Receive video frames from the sender
            while True:
                data = sender_socket.recv(4096)
                if not data:
                    break
                frame = frame + data

            # Send the video frame to all video clients
            for client in self.video_clients:
                if client != sender_socket:
                    try:
                        client.sendall(frame)
                    except:
                        # Remove broken connections
                        self.video_clients.remove(client)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    server = ChatServer()
    server.start()
