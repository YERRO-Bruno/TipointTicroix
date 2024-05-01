document.addEventListener("DOMContentLoaded", function () {

   // mise en place plateau de jeu HTLM
    displayGameBoard()
    document.getElementById("table").addEventListener('click', function(e) {
        e.preventDefault()
        alert(e.target.id)
        case_clicked = e.target.id.split('/')
        document.getElementById(e.target.id).textContent = "O"

        e.target.blur()

    })
    var tablx = document.getElementById("table")
    // cellx = tablx.getElementsByTagName('tr')[0].getElementsByTagName('td')[0]
    cellx=document.getElementById("0/0").textContent="X"
    cellx.fontSize= "smaller"
    // cellx.textContent="X"

    // cellx.style.textAlign = "center"

//Functions

    function displayGameBoard(){

        var cell, ligne;
        var tableau = document.getElementById("table");
        // nombre de lignes dans la table (avant ajout de la ligne)

        // creation lignes du tableau
        for (let j = 0; j < 22; j++) {
            ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
                                       // le paramètre est dans ce cas (-1)

        // création et insertion des cellules dans la nouvelle ligne créée
            for (let i = 0; i < 22; i++) {
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
                cell.style.height = "2vh"
                cell.style.width = "2vh"
                cell.style.background = "white"
                cell.style.border = "1px solid"
                cell.borderSpacing ="0"
                cell.style.textAlign = "center"
            }
        }
    }
})