import asyncio
import websockets
import base64
import cv2
import numpy as np


async def send_text_and_receive_frames():
    uri = "ws://192.168.0.172:8000/ws"  # Connect to the text WebSocket
    async with websockets.connect(uri) as websocket:
        while True:
            # text = input("Enter text to send: ")  # Get user input
            text = "Some data"
            await websocket.send(text)  # Send text to the server

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
    asyncio.run(send_text_and_receive_frames())
