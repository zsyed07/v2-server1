import asyncio
import websockets
import json

# Store connected clients
connected_clients = []

async def handle_connection(websocket, path):
    # Register client
    connected_clients.append(websocket)
    print("New client connected")

    try:
        async for message in websocket:
            print(f"Received message: {message}")

            # Broadcast message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Prevent echoing back to sender
                    await client.send(message)

    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Unregister client
        connected_clients.remove(websocket)

# Start WebSocket server
start_server = websockets.serve(handle_connection, "0.0.0.0", 8765)

print("WebSocket server is running on ws://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
