document.addEventListener("DOMContentLoaded", function () {
  // mise en place plateau de jeu HTLM
  //displayGameBoard()
  // Click du joueur sur le bouton quitter en cours de jeu
  
  document.getElementById("btn-quitter2").addEventListener('click', function(e) {
    alert("quitter2")
    e.preventDefault()
    if (document.getElementById("nb-tour").textContent > "0") {
      if (confirm("Voulez vous revenir à l'accueil?")==true) {
        document.location.href='/tipointticroix'
      }
    }
  })

})
document.getElementById("btn-manche2").style.display="none"
document.getElementById("btn-rejouer").style.display="none"
displayGameBoard()
if (document.getElementById("id-jeton").textContent=="Non") {
  document.getElementById("ALUI").style.display="block"   
  document.getElementById("AVOUS").style.display="none"
  document.getElementById("victoire").style.display="none"
  document.getElementById("defaite").style.display="none"
  document.getElementById("jeton").value="Non"
  document.getElementById("id-rolesocket").value=document.getElementById("rolesocket").textContent
  //displayGameBoard()
  document.forms["internet"].submit();
}

// Click du joueur sur une des cases
document.getElementById("table").addEventListener('click', function(e) {
  //e.preventDefault()
  if (document.getElementById("id-finpartie").value=="Non") {
     if (document.getElementById("id-jeton").textContent=="Non") {
       alert("Ce n'est pas à vous de jouer")
     } else {
       if (document.getElementById("id-begin").textContent=="Oui") {
         marque="O"
       } else {
         marque="X"
       }
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
         document.getElementById("ALUI").style.display="block"   
         document.getElementById("AVOUS").style.display="none"
         document.getElementById("jeton").value="Oui"
         document.getElementById("id-rolesocket").value=document.getElementById("rolesocket").textContent
         document.getElementById("id-sequence").value=e.target.id   
         document.forms["internet"].submit();
       } else {
           alert("Case déjà utilisée")
        }
      }
  } else {
    alert("la partie est terminée!")
  }
})
  //Functions
  //Affichage de la grille
  function displayGameBoard(){
    if (document.getElementById("id-etape").value=="connexion") {
      document.getElementById("x-board").style.display="none"
    }
    if (document.getElementById("id-etape").value!="connexion") {
      document.getElementById("x-connect").style.display="none"
    }
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
    if (document.getElementById("id-etape").value=="echange") {
      document.getElementById("victoire").style.display="none"
      document.getElementById("defaite").style.display="none"
      if (document.getElementById("id-jeton").textContent=="Oui") {
        document.getElementById("ALUI").style.display="none"
      } else {

        document.getElementById("AVOUS").style.display="none"
      }
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

//si 1ere manche préparation 2eme manche
document.getElementById("btn-manche2").addEventListener('click', function(e) {
  document.getElementById("id-etape").value="change"
  for (let j = 0; j < 25; j++) {
    for (let i = 0; i < 25; i++) {
      var idx= j+"/"+i
      let cell=document.getElementById(idx)
      cell.textContent = ""
    }
    document.getElementById("id-sequence").value=""
  }
  if (document.getElementById("rolesocket").textContent=="client") {
    document.getElementById("id-rolesocket").value="client"
    document.forms["internet"].submit();
  } else {
    document.getElementById("id-rolesocket").value="serveur"    
    document.forms["internet"].submit();
  }
})

document.getElementById("btn-rejouer").addEventListener('click', function(e) {
  document.getElementById("id-etape").value="debut"
  for (let j = 0; j < 25; j++) {
    for (let i = 0; i < 25; i++) {
      var idx= j+"/"+i
      let cell=document.getElementById(idx)
      cell.textContent = ""
    }
  }
  if (document.getElementById("rolesocket").textContent=="client") {
    document.getElementById("id-rolesocket").value="client"
    document.forms["internet"].submit();
  } else {
    document.getElementById("id-rolesocket").value="serveur"    
    document.forms["internet"].submit();
  }
})

document.getElementById("btn-client").addEventListener('click', function(e) {
  //alert("client")
  e.preventDefault()
  document.getElementById("id-etape").value="Connexion"
  document.getElementById("id-rolesocket").value="client"
  document.forms["internet"].submit();
})
document.getElementById("btn-serveur").addEventListener('click', function(e) {
  //alert("serveur")
  e.preventDefault()
  document.getElementById("id-etape").value="Connexion"
  document.getElementById("id-rolesocket").value="serveur"
  document.forms["internet"].submit();
  })

  // Click du joueur sur le bouton quitter en debut de jeu
  document.getElementById("btn-quitter").addEventListener('click', function(e) {
    e.preventDefault()
    document.getElementById("id-etape").value="deconnexion"
    document.forms["internet"].submit()
  })

  