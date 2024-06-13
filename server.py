import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    server = await websockets.serve(echo, '0.0.0.0', 8765)
    print('WebSocket server is running on ws://0.0.0.0:8765')
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())