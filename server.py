from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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


# @app.websocket("/ws")
# async def video_websocket(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()  # Expecting frames in base64
#             for client in clients:
#                 if client is not websocket:
#                     await client.send_text(data)  # Send the frame to other clients
#     except Exception as e:
#         print(f"Connection closed: {e}")
#     finally:
#         clients.remove(websocket)


@app.websocket("/ws")
async def video_websocket(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            message = await websocket.receive()  # Can handle both text and binary
            if "text" in message:
                data = message["text"]  # Handle text (base64 frames)
            elif "bytes" in message:
                data = message["bytes"]  # Handle binary data (e.g., raw images)

            # Forward the message to other clients
            for client in clients:
                if client is not websocket:
                    if "text" in message:
                        await client.send_text(data)
                    elif "bytes" in message:
                        await client.send_bytes(data)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.171", port=8000)
