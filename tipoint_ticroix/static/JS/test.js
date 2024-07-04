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
    var socket = new WebSocket('ws://77.37.125.25:8765/ws/chat/');
    alert("websock2")
    socket.addEventListener('open', (event) => {
            alert('WebSocket is connected.');
            alert(JSON.stringify({ message: 'Hello Server!' }));
    });
    // Envoyer un message au serveur
    var message = {
        'message': 'Hello, server!'
    };
    socket.send(JSON.stringify(message));
    
    socket.addEventListener('message', (event) => {
            alert('Message from server ', event.data);
    });
})