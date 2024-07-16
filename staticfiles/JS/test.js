document.addEventListener("DOMContentLoaded", function () {
    pseudox=document.getElementById("id-connec").textContent
    const userconnecteds=document.getElementById("id_userconnecteds")
    userconnecteds.addEventListener("click", function(e) {
        e.preventDefault()
        alert(e.target.id)
        socket.send('invite/'.concat(e.target.id))
    })
    //alert("Websocket1");
    var socket = new WebSocket('wss://ti-points-ti-croix.fr:8765/ws/chat/');
    //alert("Websock2");

    socket.addEventListener('open', (event) => {
        alert('WebSocket is connected.');
        socket.send('connexion/'.concat(pseudox));
    });

    let msg=[]
    socket.addEventListener('message', (event) => {
        alert('Message from server: ' + event.data);
        msg=event.data.split(",")
        if (msg[0]=="connected") {
            for (let i = 1; i < msg.length; i++) {
                const li=document.createElement("li")
                li.textContent=msg[i]
                li.id=msg[i]
                li.class="joueur"
                li.href='action'
                if (msg[i]==pseudox) {
                    li.style.color='blue'
                    li.style.fontWeight='1000'
                }
                userconnecteds.appendChild(li)
            }
        }
        if (msg[0]=="invite") {
            alert("invité par " + msg[1])

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

