import asyncio
import websockets

PORT =  8766

# Keep track of all connected clients
connected_clients = set()

# Handles 
async def handler(websocket):
    # Register client
    connected_clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            # Simple ping-pong logic
            if message == "ping":
                await websocket.send("pong")
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)


async def start_stream():
    while True:
        msg = await get_terminal_input()    # REPLACE METHOD WITH FUNCTION THAT RETURNS MESSAGE TO SEND TO HTML
        if msg.strip().lower() == "exit":
            print("Stopping server...")
            for ws in connected_clients:
                await ws.close()
            break
        # Broadcast input to all connected clients
        for ws in connected_clients:
            try:
                await ws.send(msg)
            except websockets.ConnectionClosed:
                pass


async def get_terminal_input() -> str:
    loop = asyncio.get_running_loop()
    msg = await loop.run_in_executor(None, input, "")
    print(f"Received in terminal: {msg}")
    return msg


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        print(f"Server running at ws://localhost:{PORT}")
        # Run terminal input task concurrently with server
        await start_stream()

asyncio.run(main())
