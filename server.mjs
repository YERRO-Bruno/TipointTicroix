import https from 'https';
import { WebSocketServer, WebSocket } from 'ws'
import fs from 'fs';
import mysql from 'mysql2/promise';
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
let hote=""
let invité=""
global.tabusers=[]
global.connectedUsers={}
wss.on('connection', (socket) => {
    //console.log('Client connected');    
    
    // Événement déclenché lorsqu'un message est reçu du client
    socket.on('message', (message) => {
    //    let tabusers=[]
        console.log('Received: %s', message);
        const msgStr = message.toString();
        let msg=msgStr.split(",")
        pseudo=msg[1]
        //delete global.connectedUsers[msg[1]]
        global.connectedUsers[msg[1]]=socket
        if (msg[0]=='connexion') {
            // Répondre au client-connexion
            console.log(msg[0],msg[1])
            //tabusers.push("connected")
            global.tabusers.push(msg[1])
            console.log(global.tabusers)
            let tabusers2=global.tabusers
            global.tabusers.forEach(pseudo => {
                    let socketx=global.connectedUsers[pseudo]
                    socketx.send("connected,"+tabusers2.join(","))                
            })            
        }
        if (msg[0]=='nouveautour') {
            console.log(msg[0],msg[1])
        }

        if (msg[0]=='invite') {           
            Object.keys(global.connectedUsers).forEach(pseudox => {
                let socketx = global.connectedUsers[pseudox];
                if (socketx==socket) {
                    hote=pseudox
                }
            });
            let socketinvite=global.connectedUsers[msg[2]]
            socketinvite.send("invite,"+msg[1]+","+msg[2])
        }
        if (msg[0]=='accept') {
            let sockethote=global.connectedUsers[msg[2]]
            sockethote.send("accept,"+msg[1]+","+msg[2])
        }
        if (msg[0]=="tourjeu") {
            let socketadversaire=global.connectedUsers[msg[2]]
            socketadversaire.send("tourjeu,"+msg[1]+","+msg[2]+","+msg[3])
        }
    });

    // Événement déclenché lorsque la connexion WebSocket est fermée
    socket.on('close', () => {
        Object.keys(global.connectedUsers).forEach(pseudo => {
            const socketx = global.connectedUsers[pseudo];
            if (socketx==socket) {
                let i=0
                global.tabusers.forEach(pseudox => {
                    if (pseudox=pseudo) {
                        global.tabusers.splice(i,1)
                    }
                });
                console.log('Client disconnected',pseudo);
                delete global.connectedUsers[pseudo];
                console.log(Object.keys(global.connectedUsers, global.tabusers))
            }           
        })
        let tabusers2=global.tabusers
        global.tabusers.forEach(pseudox => {
                let socketx=global.connectedUsers[pseudox]
                socketx.send("connected,"+tabusers2.join(","))                
        }) 
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

