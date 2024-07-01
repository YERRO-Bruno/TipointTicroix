#!/usr/bin/env python3
import asyncio
import websockets
import socket
import logging
logging.basicConfig(level=logging.DEBUG, filename='server.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
print("debut")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddress = s.getsockname()[0]
print(ipaddress)
async def handler(websocket):
    try:
        message = await websocket.recv()
        res=message.split("/")
        print(res)
        await websocket.send("retour " + res[1])
    except websockets.exceptions.ConnectionClosedOK:
        print("connexion close")

async def main():
        async with websockets.serve(handler, ipaddress, 8765):
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
