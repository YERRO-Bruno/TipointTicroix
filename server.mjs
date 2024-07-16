import https from 'https';
import { WebSocketServer } from 'ws';
import fs from 'fs';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();
global.connectedUsers = [];

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
global.connectedUsers=new Map
wss.on('connection', (socket) => {
    console.log('Client connected');    
    
    // Événement déclenché lorsqu'un message est reçu du client
    socket.on('message', (message) => {
        let tabusers=[]
        let tabinvite=[]
        console.log('Received: %s', message);
        const msgStr = message.toString();
        let msg=msgStr.split("/")
        if (msg[0]='connexion') {
            pseudo=msg[1]
            global.connectedUsers.set(socket,pseudo)
            // Répondre au client-connexion
            tabusers.push("connected")
            for (var [key, value] of global.connectedUsers) {
                tabusers.push(value)
            }
            socket.send(tabusers.join());
        }
        if (msg[0]='invite') {
            console.log("invite")
            let socketinvité=""
            //tabinvite.push("invite")
            //tabinvite.push(global.connectedUsers.get(String(socket)))
            for (var [key, value] of global.connectedUsers) {
                if (value=msg[1]) {
                    socketinvité=key
                    break
                }
            }
            socketinvité.send(tabinvite.join)
        }

    });

    // Événement déclenché lorsque la connexion WebSocket est fermée
    socket.on('close', () => {
        console.log('Client disconnected');
        global.connectedUsers.delete(socket);
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
