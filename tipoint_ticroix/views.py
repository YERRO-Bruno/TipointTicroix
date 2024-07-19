from .models import User, VerifUser, UserConnected
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from .functions import coupordi,coupmachine,majgrille,trouve_5, estconnecté
from .functions import nomniveau,connecclient,connecserveur, nbtour, estconnecté_async
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
import bcrypt
from django.core.mail import send_mail
from django.http import JsonResponse

#page test
def test(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
        if request.method == 'POST':
            if request.POST['etape'] =="début":
                #Début
                print("début")
                if request.POST["jeton"]=="Oui":
                    settings.PREMIER=request.POST['joueur']
                    settings.SECOND=request.POST['adversaire']
                    context['joueur']=settings.PREMIER
                    context['adversaire']=settings.SECOND
                    settings.BEGIN="Oui"
                else:
                    settings.PREMIER=request.POST['adversaire']
                    settings.SECOND=request.POST['joueur']
                    context['joueur']=settings.SECOND
                    context['adversaire']=settings.PREMIER
                    settings.BEGIN="Non"
                settings.MATCH=1
                settings.SCORE1=0
                settings.SCORE2=0
                settings.TOUR=1
                context["etape"]="nouveautour"
                context["jeton"]=request.POST['jeton']
                context["match"]=settings.MATCH
                context['begin']=settings.BEGIN
                context["premier"]=settings.PREMIER
                context["second"]=settings.SECOND
                context["score1"]=settings.SCORE1
                context["score2"]=settings.SCORE2
                context["nbtour"]=settings.TOUR
                context["finpartie"]="Non"
                context["victoire"]="Non"
                context["defaite"]="Non"
                return render(request, "test.html", context)
            if request.POST['etape'] =="tourjeu":
                #tour de jeu
                print("tourjeu")
                if settings.BEGIN=="Oui":
                    marque="O"
                else:
                    marque="X"
                context["finpartie"]="Non"
                context["victoire"]="Non"
                context["defaite"]="Non"
                majgrille(request.POST["coupjoueur"],marque)    
                settings.SEQUENCE=settings.SEQUENCE+[request.POST["coupjoueur"]]
                res = trouve_5(request.POST["coupjoueur"],marque)
                if res != "Non":
                    settings.MATCH=settings.MATCH+1
                    if request.POST['jeton']=="Oui":
                        context['defaite']=res
                        context['victoire']="Non"
                        if settings.BEGIN=="Oui":
                            settings.SCORE2=settings.SCORE2+1
                            context['score2']=settings.SCORE2
                        else:
                            settings.SCORE1=settings.SCORE1+1
                            context['score1']=settings.SCORE1
                    else:
                        context['defaite']="Non"
                        context['victoire']=res
                        if settings.BEGIN=="Oui":
                            settings.SCORE1=settings.SCORE1+1
                            context['score1']=settings.SCORE1
                        else:
                            settings.SCORE2=settings.SCORE2+1
                            context['score2']=settings.SCORE2
                    if settings.MATCH>2:
                        context['finpartie']="Oui"
                    
                if request.POST['jeton']=="Oui":
                    context['jeton']="Oui"
                else:
                    context['jeton']="Non"
                if settings.BEGIN=="Oui":
                    context['joueur']=settings.PREMIER
                    context['adversaire']=settings.SECOND
                else:
                    context['joueur']=settings.SECOND
                    context['adversaire']=settings.PREMIER
                context["match"]=settings.MATCH
                context['begin']=settings.BEGIN
                context["premier"]=settings.PREMIER
                context["second"]=settings.SECOND
                context["score1"]=settings.SCORE1
                context["score2"]=settings.SCORE2
                context["nbtour"]=nbtour()
                context['sequence']=settings.SEQUENCE
                print("seq",context['sequence'])
                context["etape"]="nouveautour"
                return render(request, "test.html", context)
        else:    
            context["etape"]="connexion"
            settings.MATCH=0
            return render(request, "test.html", context)
    else:
        context["connexion"]="Non"
        return redirect('/tipointticroix/connect',context)

#page accueil
def accueil(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    else:
        context["connexion"]="Non"
        context["connec"]=connec[1]
            
    return render(request, "accueil.html", context)

#déconnexion
def logout_view(request):
    logout(request)
    #messages.add_message(request, messages.INFO, "Vous êtes déconnecté")
    return redirect("/tipointticroix")

def preregister(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        userx=User.objects.filter(email=emailx)
        if len(userx)==0:
            #emailx n'est pas encore enregistré
            verifuser=VerifUser.objects.filter(email=emailx)
            if len(verifuser)>0:
                verifuser[0].delete()
            verifuser=VerifUser.objects.create(email=emailx)
            original_code = get_random_string(length=8)
            salt = bcrypt.gensalt()
            crypted_code = bcrypt.hashpw(original_code.encode('utf-8'), salt)
            hash_verif = crypted_code.decode('utf-8')
            verifuser.codeverif = hash_verif
            verifuser.save()
            #envoi code verification
            recipient_email = emailx
            mail_subject = "Code de verification pour l'inscription à tipointticroix.com"
            mail_message = "bonjour, \n"
            mail_message = mail_message + "Veuiller trouvez ci-dessous le code de verification" \
                                            " pour votre inscription au en tant qu'administrateur du site tipointticroix.com :\n"
            mail_message = mail_message + "\n"
            mail_message = mail_message + original_code
            mail_message = mail_message + "\n"
            mail_message = mail_message + "\n"
            mail_message = mail_message + "Cordialement"

            try:
                send_mail(mail_subject, mail_message, 'brunoyerro@gmail.com', {emailx},
                            fail_silently=False)
            except Exception as error:
                print('mail error')
                print(error)
                return render(request,'register.html',{'email':emailx,'errorVerif':"error Mailing"})
            settings.EMAIL=emailx
            return redirect('/tipointticroix/register')
        return render(request, 'preregister.html',
                      {'errorVerif': "Email déjà existant", 'email': emailx})

    else:
        return render(request, 'preregister.html')

#Inscription
def register(request):
    if request.method == 'POST':
        context = {}
        emailx = request.POST['email']
        passwordx = request.POST['password']
        pseudox = request.POST['pseudo']
        verifx = request.POST['verification']
        #test d'unicité email et pseudo
        userx=User.objects.filter(email=emailx)
        if len(userx)>0:
            return render(request, 'register.html',
                        {'errorinscription': "Email déjà existant", 'email': emailx})
        userx=User.objects.filter(pseudo=pseudox)
        if len(userx)>0:
            return render(request, 'register.html',
                        {'errorinscription': "pseudo déjà existant", 'email': emailx})   
        #récupération et test code verification
        print("cherche verifuser")
        verifuser=VerifUser.objects.get(email=emailx)
        print("cherche verifuser2")
        if verifuser is not None:
                if bcrypt.checkpw(verifx.encode('utf-8'),verifuser.codeverif.encode('utf-8')):
                    print("code ok",emailx)
                    try:
                        userx = User.objects.create_user(email=emailx, password=passwordx)
                        userx.pseudo=pseudox
                        userx.save()
                        verifuser.delete()
                    except Exception as error:
                        print(error)
                    return redirect('/tipointticroix/connect')       
        else:
            return render(request, 'register.html',
                        {'errorinscription': "Code inexact", 'email': emailx})
    else:
       return render(request, 'register.html',{'email':settings.EMAIL,'pseudo':"",'password':""})
    
#connexion
def connect(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        passwordx = request.POST['password']
        userConnected = authenticate(email=emailx, password=passwordx)
        if userConnected is not None:
            request.session['email'] = emailx
            request.session['password'] = passwordx
            login(request, userConnected )
            #messages.add_message(request, messages.INFO, "Vous êtes connecté.")
            return redirect('/tipointticroix')
        else:
            #messages.add_message(request, messages.INFO, "Vous n' avez pas été authentifié")
            return render(request, 'connect.html', {'errorLogin': "Email et/ou mot de passe erroné"})
    else:
        return render(request, 'connect.html')

#page tipointticroix
def tipointticroix(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    else:
        context["connexion"]="Non"
        context["connec"]="Vous"
    print(context)
    if request.method == 'POST':
        print("tour : " + str(settings.TOUR))
        print("joueur : " + request.POST["coupjoueur"])
        if request.POST["annuler"]=="Oui":
            print("annuler : " + request.POST["annuler"])
            settings.TOUR=settings.TOUR-1 
            context['tour']=str(settings.TOUR)
            seq=settings.SEQUENCE
            derniercoup = seq[-1]
            avantdercoup = seq[-2]
            #suppression 2 derniers coups dans settings.SEQUENCE
            seq.pop(-1)
            seq.pop(-1)
            settings.SEQUENCE=seq
            context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
            #suppression 2 derniers coups dans settings.GRILLE
            grid=settings.GRILLE
            ix=int(derniercoup.split("/")[1])
            iy=int(derniercoup.split("/")[0])
            grid[ix][iy]="-"
            ix=int(avantdercoup.split("/")[1])
            iy=int(avantdercoup.split("/")[0])
            grid[ix][iy]="-"
            context['begin']=settings.BEGIN
            context['victoire']="Non"
            context['defaite']="Non"
            print(context)
            return render(request, "tipointticroix.html", context)
            
        #MAJ TABLEAU
        if settings.TOUR==0 :
            settings.NIVEAU=int(request.POST["niveau"])
            if request.POST["check-begin"]=="Non" :
                marqueordi="O"
                marquejoueur="X"
                #le joueur ne commence pas - 1er COUP ORDINATEUR
                #settings.GRILLE[12][12]="X"
                majgrille("12/12",marqueordi)
                print("ordi : " + "12/12")
                settings.SEQUENCE=settings.SEQUENCE+["12/12"]
                context['begin']="Non"
                settings.BEGIN="Non"
            else:
                marqueordi="X"
                marquejoueur="O"
                context['begin']="Oui"
                settings.BEGIN="Oui"
            settings.MARQUEORDI=marqueordi
            settings.MARQUEJOUEUR=marquejoueur
            context['nom1']=nomniveau(settings.NIVEAU)
            context['niveau']=settings.NIVEAU
            context['tour']=str(settings.TOUR)
            context['victoire']="Non"
            context['defaite']="Non"
        else :
            marqueordi=settings.MARQUEORDI
            marquejoueur=settings.MARQUEJOUEUR
            context['nom1']=nomniveau(settings.NIVEAU)
            context['niveau']=settings.NIVEAU
            context['begin']=settings.BEGIN
            context['victoire']="Non"
            context['defaite']="Non"
            #COUP JOUEUR
            settings.SEQUENCE=settings.SEQUENCE+[request.POST["coupjoueur"]]
            #settings.GRILLE=COUPDUJOUEUR
            majgrille(request.POST["coupjoueur"],marquejoueur)
            #victoire joueur
            res = trouve_5(request.POST["coupjoueur"],marquejoueur)
            if res != "Non":
                context['victoire']=res
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                #print(context) 
                return render(request, "tipointticroix.html", context)

            #COUP ORDINATEUR
            coupordinateur=coupordi(marqueordi)
            settings.SEQUENCE=settings.SEQUENCE+[coupordinateur]
            #settings.GRILLE=COUPORDINATEUR
            majgrille(coupordinateur,marqueordi)
            res = trouve_5(coupordinateur,marqueordi)
            if res != "Non":
                context['defaite']=res
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                print(context) 
                return render(request, "tipointticroix.html", context)
        context['marquevous']=marquejoueur
        context['marqueordi']=marqueordi
        settings.TOUR=settings.TOUR+1 
        context['tour']=str(settings.TOUR)   
        context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
        #print(settings.GRILLE)
        #print(context) 
        return render(request, "tipointticroix.html", context)
    #Appel initial
    settings.TOUR=0
    settings.GRILLE = [["-"] * 25 for _ in range(25)]
    settings.SEQUENCE=[]
    return render(request, "tipointticroix.html", context)

#page machines
def machines(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    else:
        context["connexion"]="Non"
        context["connec"]=connec[1]
    print(context)
    if request.method == 'POST':
        if request.POST["annuler"]=="Oui":
            print("annuler : " + request.POST["annuler"])
            settings.TOUR=settings.TOUR-1 
            context['tour']=str(settings.TOUR)
            seq=settings.SEQUENCE
            derniercoup = seq[-1]
            avantdercoup = seq[-2]
            #suppression 2 derniers coups dans settings.SEQUENCE
            seq.pop(-1)
            seq.pop(-1)
            settings.SEQUENCE=seq
            context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
            #suppression 2 derniers coups dans settings.GRILLE
            grid=settings.GRILLE
            ix=int(derniercoup.split("/")[1])
            iy=int(derniercoup.split("/")[0])
            grid[ix][iy]="-"
            ix=int(avantdercoup.split("/")[1])
            iy=int(avantdercoup.split("/")[0])
            grid[ix][iy]="-"
            context['victoire1']="Non"
            context['victoire2']="Non" 
            context['nom1']=nomniveau(settings.NIVEAU1)
            context['nom2']=nomniveau(settings.NIVEAU2)
            context['niveau1']=settings.NIVEAU1
            context['niveau2']=settings.NIVEAU2
            settings.MODEJEU="pas à pas"
            context['modejeu']=settings.MODEJEU
            context['victoire1']="Non"
            context['victoire2']="Non" 
            print(context)
            return render(request, "machines.html", context)
        #MAJ TABLEAU
        if settings.TOUR==0 :
           settings.SEQUENCE=[]
           settings.NIVEAU1=int(request.POST["niveau1"])
           settings.NIVEAU2=int(request.POST["niveau2"])
           settings.MODEJEU=request.POST["modejeu"]
           context['tour']=str(settings.TOUR)
           context['sequence']=""
        nbcoup=len(settings.SEQUENCE)
        if nbcoup%2==0:
            coup=coupmachine("O",settings.NIVEAU1)
            settings.SEQUENCE=settings.SEQUENCE+[coup]
            majgrille(coup,"O")
            res = trouve_5(coup,"O")
            if res != "Non":
                context['nom1']=nomniveau(settings.NIVEAU1)
                context['nom2']=nomniveau(settings.NIVEAU2)
                context['niveau1']=settings.NIVEAU1
                context['niveau2']=settings.NIVEAU2
                context['victoire1']=res
                context['victoire2']="Non"
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                #print(context) 
                return render(request, "machines.html", context)
        else:
            coup=coupmachine("X",settings.NIVEAU2)
            settings.SEQUENCE=settings.SEQUENCE+[coup]
            majgrille(coup,"X")
            res = trouve_5(coup,"X")
            if res != "Non":
                context['nom1']=nomniveau(settings.NIVEAU1)
                context['nom2']=nomniveau(settings.NIVEAU2)
                context['niveau1']=settings.NIVEAU1
                context['niveau2']=settings.NIVEAU2
                context['victoire2']=res
                context['victoire1']="Non"
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                #print(context) 
                return render(request, "machines.html", context)
        context['victoire1']="Non"
        context['victoire2']="Non"
        context['nom1']=nomniveau(settings.NIVEAU1)
        print(nomniveau(settings.NIVEAU1))
        context['nom2']=nomniveau(settings.NIVEAU2)    
        context['niveau1']=settings.NIVEAU1
        context['niveau2']=settings.NIVEAU2
        context['modejeu']=settings.MODEJEU
        settings.TOUR=len(settings.SEQUENCE)//2+1
        print(settings.TOUR)
        context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
        context['tour']=str(settings.TOUR)
        #print(context)    
        return render(request, "machines.html", context) 
    settings.TOUR=0
    settings.GRILLE = [["-"] * 25 for _ in range(25)]
    settings.SEQUENCE=[] 
    return render(request, "machines.html", context) 

#page internet
def internet(request):
    
    #import asyncio
    #from websockets.sync.client import connect
    #with connect("ws://localhost:8765") as websocket:
    #with connect("ws://172.18.0.6:8765") as websocket:
    
    #    websocket.send("Hello world!")
    #    message = websocket.recv()
    #    print(f"Received from server : {message}")
    


    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    context['victoire']="Non"
    context['defaite']="Non"
    context['finpartie']="Non"
    if request.method == 'POST':
        if request.POST['etape'] =="Connexion":
            print("connexion")
            #connexion
            settings.SCORESERVEUR=0  
            settings.SCORECLIENT=0  
            context['score1']=settings.SCORE1
            context['score2']=settings.SCORE2
            if request.POST['rolesocket'] =="client":
                print("client")
                if request.POST['serveur'] !="":
                    settings.SERVEURHOST=request.POST['serveur']
                    msg,mySocket=connecclient(request.POST['serveur'],connec[1])
                    context['begin']="Non"
                    context['jeton']="Non"
                    context['match']="1"
                    context['premier']=msg
                    context["second"]=connec[1]
                    context["rolesocket"]="client"
                    settings.BEGINCLIENT="Non"
                    settings.MATCH="1"
                    settings.NOMSERVEUR=context['premier']
                    settings.NOMCLIENT=connec[1]
                    settings.PREMIER=settings.NOMSERVEUR
                    settings.SECOND=settings.NOMCLIENT
                    settings.SOCKETSERVEUR = mySocket
                    context['etape']="echange"
                    context['finpartie']="Non" 
                    context['nbtour']=nbtour()   
                    return render(request, "internet.html", context)
                else:
                    print("noserver")
                    context["noserver"]="Renseigner l'ip de votre adversaire"
                    return render(request, "internet.html", context)
            if request.POST['rolesocket'] =="serveur":
                print("connect serveur")
                msg=connecserveur(request.POST['serveur'],connec[1],)
                context['begin']="Oui"
                context['jeton']="Oui"
                context['match']="1"
                context['premier']=connec[1]
                context["second"]=msg
                context["rolesocket"]="serveur"
                settings.BEGINSERVEUR="Oui"
                settings.NOMSERVEUR=context['premier']
                settings.PREMIER=settings.NOMSERVEUR
                settings.SECOND=settings.NOMCLIENT
                settings.NOMCLIENT=context['second']
                #settings.SOCKETCLIENT = mySocket
                context['etape']="echange"
                context['finpartie']="Non"
                context['nbtour']=nbtour()    
                return render(request, "internet.html", context)
        
        if request.POST['etape'] =="deconnexion":
            if settings.SOCKETSERVEUR!="":
                settings.SOCKETSERVEUR.close()
            if settings.SOCKETCLIENT!="":
                settings.SOCKETCLIENT.close()
            print("cloture des socket")
            return redirect('/tipointticroix')
        
        if request.POST['etape'] =="debut":
            #1ere manche
            print("debut")
            context['match']="1"
            context['victoire']="Non"
            context['defaite']="Non"
            settings.SCORE1=0
            settings.SCORE2=0
            settings.MATCH="1"
            context['score1']=0
            context['score2']=0
            settings.PREMIER=settings.NOMSERVEUR
            settings.SECOND=settings.NOMCLIENT
            context['premier']=settings.PREMIER
            context["second"]=settings.SECOND
            settings.GRILLE=[["-"] * 25 for _ in range(25)]
            settings.SEQUENCE=[]
            context['finpartie']="Non"   
            context['etape']="echange"
            context['nbtour']=nbtour()   
            if request.POST['rolesocket'] =="client":
                context['begin']="Non"
                context['jeton']="Non"               
                context["rolesocket"]="client"
                settings.BEGINCLIENT="Non"
                return render(request, "internet.html", context)
            if request.POST['rolesocket'] =="serveur":
                context['begin']="Oui"
                context['jeton']="Oui"
                context["rolesocket"]="serveur"    
                settings.BEGINSERVEUR="Oui"
                return render(request, "internet.html", context)
            
        if request.POST['etape'] =="change":
            #2eme manche
            print("change")
            context['victoire']="Non"
            context['defaite']="Non"
            settings.PREMIER=settings.NOMCLIENT
            settings.SECOND=settings.NOMSERVEUR
            context['premier']=settings.PREMIER
            context["second"]=settings.SECOND
            context['finpartie']="Non"
            context['nbtour']=nbtour()
            settings.GRILLE=[["-"] * 25 for _ in range(25)]
            settings.SEQUENCE=[]   
            context['sequence']=','.join([str(i) for i in settings.SEQUENCE])   
            if request.POST['rolesocket'] =="client":
                settings.GRILLE=[["-"] * 25 for _ in range(25)]
                settings.SEQUENCE=[]
                context['begin']="Oui"
                context['jeton']="Oui"
                context['match']="2"
                if settings.MATCH=="1":
                    res=settings.SCORE1
                    settings.SCORE1=settings.SCORE2
                    settings.SCORE2=res
                settings.MATCH="2"
                context['score1']=settings.SCORE1
                context['score2']=settings.SCORE2
                context["rolesocket"]="client"
                settings.BEGINCLIENT="Oui"
                context['etape']="echange"
                return render(request, "internet.html", context)
            if request.POST['rolesocket'] =="serveur":
                settings.GRILLE=[["-"] * 25 for _ in range(25)]
                settings.SEQUENCE=[]
                context['begin']="Non"
                context['jeton']="Non"
                context['match']="2"
                context["rolesocket"]="serveur"
                if settings.MATCH=="1":
                    res=settings.SCORE1
                    settings.SCORE1=settings.SCORE2
                    settings.SCORE2=res
                settings.MATCH="2"
                context['score1']=settings.SCORE1
                context['score2']=settings.SCORE2    
                settings.BEGINSERVEUR="Non"
                context['etape']="echange"
                return render(request, "internet.html", context)
            
        if request.POST['etape'] =="echange":
            #echanges
            print("echange",request.POST['rolesocket'],request.POST['jeton'])
            context['score1']=settings.SCORE1
            context['score2']=settings.SCORE2
            context['finpartie']="Non"
            context['victoire']="Non"
            context['defaite']="Non"
            context['etape']="echange"
            context['premier']=settings.PREMIER
            context["second"]=settings.SECOND
            if request.POST['jeton']=="Oui":
                context['jeton']="Non"
                if request.POST['rolesocket'] =="client":
                    #COUP JOUEUR
                    context['begin']=settings.BEGINCLIENT
                    context['match']=settings.MATCH
                    settings.SEQUENCE=settings.SEQUENCE+[request.POST["coupjoueur"]]
                    context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                    majgrille(request.POST["coupjoueur"],"X")
                    res = trouve_5(request.POST["coupjoueur"],"X")
                    if res != "Non":
                        context['victoire']=res
                        context['defaite']="Non"
                        if settings.MATCH=="1":
                            settings.SCORE2=settings.SCORE2+1
                            context['score2']=settings.SCORE2
                        else:
                            settings.SCORE1=settings.SCORE1+1
                            context['score1']=settings.SCORE1
                        if settings.MATCH=="2":
                            context['finpartie']="Oui"
                        context['etape']="change"
                        context['jeton']="Fin"
                        print("victoire") 
                    context["rolesocket"]="client"
                    settings.SOCKETSERVEUR.send(request.POST["coupjoueur"].encode('utf-8'))

                if request.POST['rolesocket'] =="serveur":
                    #COUP JOUEUR
                    context['begin']=settings.BEGINSERVEUR
                    context['match']=settings.MATCH
                    settings.SEQUENCE=settings.SEQUENCE+[request.POST["coupjoueur"]]
                    context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                    majgrille(request.POST["coupjoueur"],"O")
                    res = trouve_5(request.POST["coupjoueur"],"O")
                    if res != "Non":
                        context['victoire']=res
                        context['defaite']="Non"
                        if settings.MATCH=="1":
                            settings.SCORE1=settings.SCORE1+1
                            context['score1']=settings.SCORE1
                        else:
                            settings.SCORE2=settings.SCORE2+1
                            context['score2']=settings.SCORE2
                        if settings.MATCH=="2":
                            context['finpartie']="Oui"
                        context['etape']="change"
                        context['jeton']="Fin"
                        print("victoire")   
                    context["rolesocket"]="serveur"
                    settings.SOCKETCLIENT.send(request.POST["coupjoueur"].encode('utf-8'))
                context['nbtour']=nbtour()
                return render(request, "internet.html", context)
            else:
                context['jeton']="Oui"
                context['match']=settings.MATCH
                context['etape']="echange"
                context['premier']=settings.PREMIER
                context["second"]=settings.SECOND
                context['finpartie']="Non"
                msgserveur=""
                if request.POST['rolesocket'] =="client":
                    msgserveur=settings.SOCKETSERVEUR.recv(1024)
                    print("fromserveur : ",msgserveur)
                    res = trouve_5(msgserveur,"O")
                    if res != "Non":
                        context['victoire']="Non"
                        context['defaite']=res
                        context['score1']=settings.SCORE1
                        context['score2']=settings.SCORE2
                        context['etape']="change"
                        context['jeton']="Fin"
                        if settings.MATCH=="2":
                            context['finpartie']="Oui"
                        print("defaite")
                    context['begin']=settings.BEGINCLIENT
                    context["rolesocket"]="client"
                    context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                if request.POST['rolesocket'] =="serveur":
                    context['premier']=settings.PREMIER
                    msgclient=settings.SOCKETCLIENT.recv(1024)
                    print(msgclient.decode('utf-8'),"X")
                    res = trouve_5(msgclient.decode('utf-8'),"X")
                    if res != "Non":
                        context['victoire']="Non"
                        context['defaite']=res
                        context['score1']=settings.SCORE1
                        context['score2']=settings.SCORE2
                        context['finpartie']="Oui"
                        context['etape']="echange"
                        context['jeton']="Fin"
                        if settings.MATCH=="2":
                            context['finpartie']="Oui"
                        print("defaite")
                    context['begin']=settings.BEGINSERVEUR
                    context["rolesocket"]="serveur"
                    context['premier']=settings.PREMIER
                    context["second"]=settings.SECOND
                    context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['nbtour']=nbtour()
                return render(request, "internet.html", context)                   
    else:
        settings.SEQUENCE=[]
        import socket
        if connec[0]:
            import asyncio
            from websockets.server import serve
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ipaddress = s.getsockname()[0]
            s.close()
            print(ipaddress)
            context['ip']=ipaddress
            context["etape"]="connexion"
            return render(request, "internet.html", context)
        else:
            return redirect('/tipointticroix/connect')

#page apropos
def apropos(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    else:
        context["connexion"]="Non"
        context["connec"]=connec[1]
    return render(request, "apropos.html", context)

#page mentions
def mentions(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
    else:
        context["connexion"]="Non"
        context["connec"]=connec[1]
    return render(request, "mentions.html", context)

#liste des usersconnected
def api_userconnecteds(request):
    userconnecteds=UserConnected.objects.all()
    userconnecteds_json=[{'pseudo':userconnected.pseudo} for userconnected in userconnecteds]
    return JsonResponse(userconnecteds_json,safe=False)