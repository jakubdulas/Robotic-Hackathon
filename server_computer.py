import asyncio
import websockets
from PIL import Image
import io


async def receive_frames(websocket, path):
    while True:
        try:
            # Receive frame data
            data = await websocket.recv()

            # Convert to image
            image = Image.open(io.BytesIO(data))
            image.show()

        except Exception as e:
            print(f"Error: {e}")
            break


async def main():
    async with websockets.serve(receive_frames, "192.168.0.153", 8765):
        await asyncio.Future()  # Keep the server running


if __name__ == "__main__":
    asyncio.run(main())
