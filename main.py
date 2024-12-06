from typing import Optional
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Voice Interaction POC",
    description="A basic PoC for real-time voice interaction using WebSockets and FastAPI.",
    version="0.1.0"
)

# Allow CORS for local testing (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", response_class=HTMLResponse)
def get_home_page() -> str:
    """
    Return a simple HTML page with instructions on how to connect to the WebSocket endpoint.
    
    :return: HTML content as a string.
    """
    return """
    <html>
        <head><title>Voice Interaction POC</title></head>
        <body>
            <h1>WebSocket Voice Interaction POC</h1>
            <p>Use a WebSocket client to connect to <code>ws://localhost:8000/ws</code>.</p>
            <p>Send binary (audio) data frames and the server will respond with acknowledgments.</p>
        </body>
    </html>
    """


@app.get("/ws")
def websocket_handshake_info() -> None:
    """
    This route exists primarily for documentation and OpenAPI visibility.
    The actual WebSocket connection upgrade occurs on the /ws websocket route below.
    
    Attempting to call this route directly will result in an error.
    """
    raise HTTPException(status_code=400, detail="Use WebSocket at ws://localhost:8000/ws")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle a WebSocket connection for receiving audio data and sending acknowledgments.
    
    **Protocol**:
    - Client connects to the WebSocket at /ws.
    - Client sends binary data frames (representing audio chunks).
    - For each received chunk, the server sends back a text acknowledgment.
    - If the client disconnects, the server will stop.
    
    :param websocket: The WebSocket connection.
    """
    await websocket.accept()
    await websocket.send_text("Connection established. Send audio data as binary messages.")
    
    try:
        while True:
            # Receive binary data (simulate audio frames)
            data: Optional[bytes] = await websocket.receive_bytes()
            
            # Here, you'd integrate actual audio processing or STT logic.
            # For now, just acknowledge the receipt of data.
            chunk_size = len(data)
            response_msg = f"Received {chunk_size} bytes of audio data."
            
            # Send back a text acknowledgment
            await websocket.send_text(response_msg)
    except WebSocketDisconnect:
        # The client disconnected gracefully
        print("Client disconnected.")
    except Exception as e:
        # Handle unexpected errors
        error_msg = f"An error occurred: {str(e)}"
        await websocket.send_text(error_msg)
        await websocket.close(code=1011, reason="Internal server error")