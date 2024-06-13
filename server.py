import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    server = await websockets.serve(echo, "127.0.0.1", 8765)
    print(server, websockets)
    print('WebSocket server is running')
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())