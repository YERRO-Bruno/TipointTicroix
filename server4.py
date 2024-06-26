import asyncio
from websockets.server import serve
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddress = s.getsockname()[0]
s.close()
port = 8765
msg=""
webs=""
async def echo(websocket):
    async for message in websocket:
        print("received from {}:{} : ".format(websocket.remote_address[0],websocket.remote_address[1]) + message)
        await websocket.send(message)
        msg=message
        webs=websocket
async def main():
    print("Server is activated on ws://{}:{}".format(ipaddress,port))
    #async with serve(echo, "localhost", 8765):
    async with serve(echo, ipaddress, port):
            await asyncio.Future()  # run forever
asyncio.run(main())