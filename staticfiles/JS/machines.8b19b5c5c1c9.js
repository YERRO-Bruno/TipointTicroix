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

// Click du joueur sur le bouton quitter en debut de jeu
document.getElementById("btn-quitter").addEventListener('click', function(e) {
    e.preventDefault()
    document.location.href='/'
})

// Click du joueur sur le bouton quitter en cours de jeu
document.getElementById("btn-quitter2").addEventListener('click', function(e) {
    e.preventDefault()
    if (document.getElementById("id-victoire1").value!="Non"||
        document.getElementById("id-victoire2").value!="Non") {
            document.location.href='/'
        } else {
            if (confirm("Voulez vous revenir à l'accueil?")==true) {
                document.location.href='/'
            }
    }
})

// Click du joueur sur le bouton annuler le tour
document.getElementById("btn-annuler").addEventListener('click', function(e) {
    e.preventDefault()
    document.getElementById("id-annuler").value="Oui"
    document.forms["grille"].submit();
})
// Click du joueur sur le bouton enregistrer position
document.getElementById("btn-save").addEventListener('click', function(e) {
    e.preventDefault()
    localStorage.setItem("enreg",document.getElementById("id-sequence").value)
})
// Click du joueur sur le bouton charger position
document.getElementById("btn-load").addEventListener('click', function(e) {
    e.preventDefault()
    document.getElementById("id-charger").value="Oui"
    document.getElementById("id-sequence").value=localStorage.getItem("enreg")
    document.forms["grille"].submit();
    })

// Click du joueur sur le bouton rejouer
document.getElementById("btn-rejouer").addEventListener('click', function(e) {
    e.preventDefault()
    document.location.href='/machines'
    })

//Functions
//Affichage de la grille
function displayGameBoard(){
    document.getElementById("AMACHINE1").style.display="none"
    document.getElementById("AMACHINE2").style.display="none"
    document.getElementById("x-board").style.display="none"
    document.getElementById("btn-annuler").style.display="none"
    document.getElementById("btn-load").style.display="none"
    document.getElementById("btn-save").style.display="none"
    document.getElementById("btn-rejouer").style.display="none"
    // creation lignes du tableau
    var cell, ligne;
    h=window.innerHeight/25        
    fontsz="0.9vw"
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
            cell.style.height = h+"px"
            cell.style.fontWeight="1000"
            cell.style.width = "4vh"
            cell.style.background = "white"
            cell.style.border = "0.1vh solid"
            cell.borderSpacing ="0"
            cell.style.textAlign = "center"
        }
    }
    if (document.getElementById("nb-tour").textContent > "0") {
        if (document.getElementById("modejeu").textContent=="pas à pas") {
            document.getElementById("coupsuivant").style.display="block"
            document.getElementById("btn-save").style.display="block"
            document.getElementById("btn-load").style.display="block"
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
        //Affichage des coups joués
        let tour=parseInt(document.getElementById("nb-tour").textContent)
        let sequence=document.getElementById("id-sequence").value
        sequence = sequence.split(',')
        let nbcoup=sequence.length
        var marque="O"
        for (let i = 0;i<nbcoup;i++) {
            document.getElementById(sequence[i]).textContent=marque
            document.getElementById(sequence[i]).style.fontSize="0.8vw"
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
        if (document.getElementById("id-pat").textContent=="Oui") {
            alert("Plus de case diponible - Match nul")
            document.getElementById("victoire1").textContent="MATCH NUL"
            document.getElementById("victoire2").textContent=""
            document.getElementById("victoire1").style.display="block"
            document.getElementById("victoire2").style.display="none"
            document.getElementById("AMACHINE1").style.display="none"
            document.getElementById("AMACHINE2").style.display="none"
            document.getElementById("btn-load").style.display="none"
            document.getElementById("btn-save").style.display="none"
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
            document.getElementById("btn-annuler").style.display="block"  
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

