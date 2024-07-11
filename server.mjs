import { WebSocketServer } from 'ws';
const ip = '0.0.0.0'; // Ecouter sur toutes les interfaces disponibles
const port = 8765;
const server = new WebSocketServer({ ip, port });
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

console.log(`WebSocket server is running on ws://${ip}:${port}`);
