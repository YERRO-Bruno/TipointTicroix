const WebSocket = require('ws');
    
    //alert("serveur0")
const server = new WebSocket.Server({ port: 9000 });
    //alert("serveur")

server.on('connection', (ws) => {
  ws.on('message', (message) => {
    console.log('A new client connected');
    console.log(`Received message: ${message}`);
    // Diffuser le message à tous les clients connectés
    server.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send("hello clients");
        }
    });
});
})
