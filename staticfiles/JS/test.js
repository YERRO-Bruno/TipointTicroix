document.addEventListener("DOMContentLoaded", function () {
    function filluserconnecteds() {
        const userconnecteds=document.getElementById("id_userconnecteds")
        const pseudox=document.getElementById("id-connec").textContent
        $.ajax({
            url:'/api/userconnecteds',
            method: "GET",
            dataType: "json",
            success: function (data) {
                var i = 0;
                data.forEach(userconnected => {
                    alert("success")
                    const li=document.createElement("li")
                    li.textContent=data[i].pseudo
                    li.class="joueur"
                    if (data[i].pseudo==pseudox) {
                        //alert(pseudox)
                        li.style.color='blue'
                        li.style.fontWeight='1000'
                    }
                    userconnecteds.appendChild(li)
                    i++
                })
            },
            error: function (xhr, status, error) {
                alert("error")

            }
        })
    }
    filluserconnecteds()
    document.getElementsByClassName("joueur").addEventListener("click", function(event) {
        alert('click')
        alert(event.target.textContent)
    })

    alert("websocket")
    try {
        var socket = new WebSocket('ws://77.37.125.25:8765/ws/chat/');
    } catch (error) {
        alert("Failed to create WebSocket: " + error);
    }
    alert("websock2")
    socket.addEventListener('open', (event) => {
            alert('WebSocket is connected.');
            socket.send(JSON.stringify({ message: 'Hello Server!' }));
    });    
    socket.addEventListener('message', (event) => {
            alert('Message from server ', event.data);
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

    // Send a message to the server
    document.getElementById('sendButton').addEventListener('click', function () {
        const messageInput = document.getElementById('messageInput');
})