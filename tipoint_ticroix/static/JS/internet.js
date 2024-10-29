document.addEventListener("DOMContentLoaded", function () {
    let précédenteposition=""
    let précédentecolor=""
    let nouvelleposition=""
    let nouvellecolor=""
    précédentecolor=""
    //taille de la grille
    if (ismobile()) {
        let nbc=18
    } else {
        let nbc=25
    }
    
    if (window.innerWidth > window.innerHeight) {    
        h=((window.innerHeight-20)/nbc)+"px"
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

    //click sur la  checkbox Positionnement et validation du coup
    document.getElementById("joyst").addEventListener('click', () => {
        if (document.getElementById("joystchecked").value=="Oui") {
            document.getElementById("joystchecked").value="Non"
            document.getElementById("joyst").checked=false
            document.getElementById("joystick").style.display="none"
        } else {
            document.getElementById("joystchecked").value="Oui"
            document.getElementById("joyst").checked=true
            document.getElementById("joystick").style.display="block"
        }
    })

    // Click du joueur sur une des cases
    document.getElementById("table").addEventListener('click', function(e) {
        if ((document.getElementById("id-victoire").value=="Non" &&
        document.getElementById("id-defaite").value=="Non" &&
        document.getElementById("id-pat").value=="Non")) {

            if (document.getElementById("id-jeton").value=="Non") {
                alert("Ce n'est pas à vous de jouer")
            } else {
                if (document.getElementById("joystchecked").value=="Oui") {
                    if (précédenteposition !="") {
                        document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
                    }
                    précédenteposition=e.target.id
                    précédentecolor=document.getElementById(e.target.id).style.backgroundColor
                    document.getElementById(e.target.id).style.backgroundColor="green"
                    document.getElementById(e.target.id).style.fontSize=fontsz
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
                            document.getElementById(e.target.id).style.backgroundColor="bisque"
                        } else {
                            document.getElementById(e.target.id).style.color="blue"
                            document.getElementById(e.target.id).style.backgroundColor="lightcyan"
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
            }
        } else {
            if (document.getElementById("nb-tour").textContent="0") {
                alert("Choisissez votre adversaire!")
            } else {
                alert("partie terminée !")
              }
        }
    })

    //click du joueur sur haut
    document.getElementById("id-haut").addEventListener('click', function(e) {
        if (précédenteposition !="") {        
            document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
            let iprec=parseInt(précédenteposition.split("/")[0])
            if (iprec >0) {
                iprec=iprec-1
            } else {
                alert("bord atteint")
            }            
            let yprec=précédenteposition.split("/")[1]
            nouvelleposition=iprec+"/"+yprec
            précédentecolor=document.getElementById(nouvelleposition).style.backgroundColor
            document.getElementById(nouvelleposition).style.backgroundColor="green"
            précédenteposition=nouvelleposition
        } else {
            sequence=document.getElementById("id-sequence").value
            sequence = sequence.split(',')
            if (sequence=="") {
                précédenteposition ="12/12"
                précédentecolor=document.getElementById("12/12").style.backgroundColor
                document.getElementById("12/12").style.backgroundColor="green"
            } else {
                précédenteposition=sequence[sequence.length-1]
                précédentecolor=document.getElementById(précédenteposition).style.backgroundColor
                document.getElementById(précédenteposition).style.backgroundColor="green"
            }
        }
    })

    //click du joueur sur bas
    document.getElementById("id-bas").addEventListener('click', function(e) {
        if (précédenteposition !="") {        
            document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
            let iprec=parseInt(précédenteposition.split("/")[0])
            if (iprec <nbc - 1) {
                iprec=iprec+1
            } else {
                alert("bord atteint")
            }            
            let yprec=précédenteposition.split("/")[1]
            nouvelleposition=iprec+"/"+yprec
            précédentecolor=document.getElementById(nouvelleposition).style.backgroundColor
            document.getElementById(nouvelleposition).style.backgroundColor="green"
            précédenteposition=nouvelleposition
        } else {
            sequence=document.getElementById("id-sequence").value
            sequence = sequence.split(',')
            if (sequence=="") {
                précédenteposition ="12/12"
                précédentecolor=document.getElementById("12/12".style.backgroundColor)
                document.getElementById("12/12".style.backgroundColor)="green"
            } else {
                précédenteposition=sequence[sequence.length-1]
                précédentecolor=document.getElementById(précédenteposition).style.backgroundColor
                document.getElementById(précédenteposition).style.backgroundColor="green"
            }
        }
    })
    //click du joueur sur droite
    document.getElementById("id-droite").addEventListener('click', function(e) {
        if (précédenteposition !="") {        
            document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
            let yprec=parseInt(précédenteposition.split("/")[1])
            if (yprec <nbc - 1) {
                yprec=yprec+1
            } else {
                alert("bord atteint")
            }            
            let iprec=précédenteposition.split("/")[0]
            nouvelleposition=iprec+"/"+yprec
            précédentecolor=document.getElementById(nouvelleposition).style.backgroundColor
            document.getElementById(nouvelleposition).style.backgroundColor="green"
            précédenteposition=nouvelleposition
        } else {
            sequence=document.getElementById("id-sequence").value
            sequence = sequence.split(',')
            if (sequence=="") {
                précédenteposition ="12/12"
                précédentecolor=document.getElementById("12/12".style.backgroundColor)
                document.getElementById("12/12".style.backgroundColor)="green"
            } else {
                précédenteposition=sequence[sequence.length-1]
                précédentecolor=document.getElementById(précédenteposition).style.backgroundColor
                document.getElementById(précédenteposition).style.backgroundColor="green"
            }
        }
    })

    //click du joueur sur gauche
    document.getElementById("id-gauche").addEventListener('click', function(e) {
        if (précédenteposition !="") {        
            document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
            let yprec=parseInt(précédenteposition.split("/")[1])
            if (yprec >0) {
                yprec=yprec-1
            } else {
                alert("bord atteint")
            }            
            let iprec=précédenteposition.split("/")[0]
            nouvelleposition=iprec+"/"+yprec
            précédentecolor=document.getElementById(nouvelleposition).style.backgroundColor
            document.getElementById(nouvelleposition).style.backgroundColor="green"
            précédenteposition=nouvelleposition
        } else {
            sequence=document.getElementById("id-sequence").value
            sequence = sequence.split(',')
            if (sequence=="") {
                précédenteposition ="12/12"
                précédentecolor=document.getElementById("12/12".style.backgroundColor)
                document.getElementById("12/12".style.backgroundColor)="green"
            } else {
                précédenteposition=sequence[sequence.length-1]
                précédentecolor=document.getElementById(précédenteposition).style.backgroundColor
                document.getElementById(précédenteposition).style.backgroundColor="green"
            }
        }
    })

    //click sur validation
    document.getElementById("id-validation").addEventListener('click', function(e) {
        if (document.getElementById("id-begin").textContent=="Oui") {
            marque="O"
        } else {
            marque="X"
        }
        if (document.getElementById(précédenteposition).textContent=="") {
            // case_clicked = précédenteposition.split('/')
            document.getElementById(précédenteposition).textContent = marque
            document.getElementById(précédenteposition).style.fontSize=fontsz
            if (marque=="X") {
                document.getElementById(précédenteposition).style.color="red"
                document.getElementById(précédenteposition).style.backgroundColor="bisque"
            } else {
                document.getElementById(précédenteposition).style.color="blue"
                document.getElementById(précédenteposition).style.backgroundColor="lightcyan"
            }
            document.getElementById("coup-joueur").value=précédenteposition
            document.getElementById("id-etape").value="tourjeu"
            document.getElementById("id-jeton").value="Non"
            //alert("jeu")
            socket.send('tourjeu,'.concat(document.getElementById("id-connec").textContent,
            ",",document.getElementById("id-adversaire").value,",",précédenteposition))
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
            alert("Case déjà utilisée!")
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
        if (msg[0]=="PB") {
            alert("perte de connection")
        }


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

        if (msg[0]=="PB") {
            alert("perte de connexion")
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
                if (ismobile()) {
                    document.getElementById("joystchecked").value="Oui"                    
                } else {
                    document.getElementById("joystchecked").value="Non"
                }
                if (window.innerWidth > window.innerHeight) {
                    document.getElementById("orientation").value="paysage"
                } else {
                    document.getElementById("orientation").value="portrait"
                }
                document.forms["internet"].submit();
            } else {
                socket.send('refus,'.concat(document.getElementById("id-connec").textContent,',',msg[1]))
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
            if (ismobile()) {
                document.getElementById("joystchecked").value="Oui"                    
            } else {
                document.getElementById("joystchecked").value="Non"
            }
            if (window.innerWidth > window.innerHeight) {
                document.getElementById("orientation").value="paysage"
            } else {
                document.getElementById("orientation").value="portrait"
            }
            document.forms["internet"].submit();
        } 

        if (msg[0]=="refus") {
            alert(msg[1]+" n'accepte pas votre proposition de jouer !")
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
    let d1=0
    let d2=0
    displayGameBoard()
})

//Functions
//Affichage de la grille
function displayGameBoard(){
    // alert(document.getElementById("id-etape").value)
    if (document.getElementById("id-etape").value=="nouveautour") {
        document.getElementById("x-jouer").style.display="none"
        document.getElementById("x-board").style.display="block"
        document.getElementById("cadrej").style.display="block"
        if (document.getElementById("joystchecked").value=="Oui") {
            document.getElementById("joyst").checked=true
            document.getElementById("joystick").style.display="block"
        } else {
            document.getElementById("joyst").checked=false
            document.getElementById("joystick").style.display="none"
        }

    }

    // creation lignes du tableau
    var cell, ligne;
    if (window.innerWidth > window.innerHeight) {
        h=window.innerHeight/nbc        
        fontsz="0.9vw"
      } else {
        h=window.innerWidth/nbc
        fontsz="0.9vh"
        let h1=document.documentElement.scrollHeight
        let h3=window.innerHeight
        d1=(h1-h3)
      }   
    h=h
    var tableau = document.getElementById("table");
    for (let j = 0; j < nbc; j++) {
      
        ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
                                        // le paramètre est dans ce cas (-1)

    // création et insertion des cellules dans la nouvelle ligne créée
      for (let i = 0; i < nbc; i++) {
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
          cell.style.height = h+"px"
          cell.style.width = "4vh"
          cell.style.background = "white"
          cell.style.border = "1px solid"
          cell.borderSpacing ="0"
          cell.style.textAlign = "center"
      }
    }    
    if (window.innerWidth < window.innerHeight) {
        let h1=document.documentElement.scrollHeight
        let h3=window.innerHeight
        d2=(h1-h3)
        let diftaille=d2-d1
        if (diftaille>0) {
            h=h-(diftaille/nbc)
            document.getElementById("table").width=diftaille
            for (let j = 0; j < nbc; j++) {
                for (let i = 0; i < nbc; i++) {
                    var idx= j+"/"+i
                    document.getElementById(idx).style.height=h+"px"
                }
            }
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
    } else {
        
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