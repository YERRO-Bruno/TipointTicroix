document.getElementById("btn-client").addEventListener('click', function(e) {
  //alert("client")
  
// Créer une nouvelle connexion WebSocket
const socket = new WebSocket('192.168.1.188');

// Événement lorsque la connexion est ouverte
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Événement lorsque le serveur envoie un message
socket.addEventListener('message', function (event) {
    alert(event.data);
});

})

document.getElementById("btn-serveur").addEventListener('click', function(e) {
  //alert("serveur")
  
  const WebSocket = require('ws');

  const server = new WebSocket.Server({ port: 8080 });

  server.on('connection', (ws) => {
      ws.on('message', (message) => {
          alert(message);
      });
      ws.send('Hello! Message from server.');
  });

})