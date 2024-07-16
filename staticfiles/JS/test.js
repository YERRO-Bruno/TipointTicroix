document.addEventListener("DOMContentLoaded", function () {
    alert("1")
    pseudox=document.getElementById("id-connec").textContent
    const userconnecteds=document.getElementById("id_userconnecteds")
    userconnecteds.addEventListener("click", function(e) {
        e.preventDefault()
        alert("click joueur")
        alert(e.target.id)
    })
    //alert("Websocket1");
    var socket = new WebSocket('wss://ti-points-ti-croix.fr:8765/ws/chat/');
    //alert("Websock2");

    socket.addEventListener('open', (event) => {
        alert('WebSocket is connected.');
        socket.send('connexion/'.concat(pseudox));
    });
    let joueurs=[]
    socket.addEventListener('message', (event) => {
        alert('Message from server: ' + event.data);
        joueurs=event.data.split(",")
        for (let i = 0; i < joueurs.length; i++) {
            const li=document.createElement("li")
            li.textContent=joueurs[i]
            li.id=joueurs[i]
            li.class="joueur"
            li.href='action'
            if (joueurs[i]==pseudox) {
                li.style.color='blue'
                li.style.fontWeight='1000'
            }
            userconnecteds.appendChild(li)
        }
    });

    // Connection closed
    socket.addEventListener('close', function (event) {
        alert("WebSocket is closed now.");
        console.log('WebSocket is closed now.');
    });

    // Listen for errors
    socket.addEventListener('error', function (error) {
        alert("WebSocket error: " + error);
        console.log('WebSocket error: ', error);
    });
})

