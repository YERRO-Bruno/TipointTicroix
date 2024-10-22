document.addEventListener("DOMContentLoaded", function () {
    if (window.innerWidth > window.innerHeight) {    
        h=((window.innerHeight-20)/25)+"px"
        fontsz="1vw"
    } else {
        h="4vw"
        fontsz="1vh"
    }
    document.getElementById("x-board").style.display="none"
    document.getElementById("id-bandeau").style.display="none"
    //pseudox=document.getElementById("id-connec").textContent
    const userconnecteds=document.getElementById("id_userconnecteds")
    let msg=[]
    
    const joueur=document.getElementById("id-joueur")
    var socket = new WebSocket('wss://ti-points-ti-croix.fr:8765/ws/chat/');
    userconnecteds.addEventListener("click", function(e) {
        e.preventDefault()
        invite=e.target.id
        message="invite,"+document.getElementById("id-connec").textContent+","+e.target.id
        socket.send(message)  
    })

    document.getElementById("btn-quitter").addEventListener('click', function(e) {
        e.preventDefault()
        document.location.href='/'        
    })

    // Click du joueur sur une des cases
    document.getElementById("table").addEventListener('click', function(e) {
        if ((document.getElementById("id-victoire").value=="Non" &&
        document.getElementById("id-defaite").value=="Non")) {
            if (document.getElementById("id-jeton").value=="Non") {
                alert("Ce n'est pas à vous de jouer")
            } else {
            if (document.getElementById("id-begin").textContent==document.getElementById("id-joueur").value) {
            marque="O"
            } else {
                marque="X"
            }
            if (document.getElementById(e.target.id).textContent=="") {
            document.getElementById(e.target.id).textContent = marque
            document.getElementById(e.target.id).style.fontSize=fontsz
            if (marque=="X") {
                document.getElementById(e.target.id).style.color="red"
            } else {
                document.getElementById(e.target.id).style.color="blue"
            }   
            e.target.blur()
            document.getElementById("coup-joueur").value=e.target.id
            document.getElementById("id-etape").value="tourjeu"
            document.getElementById("id-jeton").value="Non"
              
            //alert("jeu")
            socket.send('tourjeu,'.concat(document.getElementById("id-connec").textContent,
            ",",document.getElementById("id-adversaire").value,",",e.target.id))
            document.getElementById("id-etape").value="tourjeu"
            document.getElementById("id-jeton").value="Non"
            document.getElementById("id-joueur").value=document.getElementById("id-connec").textContent
            if (window.innerWidth > window.innerHeight) {
                document.getElementById("orientation").value="paysage"
            } else {
                document.getElementById("orientation").value="portrait"
            }
            document.forms["internet"].submit();
            } else {
                alert("Case déjà utilisée")
            }
            }
        } else {
            if (document.getElementById("nb-tour").textContent="0") {
                alert("Choisissez votre adversaire!")
            } else {
                alert("partie terminée !")
              }
        }
    })

    socket.addEventListener('open', (event) => {
        if (document.getElementById("id-etape").value=="connexion") {
            socket.send('connexion,'.concat(document.getElementById("id-connec").textContent));
        }
        if (document.getElementById("id-etape").value=="nouveautour") {
            socket.send('nouveautour,'.concat(document.getElementById("id-connec").textContent));
        }
    });

    socket.addEventListener('message', (event) => {

        msg=event.data.split(",")
        if (msg[0]=="connected") {
            while (userconnecteds.firstChild) {
                userconnecteds.removeChild(userconnecteds.lastChild);
            }
            for (let i = 1; i < msg.length; i++) {
                if (msg[i]!=document.getElementById("id-connec").textContent) {
                    const li=document.createElement("li")
                    li.textContent=msg[i]
                    li.id=msg[i]
                    li.class="joueur"
                    li.href='action'
                    li.style.color='blue'
                    li.style.fontSize=fontsz
                    li.style.fontWeight='1000'
                    userconnecteds.appendChild(li)
                }
            }
        }
        if (msg[0]=="invite") {
            if (confirm("Acceptez-vous de jouer avec "+msg[1])) {
                socket.send('accept,'.concat(document.getElementById("id-connec").textContent,',',msg[1]))
                document.getElementById("id-etape").value="début"
                document.getElementById("id-jeton").value="Non"
                document.getElementById("id-joueur").value=document.getElementById("id-connec").textContent
                document.getElementById("id-adversaire").value=msg[1]
                document.getElementById("id-match").value=1
                document.getElementById("id-score1").value=0
                document.getElementById("id-score2").value=0
                if (window.innerWidth > window.innerHeight) {
                    document.getElementById("orientation").value="paysage"
                } else {
                    document.getElementById("orientation").value="portrait"
                }
                document.forms["internet"].submit();
            } 
        }
        if (msg[0]=="accept") {
            document.getElementById("id-etape").value="début"
            document.getElementById("id-jeton").value="Oui"
            document.getElementById("id-joueur").value=document.getElementById("id-connec").textContent
            document.getElementById("id-adversaire").value=msg[1]
            document.getElementById("id-match").value=1
            document.getElementById("id-score1").value=0
            document.getElementById("id-score2").value=0
            if (window.innerWidth > window.innerHeight) {
                document.getElementById("orientation").value="paysage"
            } else {
                document.getElementById("orientation").value="portrait"
            }
            document.forms["internet"].submit();
        } 
        if (msg[0]=="tourjeu") {
            document.getElementById("coup-joueur").value=msg[3]
            document.getElementById("id-etape").value="tourjeu"
            document.getElementById("id-jeton").value="Oui"
            document.getElementById("id-joueur").value=document.getElementById("id-connec").textContent
            document.getElementById("id-adversaire").value=msg[1]
            if (window.innerWidth > window.innerHeight) {
                document.getElementById("orientation").value="paysage"
            } else {
                document.getElementById("orientation").value="portrait"
            }
            document.forms["internet"].submit();
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

    //changement de l'orientation de l'ecran
    window.screen.orientation.addEventListener("change", function() {
        if (document.getElementById("nb-tour").textContent > "0") {
            document.getElementById("id-etape").value="charger"
        } else {
            document.getElementById("id-etape").value="rotatdébut"
        }             
        if (window.innerWidth > window.innerHeight) {
            document.getElementById("orientation").value="paysage"
        } else {
            document.getElementById("orientation").value="portrait"
        }
        //
        document.forms["internet"].submit();
    });

    //AFFICHAGE
    displayGameBoard()

})

//Functions
//Affichage de la grille
function displayGameBoard(){
    // alert(document.getElementById("id-etape").value)
    if (document.getElementById("id-etape").value=="nouveautour") {
        document.getElementById("x-jouer").style.display="none"
        document.getElementById("x-board").style.display="block"
        if (ismobile()) {
            document.getElementById("joystick").style.display="block"
        }
        // document.getElementById("btn-quitter").style.display="none"
    }
    // creation lignes du tableau
    var cell, ligne;
    if (window.innerWidth > window.innerHeight) {
        h=window.innerHeight/25        
        fontsz="0.9vw"
      } else {
        h=window.innerWidth/25
        fontsz="0.9vh"
      }   
    h=h+"px"
    var tableau = document.getElementById("table");
    for (let j = 0; j < 25; j++) {
      
        ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
                                        // le paramètre est dans ce cas (-1)

    // création et insertion des cellules dans la nouvelle ligne créée
      for (let i = 0; i < 25; i++) {
          var idx= j+"/"+i
          var imghtml=`
              <input class="textcenter" id=${idx} type="text"
                  style="margin: 0; margin-left: 4; border-spacing: 0;width=10vh">
              </input>
          `
          cell = ligne.insertCell(i);
          cell.id = idx
          cell.innerHTML = imghtml
          cell.style.color = "black"
          cell.textContent = ""
          cell.style.height = h
          cell.style.width = "4vh"
          cell.style.background = "white"
          cell.style.border = "1px solid"
          cell.borderSpacing ="0"
          cell.style.textAlign = "center"
      }
    }
    document.getElementById("victoire").style.display="none"
    document.getElementById("defaite").style.display="none"
    if (document.getElementById("id-jeton").value=="Oui") {
        document.getElementById("ALUI").style.display="none"
    } else {
        document.getElementById("AVOUS").style.display="none"
    }
    //document.getElementById("nb-tour").textContent="1"
    let scor1=document.getElementById("id-score1").value
    let scor2=document.getElementById("id-score2").value
    res=document.getElementById("id-sequence").value
    if (res.length > 0) { 
        let sequence=res.split(',')  
        //Affichage des coups joués
        let nbcoup=sequence.length
        var marque="O"
        for (let i = 0;i<nbcoup;i++) {
            document.getElementById(sequence[i]).textContent=marque
            document.getElementById(sequence[i]).style.fontSize=fontsz
            document.getElementById(sequence[i]).style.color="black"
            if (marque=="X") {
                document.getElementById(sequence[i]).style.backgroundColor="lightpink"
            } else {
                document.getElementById(sequence[i]).style.backgroundColor="cyan"
            }
            if (i>sequence.length -3) {
                document.getElementById(sequence[i]).style.fontWeight="1000"
                if (document.getElementById(sequence[i]).textContent=="O") {
                    document.getElementById(sequence[i]).style.backgroundColor="dodgerblue"
                } else {
                    document.getElementById(sequence[i]).style.backgroundColor="red"
                }
            }
            if (marque=="O") {
                marque="X"
            } else {
                marque="O"
            }              
        }
        const countdownField = document.getElementById("id-bandeau")
        let count = 0;
        let msgfin=""
        if (document.getElementById("id-pat").textContent=="Oui") {
            document.getElementById("ALUI").style.display="none"
            document.getElementById("victoire").textContent="MATCH NUL"
            document.getElementById("victoire").style.display="block"
            document.getElementById("AVOUS").style.display="none"
        }
        win="Non"
        if (document.getElementById("id-victoire").value!="Non") {
            document.getElementById("ALUI").style.display="none"
            document.getElementById("AVOUS").style.display="none"
            win=document.getElementById("id-victoire").value
            document.getElementById("victoire").style.display="block"
            document.getElementById("defaite").style.display="none"
        }
        if (document.getElementById("id-defaite").value!="Non") {
            win=document.getElementById("id-defaite").value
            document.getElementById("defaite").style.display="block"
            document.getElementById("victoire").style.display="none"
            document.getElementById("ALUI").style.display="none"
            document.getElementById("AVOUS").style.display="none"
        }
        if (win != "Non") {
            win=win.split(",")
            for (let i = 0;i<5;i++) {
                document.getElementById(win[i]).style.backgroundColor="yellow"
            }
        }
        if (document.getElementById("id-finmanche").value=="Oui") {
            msgfin="La manche 2 demarre dans "
        }
        if (document.getElementById("id-finpartie").value=="Oui") {
            if (document.getElementById("id-joueur").value==document.getElementById("id-premier").value) {
                if (scor1==scor2) {
                        msgfin="Nul : 1-1. Retour au lobby dans "
                }
                if (scor1>scor2) {
                        msgfin="Victoire : ".concat(scor1,"-",scor2,". Retour au lobby dans ")
                }
                if (scor1<scor2) {
                        msgfin="Défaite : ".concat(scor1,"-",scor2,". Retour au lobby dans ")
                }

            }
            else {
                if (scor1==scor2) {
                        msgfin="Nul : 1-1. Retour au lobby dans "
                }
                if (scor1>scor2) {
                        msgfin="Défaite : ".concat(scor1,"-",scor2,". Retour au lobby dans ")
                }
                if (scor1<scor2) {
                    msgfin="Victoire : ".concat(scor1,"-",scor2,". Retour au lobby dans ")
                }
            }
        }
        if (msgfin.length>0) {
            countdownField.style.display="block"
            let interval = setInterval(function() {
                countdownField.textContent =msgfin.concat(10-count," s")
                if (count >= 10) {
                    clearInterval(interval);
                    if (document.getElementById("id-finpartie").value=="Oui") {
                        document.location.href='/internet'
                    } else {
                        document.getElementById("id-etape").value="début"
                        if (document.getElementById("id-begin").textContent==
                            document.getElementById("id-joueur").value) {
                            document.getElementById("id-jeton").value="Non"
                        } else {
                            document.getElementById("id-jeton").value="Oui"
                        }
                        document.getElementById("id-match").value="2"
                        if (window.innerWidth > window.innerHeight) {
                            document.getElementById("orientation").value="paysage"
                        } else {
                            document.getElementById("orientation").value="portrait"
                        }
                        document.forms["internet"].submit();
                    }
                }
                count++;
            }, 1000);  
        }
    }
}
//fonction ismobile
function ismobile() {
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
        // true for mobile device
        return true
      }else{
        // false for not mobile device
        return false
      }
}