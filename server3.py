import asyncio
import websockets
import socket
print("debut")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("", 80))
ipaddress = s.getsockname()[0]
print(ipaddress)
async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)

async def main():
    async with websockets.serve(handler, ipaddress, 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())