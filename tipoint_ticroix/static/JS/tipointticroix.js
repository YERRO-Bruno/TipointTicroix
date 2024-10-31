document.addEventListener("DOMContentLoaded", function () {
    let précédenteposition=""
    let précédentecolor=""
    let nouvelleposition=""
    let nouvellecolor=""
    précédentecolor=""
    let nbc=25
    //taille de la grille
    if (ismobile()) {
        nbc=18
    } else {
        nbc=25
    }
    
    if (window.innerWidth > window.innerHeight) {    
        h=((window.innerHeight-20)/nbc)+"px"
        fontsz="1vw"
    } else {
        h="4vw"
        fontsz="1vh"
    }
    
    // mise en place plateau de jeu HTLM
    let d1=0
    let d2=0
    displayGameBoard()  
    
    // Click sur le bouton jouer
    document.getElementById("btn-jouer").addEventListener('click', function(e){
        e.preventDefault()
        if (window.innerWidth > window.innerHeight) {
            document.getElementById("orientation").value="paysage"
        } else {
            document.getElementById("orientation").value="portrait"
        }
        if (ismobile()) {
            document.getElementById("joystchecked").value="Oui"
        } else {
            document.getElementById("joystchecked").value="Non"
        }
        document.forms["grille"].submit();
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
        e.preventDefault()
        if (document.getElementById("begin-id").textContent=="Oui") {
            marque="O"
        } else {
            marque="X"
        }
        //test si la case est déjà occupée
        if (document.getElementById("id-victoire").value=="Non" && 
        document.getElementById("id-defaite").value=="Non" &&
        (document.getElementById("id-pat").value=="Non")) {
            if (document.getElementById("joystchecked").value=="Oui") {
                if (précédenteposition !="") {
                    document.getElementById(précédenteposition).style.backgroundColor=précédentecolor
                }
                précédenteposition=e.target.id
                précédentecolor=document.getElementById(e.target.id).style.backgroundColor
                document.getElementById(e.target.id).style.backgroundColor="green"
                document.getElementById(e.target.id).style.fontSize=fontsz
            } else {
                // document.getElementById("joyst").value="Non"
                if (document.getElementById(e.target.id).textContent=="") {
                    // case_clicked = e.target.id.split('/')
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
            }
        } else {
            if (document.getElementById("x-board").style.display=="none") {
                alert("Lancez d'abord la partie!")
            } else{
                alert("La partie est terminée!")
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
    if (document.getElementById("begin-id").textContent=="Oui") {
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
        if (document.getElementById("id-stat").textContent=="Oui") {
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
        } else {
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
        if (document.getElementById("nb-tour").textContent > "0") {
            document.getElementById("id-charger").value="Oui"
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
    document.getElementById("mp-0").style.Height="100%"
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
    let nbc=25
    //taille de la grille
    if (ismobile()) {
        nbc=18
    } else {
        nbc=25
    }
    if (window.innerWidth > window.innerHeight) {
        h=window.innerHeight/parseInt(nbc)         
        fontsz="0.9vw"
    } else {
        h=window.innerWidth/parseInt(nbc)
        fontsz="0.9vh"
        let h1=document.documentElement.scrollHeight
        let h3=window.innerHeight
        d1=(h1-h3)
    }   
    var tableau = document.getElementById("table");
    for (let j = 0; j < nbc ; j++) {
        ligne = tableau.insertRow(-1); // création d'une ligne pour ajout en fin de table
        ligne.id="L"+j
        // création et insertion des cellules dans la nouvelle ligne créée
        for (let i = 0; i < nbc ; i++) {
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
            cell.style.fontWeight="1000"
            cell.style.width = "4vh"
            cell.style.background = "white"
            cell.style.border = "0.1vh solid"
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
            h=h-(diftaille/nbc )
            document.getElementById("table").width=diftaille
            for (let j = 0; j < nbc ; j++) {
                for (let i = 0; i < nbc ; i++) {
                    var idx= j+"/"+i
                    document.getElementById(idx).style.height=h+"px"
                }
            }
        }
    }
    if (document.getElementById("nb-tour").textContent > "0") {
        document.getElementById("cadrej").style.display="block"
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
        if (document.getElementById("joystchecked").value=="Oui") {
            document.getElementById("joyst").checked=true
            document.getElementById("joystick").style.display="block"
        } else {
            document.getElementById("joyst").checked=false
            document.getElementById("joystick").style.display="none"
        }

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
            document.getElementById(sequence[i]).style.fontSize=fontsz
            document.getElementById(sequence[i]).style.color="black"
            if (marque=="X") {
                // document.getElementById(sequence[i]).style.color="red"
                document.getElementById(sequence[i]).style.backgroundColor="lightpink"
            } else {
                //document.getElementById(sequence[i]).style.color="blue"
                document.getElementById(sequence[i]).style.backgroundColor="cyan"
            }
            if (i>sequence_size -3) {
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
        if (document.getElementById("id-sequence").value!="") {
            if (document.getElementById("id-pat").value=="Non" &&
                document.getElementById("id-victoire").value=="Non" &&
                document.getElementById("id-defaite").value=="Non") {
                localStorage.setItem("partiencours",document.getElementById("id-sequence").value)
            }
        }
        if (document.getElementById("id-pat").value=="Oui") {
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
                document.getElementById("id-pat").value="Non"
                document.getElementById("id-victoire").value="Non"
                document.getElementById("id-defaite").value="Non"
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
