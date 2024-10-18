import asyncio
import websockets
import cv2
import numpy as np


async def send_text_and_receive_frames():
    uri = "ws://192.168.0.21:8000/ws"  # Connect to the WebSocket server
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                frame_data = (
                    await websocket.recv()
                )  # Receive raw frame bytes from the server

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
