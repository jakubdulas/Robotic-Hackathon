import asyncio
import websockets
import base64
import cv2
import numpy as np
import threading
import keyboard  # Import the keyboard library
from remote_controller import send_command
import socket


# Global variable to store the text to send
# text_to_send = ""
# text_lock = threading.Lock()  # Lock for thread-safe access to text_to_send


# # Function to capture keyboard input
# def capture_keyboard_input():
#     global text_to_send
#     while True:
#         if keyboard.is_pressed():  # Check if any key is pressed
#             key = keyboard.read_event()  # Read the key event
#             if key.event_type == keyboard.KEY_DOWN:  # Check if it's a key down event
#                 text = key.name  # Get the name of the key pressed
#                 if len(text) == 1:  # Only consider single character inputs
#                     with text_lock:
#                         text_to_send = text  # Update the text to send


async def send_text_and_receive_frames():
    uri = "ws://192.168.0.114:8000/ws"  # Connect to the text WebSocket
    async with websockets.connect(uri) as websocket:
        while True:
            # Send the current text to the server
            # with text_lock:
            #     send_command(text_to_send, client_socket)

            # Receive frame from the server
            try:
                frame_base64 = (
                    await websocket.recv()
                )  # Receive base64 frame from the server

                frame_data = base64.b64decode(frame_base64)  # Decode the base64 frame
                # Convert the bytes to a numpy array and decode the image
                np_arr = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Display the received frame
                cv2.imshow("Received Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):  # Exit on 'q' key
                    break
            except Exception as e:
                print(f"Error receiving frame: {e}")

        cv2.destroyAllWindows()  # Close any OpenCV windows


if __name__ == "__main__":
    # Start the keyboard input thread
    # esp_ip = "192.168.0.102"
    # port = 80
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((esp_ip, port))

    # keyboard_thread = threading.Thread(target=capture_keyboard_input, daemon=True)
    # keyboard_thread.start()

    # Start the WebSocket communication
    # asyncio.run(send_text_and_receive_frames(client_socket))
    asyncio.run(send_text_and_receive_frames())
