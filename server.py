import asyncio
import websockets
import TIPOINTICROIX.settings

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

start_server = websockets.serve(echo, TIPOINTICROIX.settings.WEB_SOCKET_SERVER, 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()