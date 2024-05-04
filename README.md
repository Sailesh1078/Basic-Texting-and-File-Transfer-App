# Basic Texting and File Transfer App

This project implements a basic messaging and file transfer application using socket programming in Python. It allows communication between two laptops connected over a local network.

## Features

1. **Text Messaging**: Users can send text messages to each other in real-time.
2. **File Transfer**: Users can send files (e.g., images, documents) to each other.
3. **Simple Interface**: The interface provides an intuitive way to send messages and files.

## Components

### 1. Server

- The server component listens for incoming connections from clients.
- It manages the routing of messages and file transfer requests between clients.

### 2. Client

- The client component connects to the server to send and receive messages.
- It provides a user interface for composing and sending messages, as well as selecting and sending files.

## How It Works

1. **Server Setup**: One laptop acts as the server, listening for incoming connections on a specified port.
2. **Client Setup**: The other laptop acts as the client, connecting to the server's IP address and port.
3. **Text Messaging**: Clients can send text messages by typing in the message box and clicking "Send."
4. **File Transfer**: Clients can send files by selecting the file using the file picker and clicking "Send File."
