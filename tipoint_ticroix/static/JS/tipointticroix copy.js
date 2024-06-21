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
        //alert(e.target.id)
        case_clicked = e.target.id.split('/')
        document.getElementById(e.target.id).textContent = "O"
        e.target.blur()
        document.getElementById("coup-joueur").value=e.target.id
        // Affichage "JE REFLECHIT"
        document.getElementById("amoi").style.display="block"
        document.getElementById("avous").style.display="none"
        
        document.forms["grille"].submit();
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
        document.getElementById("amoi").style.display="none"
        document.getElementById("avous").style.display="none"
        document.getElementById("x-board").style.display="none"
        if (document.getElementById("nb-tour").textContent > "0") {
            //Affichage "A VOUS DE JOUER"
            document.getElementById("amoi").style.display="none"
            document.getElementById("avous").style.display="block"
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
            let nb_seq=tour
            let marque="X"
            sequence = sequence.split(',')
            if (sequence=="") {
                sequence_size=0
            } else {
                sequence_size=sequence.length
            }
            if (document.getElementById("begin-id").textContent == "Oui") {
                //nb_seq=tour - 1
                marque="O"
            }
            alert("999")
            alert(sequence)
            alert(sequence_size)
            for (let i = 0;i<sequence_size;i++) {
                document.getElementById(sequence[i]).textContent=marque
                if (marque=="X") {
                    marque="O"
                } else {
                    marque="X"
                }

            }
        }
    }
})
