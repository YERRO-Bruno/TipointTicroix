import https from 'https';
import { WebSocketServer } from 'ws';
import fs from 'fs';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();
global.connectedUsers = [];

// Configuration de la connexion MySQL
const dbConfig = {
    host: process.env.HOST,       // Remplacez par l'adresse de votre serveur MySQL
    user: process.env.USER,   // Remplacez par votre nom d'utilisateur MySQL
    password: process.env.PASSWORD, // Remplacez par votre mot de passe MySQL
    database: process.env.NAME  // Remplacez par le nom de votre base de données
};

// Fonction pour insérer un user dans la table userconnected
async function insertIntoDatabase(pseudo) {
    try {
        const connection = await mysql.createConnection(dbConfig);
        const [rows] = await connection.execute(
            'INSERT INTO userconnected (pseudo) VALUES (?)', 
            [pseudo] 
        );
        console.log('Data inserted successfully:', rows);
        await connection.end();
    } catch (error) {
        console.error('Error inserting data into MySQL:', error.message);
    }
}

// Fonction pour supprimer un user de la table userconnected
async function deleteFromDatabase(pseudo) {
    try {
        const connection = await mysql.createConnection(dbConfig);
        const [rows] = await connection.execute(
            'DELETE FROM userconnected WHERE pseudo = ?', 
            [pseudo] 
        );
        console.log('Data deleted successfully:', rows);
        await connection.end();
    } catch (error) {
        console.error('Error deleting data from MySQL:', error.message);
    }
}

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

wss.on('connection', (socket) => {
    console.log('Client connected');    

    // Événement déclenché lorsqu'un message est reçu du client
    socket.on('message', (message) => {
        console.log('Received: %s', message);
        const msgStr = message.toString();
        let msg=msgStr.split("/")
        if (msg[0]='connexion') {
            pseudo=msg[1]
            global.connectedUsers.push(pseudo)
            insertIntoDatabase(pseudo)
        }

        // Répondre au client
        socket.send(global.connectedUsers);
    });

    // Événement déclenché lorsque la connexion WebSocket est fermée
    socket.on('close', () => {
        console.log('Client disconnected');
        const index = global.connectedUsers.indexOf(pseudo);
        const x = global.connectedUsers.splice(index, 1);
        deleteFromDatabase(pseudo)
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
