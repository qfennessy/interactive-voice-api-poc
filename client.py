import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Receive the initial welcome message
        welcome = await websocket.recv()
        print("Server:", welcome)
        
        # Send a dummy binary message representing audio data
        await websocket.send(b"\x00\x01\x02\x03\x04")
        ack = await websocket.recv()
        print("Server:", ack)

        # Send more binary data
        await websocket.send(b"\x10\x20\x30")
        ack = await websocket.recv()
        print("Server:", ack)

        # Close the connection
        await websocket.close()

asyncio.run(test_client())