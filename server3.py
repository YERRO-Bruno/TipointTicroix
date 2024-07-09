#!/usr/bin/env python3
import asyncio
import websockets
import logging
import ssl

logging.basicConfig(level=logging.DEBUG, filename='/etc/easypanel/projects/tipointticroix/tipointticroix/server.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

connected_clients = set()

async def handler(websocket):
    global connected_clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logging.debug(f"Message received: {message}")
            res = message.split("/")
            response = "retour " + res[1]
            logging.debug(f"Response prepared: {response}")

            # Envoyer la réponse à tous les clients connectés
            for client in connected_clients:
                await client.send(response)
                logging.debug(f"Response sent to client: {response}")

    except websockets.exceptions.ConnectionClosedOK:
        logging.debug("Connection closed normally.")
    except websockets.exceptions.ConnectionClosedError as e:
        logging.error(f"Connection closed with error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        connected_clients.remove(websocket)
        await websocket.close()
        logging.debug("Connection closed and removed from the list.")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='/etc/easypanel/traefik/dump/ti-points-ti-croix.fr/certificate.crt', keyfile='/etc/easypanel/traefik/dump/ti-points-ti-croix.fr/privatekey.key')


async def main():
    async with websockets.serve(handler, "ti-points-ti-croix.fr", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

    