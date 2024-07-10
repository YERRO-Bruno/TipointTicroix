import WebSocket from 'ws';

const server = new WebSocket.Server({ port: 8765 });

server.on('connection', (socket) => {
    console.log('Client connected');

    socket.on('message', (message) => {
        console.log('Received: %s', message);
        // Répondre au client
        socket.send('Hello from server!');
    });

    socket.on('close', () => {
        console.log('Client disconnected');
    });

    socket.on('error', (error) => {
        console.error('WebSocket error: ' + error.message);
    });
});

console.log('WebSocket server is running on ws://localhost:8765');
