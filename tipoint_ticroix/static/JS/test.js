document.getElementById("btn-client").addEventListener('click', function(e) {
alert("client")
  

  const socket = new WebSocket('ws://0.0.0.0:8765');
  
  alert("1")
        socket.onopen = () => {
            console.log('Connected to the WebSocket server');
            alert("'Connected to the WebSocket server'")
        };

        socket.onmessage = (event) => {
            alert(event.data)
            messageItem.textContent = event.data;
            
        };

        function sendMessage() {
            socket.send("hello serveur bonjour");
            
        }

})