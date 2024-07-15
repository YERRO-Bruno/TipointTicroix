import https from 'https';
import { WebSocketServer } from 'ws';
import fs from 'fs';
import path from 'path';
const ip = '77.37.125.25'; // Ecouter sur toutes les interfaces disponibles
const port = 8765;
const server = new WebSocketServer({ ip, port });

const __dirname = path.resolve();
console.log("server websocket")
// Chemins vers les fichiers de certificat SSL
const privateKeyPath = '/etc/easypanel/traefik/dump/ti-points-ti-croix.fr/privatekey.key';
const certificatePath = '/etc/easypanel/traefik/dump/ti-points-ti-croix.fr/certificate.crt';

// Lire les fichiers de certificat SSL
const privateKey = fs.readFileSync(privateKeyPath, 'utf8');
const certificate = fs.readFileSync(certificatePath, 'utf8');

// Créer un serveur HTTPS
const httpsServer = https.createServer({ key: privateKey, cert: certificate });

// Créer un serveur WebSocket sécurisé (wss)
const wss = new WebSocketServer({ server: httpsServer });

// Événement déclenché lorsqu'une connexion est établie
wss.on('connection', (socket) => {
    console.log('Client connected');

    // Événement déclenché lorsqu'un message est reçu du client
    socket.on('message', (message) => {
        console.log('Received: %s', message);

        // Répondre au client
        socket.send('Hello from server!');
    });

    // Événement déclenché lorsque la connexion WebSocket est fermée
    socket.on('close', () => {
        console.log('Client disconnected');
    });

    // Gestion des erreurs WebSocket
    socket.on('error', (error) => {
        console.error('WebSocket error:', error.message);
    });
});

// Démarrer le serveur HTTPS
httpsServer.listen(port, ip, () => {
    console.log(`WebSocket Secure server is running on wss://${ip}:${port}`);
});