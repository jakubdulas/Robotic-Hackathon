from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
import asyncio

app = FastAPI()
cap = cv2.VideoCapture(
    1
)  # Open the default webcam (0 usually refers to the default camera)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected clients
clients = []


@app.get("/")
async def get():
    return HTMLResponse(
        """
        <html>
            <head>
                <title>WebSocket Video Chat</title>
            </head>
            <body>
                <h1>WebSocket Video Chat</h1>
                <p>Connect your clients to this server.</p>
            </body>
        </html>
    """
    )


@app.websocket("/ws")
async def video_websocket(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            ret, frame = cap.read()  # Capture a frame from the webcam
            if not ret:
                break

            _, buffer = cv2.imencode(".jpg", frame)  # Encode the frame to JPEG
            frame_bytes = buffer.tobytes()  # Convert to bytes

            # Send the frame bytes to all connected clients
            for client in clients:
                await client.send_bytes(frame_bytes)

            # await asyncio.sleep(0.03)  # Control frame rate
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.153", port=8000)
