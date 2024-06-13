import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    server = await websockets.serve(echo, '195.35.28.193', 8765)
    print('WebSocket server is running on ws://10.0.1.185:8765')
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())