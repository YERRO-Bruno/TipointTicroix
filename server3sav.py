#!/usr/bin python3
import asyncio
import websockets
import logging
logging.basicConfig(level=logging.DEBUG, filename='server.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
async def handler(websocket):
    try:
        message = await websocket.recv()
        logging.debug(f"Message received: {message}")
        res=message.split("/")
        print(res)
        await websocket.send("retour " + res[1])
        logging.debug(f"Response sent: retour {res[1]}")
    except websockets.exceptions.ConnectionClosedOK:
        print("connexion close")
        logging.debug("Connection closed normally.")
async def main():
        async with websockets.serve(handler, "77.37.125.25", 8765):
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
