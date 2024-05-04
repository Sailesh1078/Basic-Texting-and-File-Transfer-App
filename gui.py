from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, filedialog
import cv2
from PIL import Image, ImageTk
import threading

class GUI:
    def __init__(self, chat_client):
        self.chat_client = chat_client
        self.app = Tk()
        self.app.title("Video Conference App")

        # Label
        self.label = Label(self.app, text="Welcome to Video Conference App", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Text area for chat
        self.chat_text = Text(self.app, wrap="word", width=50, height=20)
        self.chat_text.pack(pady=10, padx=10)
        self.chat_text.config(state="disabled")  # Disable editing

        # Scrollbar for the chat text area
        self.scrollbar = Scrollbar(self.app, command=self.chat_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Entry for typing messages
        self.message_entry = Entry(self.app, width=40)
        self.message_entry.pack(pady=10)

        # Button to send messages
        self.send_button = Button(self.app, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Button to send files
        self.send_file_button = Button(self.app, text="Send File", command=self.send_file)
        self.send_file_button.pack(pady=5)

        # Label for video stream
        self.video_label = Label(self.app)
        self.video_label.pack()

        # OpenCV variables for video streaming
        self.cap = cv2.VideoCapture(0)  # Adjust the camera index if needed
        self.video_thread = threading.Thread(target=self.update_video)
        self.video_thread.start()

    def update_video(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                # Convert the OpenCV frame to ImageTk format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)

                # Update the video label with the new frame
                self.video_label.config(image=photo)
                self.video_label.image = photo

    def send_message(self):
        message = self.message_entry.get()
        self.chat_client.display_message(f"You: {message}")
        self.chat_client.client_socket.send(message.encode('utf-8'))

    def run(self):
        self.app.mainloop()
        self.cap.release()  # Release the video capture when the GUI is closed

    def send_file(self):
        self.chat_client.send_file()

    def display_message(self, message):
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", message + "\n")
        self.chat_text.config(state="disabled")
        self.message_entry.delete(0, "end")  # Clear the message entry
