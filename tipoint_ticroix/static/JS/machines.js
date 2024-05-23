document.addEventListener("DOMContentLoaded", function () {
//    alert("initialisation machines")
// mise en place plateau de jeu HTLM
    displayGameBoard()
})
// Click sur le bouton jouer
document.getElementById("btn-jouer").addEventListener('click', function(e){
    e.preventDefault()
    document.forms["grille"].submit();
})

// Click du joueur sur une des cases
document.getElementById("table").addEventListener('click', function(e) {
    e.preventDefault()
    alert("Action impossible. partie entre machines")
    })

// Click du joueur sur le bouton quitter
document.getElementById("btn-quitter").addEventListener('click', function(e) {
    e.preventDefault()
    if (confirm("Voulez vous revenir à l'accueil?")==true) {
        document.location.href='http://localhost:8000/'
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
    document.location.href='http://localhost:8000/tipointticroix/machines'
    })

//Functions
//Affichage de la grille
function displayGameBoard(){
    document.getElementById("AMACHINE1").style.display="none"
    document.getElementById("AMACHINE2").style.display="none"
    document.getElementById("x-board").style.display="none"
    document.getElementById("btn-annuler").style.display="none"
    document.getElementById("btn-rejouer").style.display="none"
    if (document.getElementById("nb-tour").textContent > "0") {
        if (document.getElementById("modejeu").textContent=="pas à pas") {
            document.getElementById("coupsuivant").style.display="block"
            if (document.getElementById("nb-tour").textContent > "1") {
                document.getElementById("btn-annuler").style.display="block"
            }
        } else {
            document.getElementById("coupsuivant").style.display="none"
        }
        res=document.getElementById("id-sequence").value
        res=res.split(',')
        aqui=res.length % 2
        if (aqui==0){
            document.getElementById("AMACHINE2").style.display="none"
            document.getElementById("AMACHINE1").style.display="block"
        } else {
            document.getElementById("AMACHINE1").style.display="none"
            document.getElementById("AMACHINE2").style.display="block"
        }
        document.getElementById("victoire1").style.display="none"
        document.getElementById("victoire2").style.display="none"
        
        //Effacement JOUER - Apparition BOARD
        document.getElementById("x-jouer").style.display="none"
        document.getElementById("x-board").style.display="block"
        // creation lignes du tableau
        var cell, ligne;
        var tableau = document.getElementById("table");
        const nbt = document.getElementById("nb-tour").textContent
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
        //Affichage des coups joués
        let tour=parseInt(document.getElementById("nb-tour").textContent)
        let sequence=document.getElementById("id-sequence").value
        sequence = sequence.split(',')
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
        if (document.getElementById("id-victoire1").value!="Non") {
            win=document.getElementById("id-victoire1").value
            document.getElementById("victoire1").style.display="block"
        }
        if (document.getElementById("id-victoire2").value!="Non") {
            win=document.getElementById("id-victoire2").value
            document.getElementById("victoire2").style.display="block"
        }
        if (win != "Non") {
            document.getElementById("AMACHINE1").style.display="none"
            document.getElementById("AMACHINE2").style.display="none"
            document.getElementById("btn-rejouer").style.display="blocK"
            document.getElementById("btn-annuler").style.display="none"  
            win=win.split(",")
            for (let i = 0;i<5;i++) {
                document.getElementById(win[i]).style.backgroundColor="yellow"
            }
        } else {
            if (document.getElementById("modejeu").textContent=="auto") {
                setTimeout(() => {
                    document.forms["grille"].submit()
                  }, 1000);
            }
        }
    }
}
function espace_pressé(evt) {
    if (document.getElementById("nb-tour").textContent > "0") {
        if(window.event) evt = window.event;
            if (evt.type == "keypress" & evt.keyCode > 0) {
                if (evt.keyCode==32) {
                    document.forms["grille"].submit();
                }
            }
        }
    }
document.onkeypress = espace_pressé;

