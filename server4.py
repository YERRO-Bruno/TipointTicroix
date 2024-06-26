import asyncio
import runpy
from websockets.server import serve
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddress = s.getsockname()[0]
s.close()
port = 8765
msg=""
webs=""
def echo(websocket):
    for message in websocket:
        print("received from {}:{} : ".format(websocket.remote_address[0],websocket.remote_address[1]) + message)
        websocket.send(message)
        msg=message
        webs=websocket
def main():
    print("Server is activated on ws://{}:{}".format(ipaddress,port))
    serve(echo, ipaddress, port):
#            await asyncio.Future()  # run forever
runpy(main())