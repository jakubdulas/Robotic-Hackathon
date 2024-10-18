import cv2
import asyncio
import websockets
import base64
import json
import socket
import time

FRAME_RATE = 30  # Target FPS


async def send_frames_and_receive_text():
    uri = "ws://192.168.0.171:8000/ws"  # Connect to the video WebSocket

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                cap = cv2.VideoCapture(1)  # Open the default webcam

                while True:
                    start_time = time.time()

                    ret, frame = cap.read()
                    if not ret:
                        continue

                    # Encode the frame as JPEG
                    _, buffer = cv2.imencode(".jpg", frame)

                    await websocket.send(buffer.tobytes())

                    elapsed_time = time.time() - start_time
                    if elapsed_time < 1.0 / FRAME_RATE:
                        time.sleep(1.0 / FRAME_RATE - elapsed_time)

                cap.release()  # Release the webcam when done
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}. Reconnecting...")
            await asyncio.sleep(2)  # Wait before trying to reconnect


if __name__ == "__main__":
    asyncio.run(send_frames_and_receive_text())

# import cv2
# import asyncio
# import websockets
# import base64
# import json
# import socket
# import time

# FRAME_RATE = 30  # Target 10 FPS


# async def send_frames_and_receive_text():
#     uri = "ws://192.168.0.171:8000/ws"  # Connect to the video WebSocket
#     async with websockets.connect(uri) as websocket:
#         cap = cv2.VideoCapture(1)  # Open the default webcam

#         while True:
#             start_time = time.time()

#             ret, frame = cap.read()
#             if not ret:
#                 continue

#             # Encode the frame as JPEG
#             _, buffer = cv2.imencode(".jpg", frame)

#             await websocket.send(buffer.tobytes())

#             # frame_base64 = base64.b64encode(buffer).decode(
#             #     "utf-8"
#             # )  # Convert frame to base64 string
#             # await websocket.send(frame_base64)  # Send frame to the server

#             elapsed_time = time.time() - start_time
#             if elapsed_time < 1.0 / FRAME_RATE:
#                 time.sleep(1.0 / FRAME_RATE - elapsed_time)

#             # Receive text messages
#             # try:
#             #     text_message = (
#             #         await websocket.recv()
#             #     )  # Receive JSON text message from server
#             #     # send signal here
#             #     print(f"Received text message: {text_message}")
#             # except ExceptionError as e:
#             #     print(f" receiving message: {e}")

#         cap.release()  # Release the webcam when done


# if __name__ == "__main__":
#     asyncio.run(send_frames_and_receive_text())
