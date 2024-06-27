import asyncio
import websockets
import socket
from tipoint_ticroix.models import UserConnected
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
    except websockets.exceptions.ConnectionClosedOK:
        print("connexion close")
        
async def main():
        async with websockets.serve(handler, ipaddress, 8765):
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())