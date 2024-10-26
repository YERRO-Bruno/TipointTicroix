
console.log("in worker")
var socket = new WebSocket('wss://ti-points-ti-croix.fr:8765/ws/chat/');
onmessage = (e) => {
  socket.addEventListener('open', (event) => {
    socket.send('test,'.concat(document.getElementById("id-connec").textContent));
    console.log("in worker")
    postMessage("message bien reçu de worker : "+document.getElementById("id-connec").textContent)
  })
}
