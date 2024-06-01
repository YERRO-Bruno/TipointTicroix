document.addEventListener("DOMContentLoaded", function () {
    //alert("initialisation")
// mise en place plateau de jeu HTLM
    displayGameBoard()

// Click sur le bouton jouer
    document.getElementById("btn-jouer").addEventListener('click', function(e){
        e.preventDefault()
        
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
        document.getElementById("id-defaite").value=="Non") {
        if (document.getElementById(e.target.id).textContent=="") {
            case_clicked = e.target.id.split('/')
            document.getElementById(e.target.id).textContent = marque

            if (marque=="X") {
                document.getElementById(e.target.id).style.color="red"
            } else {
                document.getElementById(e.target.id).style.color="blue"
            }

            e.target.blur()
            document.getElementById("coup-joueur").value=e.target.id
        
            // Affichage "JE REFLECHIT"
            document.getElementById("amoi").style.display="block"
            document.getElementById("avous").style.display="none"
            
            document.forms["grille"].submit();
        } else {
            alert("Case déjà utilisée")
        }
    } else {
        alert("La partie est terminée")
    }
    
    })

// Click du joueur sur le bouton quitter en debut de jeu
document.getElementById("btn-quitter").addEventListener('click', function(e) {
    e.preventDefault()
    document.location.href='http://localhost:8000/'
})

// Click du joueur sur le bouton quitter en cours de jeu
document.getElementById("btn-quitter2").addEventListener('click', function(e) {
    e.preventDefault()
    if (document.getElementById("nb-tour").textContent > "0") {
        if (confirm("Voulez vous revenir à l'accueil?")==true) {
            document.location.href='http://localhost:8000/'
        }
    }
})

// Click du joueur sur le bouton annuler le tour
document.getElementById("btn-annuler").addEventListener('click', function(e) {
    e.preventDefault()
    document.getElementById("id-annuler").value="Oui"
    document.forms["grille"].submit();
    })

// Click du joueur sur le bouton rejouer
document.getElementById("btn-rejouer").addEventListener('click', function(e) {
    e.preventDefault()
    document.location.href='http://localhost:8000/tipointticroix/'
    })

    //var tablx = document.getElementById("table")
    //cellx=document.getElementById("1/1").textContent="X"
    
    //Functions
    //Affichage de la grille
    function displayGameBoard(){
        document.getElementById("id-beginer").textContent="Je joue en premier"
        if (document.getElementById("begin-id").textContent == "Oui") {
            document.getElementById("id-beginer").textContent="Vous jouez en premier"
        }
        if (document.getElementById("id-vous").textContent=="O") {
            document.getElementById("id-vous").style.color = "blue"
            document.getElementById("id-ordi").style.color = "red"
        } else {
            document.getElementById("id-vous").style.color = "red"
            document.getElementById("id-ordi").style.color = "blue"
        }
        document.getElementById("amoi").style.display="none"
        document.getElementById("avous").style.display="none"
        document.getElementById("x-board").style.display="none"
        document.getElementById("btn-annuler").style.display="none"
        document.getElementById("btn-rejouer").style.display="none"
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
        if (document.getElementById("nb-tour").textContent > "0") {
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
                document.getElementById(sequence[i]).textContent=marque
                if (marque=="X") {
                    document.getElementById(sequence[i]).style.color="red"
                } else {
                    document.getElementById(sequence[i]).style.color="blue"
                }
                if (i>sequence_size -3) {
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
            }
        }
    }
})
