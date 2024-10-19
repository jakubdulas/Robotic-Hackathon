from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import time
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

FRAME_RATE = 20
FRAME_DELAY = 1 / FRAME_RATE  # Calculate delay based on the frame rate


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
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            for client in clients:
                await client.send_bytes(frame_bytes)

            await asyncio.sleep(FRAME_DELAY - (time.time() - start_time))

    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.153", port=8000)
