document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("x-board").style.display="none"
    pseudox=document.getElementById("id-connec").textContent
    const userconnecteds=document.getElementById("id_userconnecteds")
    let msg=[]
    let adv=""
    const etape=document.getElementById("id-etape")
    const jeton=document.getElementById("id-jeton")

    const joueur=document.getElementById("id-joueur")
    const adversaire=document.getElementById("id-adversaire")
    var socket = new WebSocket('wss://ti-points-ti-croix.fr:8765/ws/chat/');
    userconnecteds.addEventListener("click", function(e) {
        e.preventDefault()
        adv=e.target.id
        socket.send('invite/'.concat(e.target.id))
        
    })

    socket.addEventListener('open', (event) => {
        //alert('WebSocket is connected.');
        if (etape.value=="connexion") {
            //alert("connexion "+pseudox)
            socket.send('connexion/'.concat(pseudox));
        }
    });

    socket.addEventListener('message', (event) => {
        alert('Message from server: ' + event.data);
        msg=event.data.split("/")
        if (msg[0]=="connected") {
            alert("connected")
            for (let i = 1; i < msg.length; i++) {
                const li=document.createElement("li")
                li.textContent=msg[i]
                li.id=msg[i]
                li.class="joueur"
                li.href='action'
                if (msg[i]!=pseudox) {
                    li.style.color='blue'
                    li.style.fontWeight='1000'
                    userconnecteds.appendChild(li)
                }
            }
        }
        if (msg[0]=="invite") {
            alert("invité par " + msg[1])
            if (confirm("Acceptez-vous de jouer avec "+msg[1])) {
                socket.send('accept/'+adv)
                etape.value="début"
                jeton.value="Non"
                joueur.value=pseudox
                adversaire.value=msg[1]
                document.forms["internet"].submit();
            } 
        if (msg[0]=="accept") {
            alert("acceptation de " + msg[1])
            etape.value="début"
            jeton.value="Oui"
            joueur.value=pseudox
            adversaire.value=msg[1]
            document.forms["internet"].submit();
        } 
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

    if (etape.value=="tourjeu") {
        displayGameBoard()
    }
})
//Functions
//Affichage de la grille
function displayGameBoard(){
    document.getElementById("x-jouer").style.display="none"
    document.getElementById("x-board").style.display="block"
    
    // creation lignes du tableau
    var cell, ligne;
    var tableau = document.getElementById("table");
    for (let j = 0; j < 25; j++) {
      
        ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
                                        // le paramètre est dans ce cas (-1)

    // création et insertion des cellules dans la nouvelle ligne créée
      for (let i = 0; i < 25; i++) {
          var idx= j+"/"+i
          var imghtml=`
              <input class="textcenter" id=${idx} type="text"
                  style="margin: 0; margin-left: 4; border-spacing: 0">
              </input>
          `
          cell = ligne.insertCell(i);
          cell.id = idx
          cell.innerHTML = imghtml
          cell.style.color = "black"
          cell.textContent = ""
          cell.style.height = "3vh"
          cell.style.width = "3vh"
          cell.style.background = "white"
          cell.style.border = "1px solid"
          cell.borderSpacing ="0"
          cell.style.textAlign = "center"
      }
    }
    document.getElementById("victoire").style.display="none"
    document.getElementById("defaite").style.display="none"
    if (document.getElementById("id-jeton").textContent=="Oui") {
        document.getElementById("ALUI").style.display="none"
    } else {
        document.getElementById("AVOUS").style.display="none"
    }
    
    //document.getElementById("nb-tour").textContent="1"
    res=document.getElementById("id-sequence").value
    
    if (res.length > 0) { 
        let sequence=res.split(',')  
        //Affichage des coups joués
        let nbcoup=sequence.length
        var marque="O"
        for (let i = 0;i<nbcoup;i++) {
            document.getElementById(sequence[i]).textContent=marque
            if (marque=="X") {
                document.getElementById(sequence[i]).style.color="red"
            } else {
                document.getElementById(sequence[i]).style.color="blue"
            }
            if (i>sequence.length -3) {
                document.getElementById(sequence[i]).style.fontWeight="1000"
            }
            if (marque=="O") {
                marque="X"
            } else {
                marque="O"
            }              
        }
        win="Non"
        if (document.getElementById("id-victoire").value!="Non") {
            win=document.getElementById("id-victoire").value
            document.getElementById("victoire").style.display="block"
            document.getElementById("defaite").style.display="none"
        }
        if (document.getElementById("id-defaite").value!="Non") {
            win=document.getElementById("id-defaite").value
            document.getElementById("defaite").style.display="block"
            document.getElementById("victoire").style.display="none"
        }
        if (win != "Non") { 
        if (document.getElementById("id-finpartie").textContent=="Oui") {
            document.getElementById("btn-rejouer").style.display="block"
        } else {
            document.getElementById("btn-manche2").style.display="block"
            }
        
        document.getElementById("ALUI").style.display="none"   
        document.getElementById("AVOUS").style.display="none"
        win=win.split(",")
        for (let i = 0;i<5;i++) {
            document.getElementById(win[i]).style.backgroundColor="yellow"
        }
        //fin de partie
        }
    }
}
