import https from 'https';
import { WebSocketServer } from 'ws';
import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

// Adresse IP et port
const ip = '77.37.125.25'; // Adresse IP spécifique à écouter
const port = 8765;

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
let pseudo=""
global.connectedUsers={}
global.disponibleUsers={}
wss.on('connection', (socket) => {
    console.log('Client connected');    
    
    // Événement déclenché lorsqu'un message est reçu du client
    socket.on('message', (message) => {
        let tabusers=[]
        console.log('Received: %s', message);
        const msgStr = message.toString();
        let msg=msgStr.split("/")
        global.connectedUsers[pseudo]=socket
        if (msg[0]=='connexion') {
            pseudo=msg[1]
            global.disponibleUsers[pseudo]=socket
            // Répondre au client-connexion
            tabusers.push("connected")
            Object.keys(global.disponibleUsers).forEach(pseudox => {
                tabusers.push(pseudox)
            });
            socket.send(tabusers.join("/"));
        }
        if (msg[0]=='invite') {
            let socketinvite=global.connectedUsers[msg[1]]
            socketinvite.send("invite/"+pseudo)
        }
    });

    // Événement déclenché lorsque la connexion WebSocket est fermée
    socket.on('close', () => {
        Object.keys(global.connectedUsers).forEach(pseudo => {
            const socketx = global.connectedUsers[pseudo];
            if (socketx==socket) {
                console.log('Client disconnected',pseudo);
                delete global.connectedUsers[pseudo];
                console.log(Object.keys(global.connectedUsers))
            }
        });
        Object.keys(global.disponibleUsers).forEach(pseudo => {
            const socketx = global.disponibleUsers[pseudo];
            if (socketx==socket) {
                delete global.disponibleUsers[pseudo];
            }
        });

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
