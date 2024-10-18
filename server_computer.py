import cv2
import asyncio
import websockets
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS if needed (optional)
# Allow CORS if needed (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Unity app's IP or use ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def receive_frames(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive frame data
            data = await websocket.receive_bytes()

            # Convert byte data to numpy array
            nparr = np.frombuffer(data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Display the image using OpenCV
            cv2.imshow("Received Frame", image)
            cv2.waitKey(1)  # Needed to update the window

        except Exception as e:
            print(f"Error: {e}")
            await websocket.close()
            break


@app.get("/")
async def get():
    return HTMLResponse(
        """
        <html>
            <head>
                <title>WebSocket Frame Receiver</title>
            </head>
            <body>
                <h1>WebSocket Frame Receiver</h1>
                <p>Connect to the WebSocket from your Unity application to receive frames.</p>
            </body>
        </html>
    """
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.153", port=8765)
