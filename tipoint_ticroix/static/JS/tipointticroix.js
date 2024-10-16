document.addEventListener("DOMContentLoaded", function () {
//alert("initialisation")
// mise en place plateau de jeu HTLM
    displayGameBoard()

// Click sur le bouton jouer
    document.getElementById("btn-jouer").addEventListener('click', function(e){
        e.preventDefault()
        if (window.innerWidth > window.innerHeight) {
            document.getElementById("orientation").value="paysage"
          } else {
            document.getElementById("orientation").value="portrait"
          }
        document.forms["grille"].submit();
    })

// Click du joueur sur une des cases
    document.getElementById("table").addEventListener('click', function(e) {
        e.preventDefault()
        if (document.getElementById("begin-id").textContent=="Oui") {
            marque="O"
        } else {
            marque="X"
        }
        //test si la case est déjà occupée
        if (document.getElementById("id-victoire").value=="Non" && 
            document.getElementById("id-defaite").value=="Non" &&
            (document.getElementById("id-pat").textContent=="Non")) {
            if (document.getElementById(e.target.id).textContent=="") {
                case_clicked = e.target.id.split('/')
                document.getElementById(e.target.id).textContent = marque
                document.getElementById(e.target.id).style.fontSize="0.9vw"
                if (marque=="X") {
                    document.getElementById(e.target.id).style.color="red"
                } else {
                    document.getElementById(e.target.id).style.color="blue"
                }

                e.target.blur()
                document.getElementById("coup-joueur").value=e.target.id
                document.getElementById("amoi").style.display="block"
                document.getElementById("avous").style.display="none"
                if (window.innerWidth > window.innerHeight) {
                    document.getElementById("orientation").value="paysage"
                  } else {
                    document.getElementById("orientation").value="portrait"
                  }
                document.forms["grille"].submit();                
            } else {
                alert("Case déjà utilisée!")
            }
        } else {
            if (document.getElementById("x-board").style.display=="none") {
                alert("Lancez d'abord la partie!")
            } else{
                alert("La partie est terminée!")
            }
        }
        
    })

// Click du joueur sur le bouton quitter en debut de jeu
    document.getElementById("btn-quitter").addEventListener('click', function(e) {
        e.preventDefault()
        document.location.href="/"
    })

// Click du joueur sur le bouton quitter en cours de jeu
    document.getElementById("btn-quitter2").addEventListener('click', function(e) {
        e.preventDefault()
        if (document.getElementById("nb-tour").textContent > "0") {
            if (document.getElementById("id-victoire").value=="Non" &&
                document.getElementById("id-defaite").value=="Non") {
                if (confirm("Voulez vous revenir à l'accueil?")==true) {
                    document.location.href="/"
                }
            } else {
                document.location.href="/"
            }
        }
    })

// Click du joueur sur le bouton annuler le tour
    document.getElementById("btn-annuler").addEventListener('click', function(e) {
        if (confirm("En cas d'annulation cette partie ne comptera pas dans les statistiques?")) {
            e.preventDefault()
            document.getElementById("id-annuler").value="Oui"
            if (window.innerWidth > window.innerHeight) {
                document.getElementById("orientation").value="paysage"
              } else {
                document.getElementById("orientation").value="portrait"
              }
            document.forms["grille"].submit();
        }
    })

// Click du joueur sur le bouton rejouer
    document.getElementById("btn-rejouer").addEventListener('click', function(e) {
        e.preventDefault()
        document.location.href='/jeu'
    })

//changement de l'orientation de l'ecran
    window.screen.orientation.addEventListener("change", function() {
        let sequence=document.getElementById("id-sequence").value
        if (document.getElementById("nb-tour").textContent > "0") {
            if (sequence.split(',')!="") {
                document.getElementById("id-charger").value="Oui"
            }
        } else {
            document.getElementById("debut").value="Oui"
        }
             
        if (window.innerWidth > window.innerHeight) {
            document.getElementById("orientation").value="paysage"
          } else {
            document.getElementById("orientation").value="portrait"
          }
        document.forms["grille"].submit();
    });
})
//Functions
//Affichage de la grille
function displayGameBoard(){
    document.getElementById("x-jouer").style.display="block"
    document.getElementById("x-board").style.display="none"
    if (document.getElementById("id-vous").textContent=="O") {
        document.getElementById("vous").style.color = "blue"
        document.getElementById("id-vous").style.color = "blue"
        document.getElementById("ordi").style.color = "red"
        document.getElementById("id-ordi").style.color = "red"
    } else {
        document.getElementById("vous").style.color = "red"
        document.getElementById("id-vous").style.color = "red"
        document.getElementById("ordi").style.color = "blue"
        document.getElementById("id-ordi").style.color = "blue"
    }
    document.getElementById("amoi").style.display="none"
    document.getElementById("avous").style.display="none"
    document.getElementById("btn-annuler").style.display="none"
    document.getElementById("btn-rejouer").style.display="none"
    var cell, ligne;
    if (window.innerWidth > window.innerHeight) {
        h=((window.innerHeight-20)/25)+"px"
    } else {
        h="4vw"
    }
    var tableau = document.getElementById("table");
    for (let j = 0; j < 25; j++) {
        ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
        ligne.id="L"+j
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
            // cell.style.height = h+"px"
            cell.style.fontWeight="1000"
            cell.style.width = "4vh"
            cell.style.background = "white"
            cell.style.border = "1px solid"
            cell.borderSpacing ="0"
            cell.style.textAlign = "center"
        }
    }
    if (document.getElementById("nb-tour").textContent > "0") {
        if (document.getElementById("id-sequence").value!="") {
            localStorage.setItem("partiencours",document.getElementById("id-sequence").value)
        }
        if (document.getElementById("nb-tour").textContent > "1") {
            document.getElementById("btn-annuler").style.display="block"
        }
        document.getElementById("victoire").style.display="none"
        document.getElementById("defaite").style.display="none"
        //Affichage "A VOUS DE JOUER"
        document.getElementById("amoi").style.display="none"
        document.getElementById("avous").style.display="block"
        //Effacement JOUER - Apparition BOARD
        document.getElementById("x-jouer").style.display="none"
        document.getElementById("x-board").style.display="block"
        document.getElementById("joystick").style.display="block"

        // creation lignes du tableau
        
        const nbt = document.getElementById("nb-tour").textContent
        //Affichage des coups joués
        let tour=parseInt(document.getElementById("nb-tour").textContent)
        
        let sequence=document.getElementById("id-sequence").value
        let nb_seq=tour
        let marque="O"
        sequence = sequence.split(',')
        if (sequence=="") {
            sequence_size=0
        } else {
            sequence_size=sequence.length
        }
        marque="O"
        for (let i = 0;i<sequence_size;i++) {
            setTimeout(() => {
              }, 1000);
            document.getElementById(sequence[i]).textContent=marque
            document.getElementById(sequence[i]).style.fontSize="1vw"
            if (marque=="X") {
                document.getElementById(sequence[i]).style.color="red"
            } else {
                document.getElementById(sequence[i]).style.color="blue"
            }
            if (i>sequence_size -3) {
                document.getElementById(sequence[i]).style.fontWeight="1000"
                if (document.getElementById(sequence[i]).textContent=="O") {
                    document.getElementById(sequence[i]).style.backgroundColor="DeepSkyBlue"
                } else {
                    document.getElementById(sequence[i]).style.backgroundColor="Pink"
                }
            }
            if (marque=="O") {
                marque="X"
            } else {
                marque="O"
            }  
        }
        if (document.getElementById("id-pat").textContent=="Oui") {
            alert("Plus de case diponible - Match nul")
            document.getElementById("victoire").textContent="MATCH NUL"
            document.getElementById("victoire").style.display="block"
            document.getElementById("btn-rejouer").style.display="block"
            document.getElementById("btn-annuler").style.display="none"
            document.getElementById("amoi").style.display="none"
        document.getElementById("avous").style.display="none"
        }
        win="Non"
        if (document.getElementById("id-victoire").value!="Non") {
            win=document.getElementById("id-victoire").value
            document.getElementById("victoire").style.display="block"
        }
        if (document.getElementById("id-defaite").value!="Non") {
            win=document.getElementById("id-defaite").value
            document.getElementById("defaite").style.display="block"
        }
        if (win != "Non") {
            document.getElementById("avous").style.display="none"
            document.getElementById("btn-rejouer").style.display="blocK"
            document.getElementById("btn-annuler").style.display="none"
            win = win.split(',')  
            for (let i = 0;i<5;i++) {
                document.getElementById(win[i]).style.backgroundColor="yellow"
            }
            localStorage.removeItem("partiencours")
        }
    } else {
        //debut de partie tour=0 - Demande si on veut reprendre une partie interrompue
        if(localStorage.getItem("partiencours") != null){
            if (confirm("Voulez-vous reprendre la dernière partie?")==true) {
                document.getElementById("id-charger").value="Oui"
                document.getElementById("id-sequence").value=localStorage.getItem("partiencours")
                if (window.innerWidth > window.innerHeight) {
                    document.getElementById("orientation").value="paysage"
                  } else {
                    document.getElementById("orientation").value="portrait"
                  }
                document.forms["grille"].submit();
            } else {
                localStorage.removeItem("partiencours")
            }
        }
    }
}
