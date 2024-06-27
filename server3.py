import asyncio
import websockets
import socket
print("debut")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddress = s.getsockname()[0]
print(ipaddress)
async def handler(websocket):
    while True:
        message = await websocket.recv()
        res=message.split("/")
        print(res)


async def main():
    try:
        async with websockets.serve(handler, ipaddress, 8765):
            await asyncio.Future()  # run forever
    except websockets.exceptions.ConnectionClosedOK:
        print("connexion close")
        
if __name__ == "__main__":
    asyncio.run(main())