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
})
alert("debut websock")
    import { connect } from 'socket.io-client';
    const socket = connect('wss://ti-points-ti-croix.fr:8765/ws/chat/', {
    transports: ['websocket']});
    alert("websock1")
    // Écoutez les événements
    socket.on('connect', () => {
    alert('WebSocket is connected.');
    socket.send(JSON.stringify({ message: 'Hello Server!' }));
    });

    socket.on('message', (data) => {
    alert('Message from server:', data);
    });

    socket.on('disconnect', () => {
    alert('WebSocket is closed now.');
    });

    socket.on('error', (error) => {
    alert('WebSocket error:', error);
    });
