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
                    const li=document.createElement("li")
                    li.textContent=data[i].pseudo
                    li.id=data[i].pseudo
                    li.class="joueur"
                    li.href='action'
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
        //alert('WebSocket is connected.');
        socket.send(JSON.stringify({ message: 'connexion/'.concat(pseudox) }));
    });

    socket.addEventListener('message', (event) => {
        //alert('Message from server: ' + event.data);
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
    filluserconnecteds()
})

