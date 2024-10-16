import cv2
import asyncio
import websockets
import base64
import json
import socket


async def send_frames_and_receive_text():
    uri = "ws://192.168.0.114:8000/ws"  # Connect to the video WebSocket
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)  # Open the default webcam

        while True:
            ret, frame = cap.read()  # Capture frame from the webcam
            if not ret:
                print("Failed to capture frame")
                break

            # Encode the frame as JPEG
            _, buffer = cv2.imencode(".jpg", frame)
            frame_base64 = base64.b64encode(buffer).decode(
                "utf-8"
            )  # Convert frame to base64 string

            await websocket.send(frame_base64)  # Send frame to the server

            # Receive text messages
            # try:
            #     text_message = (
            #         await websocket.recv()
            #     )  # Receive JSON text message from server
            #     # send signal here
            #     print(f"Received text message: {text_message}")
            # except Exception as e:
            #     print(f"Error receiving message: {e}")

        cap.release()  # Release the webcam when done


if __name__ == "__main__":
    asyncio.run(send_frames_and_receive_text())
