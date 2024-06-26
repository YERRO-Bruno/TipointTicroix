"""
ASGI config for TIPOINTICROIX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import asyncio
import websockets
from hypercorn.config import Config
from hypercorn.asyncio import serve

async def handler(websocket, path):
    while True:
        message = await websocket.recv()
        print(message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())