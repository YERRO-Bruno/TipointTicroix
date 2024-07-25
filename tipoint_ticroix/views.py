from .models import User, VerifUser, UserConnected
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .functions import coupordi,coupmachine,majgrille,trouve_5, estconnecté
from .functions import nomniveau, nbtour
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
import bcrypt
from django.core.mail import send_mail
from django.http import JsonResponse

#page internet (PvP)
def internet(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
        if request.method == 'POST':
            if request.POST['etape'] =="début":
                #Début
                request.session['SEQUENCE']=[]
                request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
                print("début",request.POST['jeton'],request.POST['joueur'])
                if request.POST["jeton"]=="Oui":
                    request.session['PREMIER']=request.POST['joueur']
                    request.session['SECOND']=request.POST['adversaire']
                    context['joueur']=request.session['PREMIER']
                    context['adversaire']=request.session['SECOND']
                if request.POST["jeton"]=="Non":
                    request.session['PREMIER']=request.POST['adversaire']
                    request.session['SECOND']=request.POST['joueur']
                    context['joueur']=request.session['SECOND']
                    context['adversaire']=request.session['PREMIER']
                request.session['BEGIN']=request.session['PREMIER']
                request.session['MATCH']=int(request.POST['match'])
                if request.session['MATCH']==2:
                    request.session['SCORE1']=int(request.POST['score2'])
                    request.session['SCORE2']=int(request.POST['score1'])
                else:
                    request.session['SCORE1']=int(request.POST['score1'])
                    request.session['SCORE2']=int(request.POST['score2'])

                request.session['TOUR']=1
                context["etape"]="nouveautour"
                context["jeton"]=request.POST['jeton']
                context["match"]=request.session['MATCH']
                context["begin"]=request.session['BEGIN']
                context["premier"]=request.session['PREMIER']
                context["second"]=request.session['SECOND']
                context["score1"]=request.session['SCORE1']
                context["score2"]=request.session['SCORE2']
                context["nbtour"]=1
                context["finpartie"]="Non"
                context["victoire"]="Non"
                context["defaite"]="Non"
                print(context)
                return render(request, "internet.html", context)
            if request.POST['etape'] =="tourjeu":
                #tour de jeu
                print("tourjeu")
                context["finpartie"]="Non"
                context["victoire"]="Non"
                context["defaite"]="Non"
                if request.session['BEGIN']==request.POST['joueur']:
                    if request.POST['jeton']=="Oui":
                        marque="O"
                    else:
                        marque="X"
                else:
                    if request.POST['jeton']=="Oui":
                        marque="X"
                    else:
                        marque="O"
                request.session['GRILLE']=majgrille(request.POST["coupjoueur"],marque,request.session['GRILLE'])
                request.session['SEQUENCE']=request.session['SEQUENCE']+[request.POST["coupjoueur"]]
                context['sequence']=','.join(str(i) for i in request.session['SEQUENCE'])    
                context["nbtour"]=nbtour(request.session['SEQUENCE'])
                res = trouve_5(request.POST["coupjoueur"],marque,request.session['GRILLE'])
                if res != "Non":
                    request.session['.MATCH']=request.session['MATCH']+1
                    if request.POST['jeton']=="Oui":
                        context['defaite']=res
                        context['victoire']="Non"
                        if request.session['PREMIER']==request.POST['joueur']:
                            request.session['SCORE2']=request.session['SCORE2']+1
                            #context['score2']=request.session['SCORE2']
                        else:
                            request.session['SCORE1']=request.session['SCORE1']+1
                            #context['score1']=request.session['SCORE1']
                    else:
                        context['defaite']="Non"
                        context['victoire']=res
                        if request.session['PREMIER']==request.POST['joueur']:
                            request.session['SCORE1']=request.session['SCORE1']+1
                            #context['score1']=request.session['SCORE1']
                        else:
                            request.session['SCORE2']=request.session['SCORE2']+1
                            #context['score2']=request.session['SCORE2']
                    if request.session['MATCH']==2:
                        context['finpartie']="Oui"
                context['jeton']=request.POST['jeton']
                context['joueur']=request.POST['joueur']
                context['adversaire']=request.POST['adversaire']
                context["match"]=request.session['MATCH']
                context["begin"]=request.session['BEGIN']
                context["premier"]=request.session['PREMIER']
                context["second"]=request.session['SECOND']
                context["score1"]=request.session['SCORE1']
                context["score2"]=request.session['SCORE2']
                context["etape"]="nouveautour"
                print(context)
                return render(request, "internet.html", context)
        else:    
            context["etape"]="connexion"
            request.session['MATCH']=0
            return render(request, "internet.html", context)
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
            request.session['EMAIL']=emailx
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
       return render(request, 'register.html',{'email':request.session['EMAIL'],'pseudo':"",'password':""})
    
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
        print("tour : " + str(request.session['TOUR']))
        print("joueur : " + request.POST["coupjoueur"])
        if request.POST["annuler"]=="Oui":
            print("annuler : " + request.POST["annuler"])
            request.session['TOUR']=request.session['TOUR']-1 
            context['tour']=str(request.session['TOUR'])
            seq=request.session['SEQUENCE']
            derniercoup = seq[-1]
            avantdercoup = seq[-2]
            #suppression 2 derniers coups dans SEQUENCE
            seq.pop(-1)
            seq.pop(-1)
            request.session['SEQUENCE']=seq
            context['sequence']=','.join(str(i) for i in request.session['SEQUENCE'])
            #suppression 2 derniers coups dans GRILLE
            grid=request.session['GRILLE']
            ix=int(derniercoup.split("/")[1])
            iy=int(derniercoup.split("/")[0])
            grid[ix][iy]="-"
            ix=int(avantdercoup.split("/")[1])
            iy=int(avantdercoup.split("/")[0])
            grid[ix][iy]="-"
            context['begin']=request.session['BEGIN']
            context['victoire']="Non"
            context['defaite']="Non"
            print(context)
            return render(request, "tipointticroix.html", context)
            
        #MAJ TABLEAU
        if request.session['TOUR']==0 :
            request.session['NIVEAU']=int(request.POST["niveau"])
            if request.POST["check-begin"]=="Non" :
                marqueordi="O"
                marquejoueur="X"
                #le joueur ne commence pas - 1er COUP ORDINATEUR
                #request.session['GRILLE[12][12]="X"
                request.session['GRILLE']=majgrille("12/12",marqueordi,request.session['GRILLE'])
                print("ordi : " + "12/12")
                request.session['SEQUENCE']=request.session['SEQUENCE']+["12/12"]
                context['begin']="Non"
                request.session['BEGIN']="Non"
            else:
                marqueordi="X"
                marquejoueur="O"
                context['begin']="Oui"
                request.session['BEGIN']="Oui"
            request.session['MARQUEORDI']=marqueordi
            request.session['MARQUEJOUEUR']=marquejoueur
            context['nom1']=nomniveau(request.session['NIVEAU'])
            context['niveau']=request.session['NIVEAU']
            context['tour']=str(request.session['TOUR'])
            context['victoire']="Non"
            context['defaite']="Non"
        else :
            marqueordi=request.session['MARQUEORDI']
            marquejoueur=request.session['MARQUEJOUEUR']
            context['nom1']=nomniveau(request.session['NIVEAU'])
            context['niveau']=request.session['NIVEAU']
            context['begin']=request.session['BEGIN']
            context['victoire']="Non"
            context['defaite']="Non"
            #COUP JOUEUR
            request.session['SEQUENCE']=request.session['SEQUENCE']+[request.POST["coupjoueur"]]
            #GRILLE=COUPDUJOUEUR
            request.session['GRILLE']=majgrille(request.POST["coupjoueur"],marquejoueur,request.session['GRILLE'])
            #victoire joueur
            res = trouve_5(request.POST["coupjoueur"],marquejoueur,request.session['GRILLE'])
            if res != "Non":
                context['victoire']=res
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                #print(context) 
                return render(request, "tipointticroix.html", context)

            #COUP ORDINATEUR
            coupordinateur=coupordi(marqueordi,request.session['NIVEAU'],
                request.session['SEQUENCE'],request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coupordinateur]
            #GRILLE=COUPORDINATEUR
            request.session['GRILLE']=majgrille(coupordinateur,marqueordi,request.session['GRILLE'])
            res = trouve_5(coupordinateur,marqueordi,request.session['GRILLE'])
            if res != "Non":
                context['defaite']=res
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                print(context) 
                return render(request, "tipointticroix.html", context)
        context['marquevous']=marquejoueur
        context['marqueordi']=marqueordi
        request.session['TOUR']=request.session['TOUR']+1 
        context['tour']=str(request.session['TOUR'])   
        context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
        return render(request, "tipointticroix.html", context)
    #Appel initial
    request.session['TOUR']=0
    request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
    request.session['SEQUENCE']=[]
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
            request.session['TOUR']=request.session['TOUR']-1 
            context['tour']=str(request.session['TOUR'])
            seq=request.session['SEQUENCE']
            derniercoup = seq[-1]
            avantdercoup = seq[-2]
            #suppression 2 derniers coups dans request.session['SEQUENCE']
            seq.pop(-1)
            seq.pop(-1)
            request.session['SEQUENCE']=seq
            context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
            #suppression 2 derniers coups dans request.session['GRILLE']
            grid=request.session['GRILLE']
            ix=int(derniercoup.split("/")[1])
            iy=int(derniercoup.split("/")[0])
            grid[ix][iy]="-"
            ix=int(avantdercoup.split("/")[1])
            iy=int(avantdercoup.split("/")[0])
            grid[ix][iy]="-"
            context['victoire1']="Non"
            context['victoire2']="Non" 
            context['nom1']=nomniveau(request.session['NIVEAU1'])
            context['nom2']=nomniveau(request.session['NIVEAU2'])
            context['niveau1']=request.session['NIVEAU1']
            context['niveau2']=request.session['NIVEAU2']
            request.session['MODEJEU']="pas à pas"
            context['modejeu']=request.session['MODEJEU']
            context['victoire1']="Non"
            context['victoire2']="Non" 
            print(context)
            return render(request, "machines.html", context)
        #MAJ TABLEAU
        if request.session['TOUR']==0 :
           request.session['SEQUENCE']=[]
           request.session['NIVEAU1']=int(request.POST["niveau1"])
           request.session['NIVEAU2']=int(request.POST["niveau2"])
           request.session['MODEJEU']=request.POST["modejeu"]
           context['tour']=str(request.session['TOUR'])
           context['sequence']=""
        nbcoup=len(request.session['SEQUENCE'])
        if nbcoup%2==0:
            coup=coupmachine("O",request.session['NIVEAU1'],
                             request.session['SEQUENCE'],request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coup]
            request.session['GRILLE']=majgrille(coup,"O",request.session['GRILLE'])
            res = trouve_5(coup,"O",request.session['GRILLE'])
            if res != "Non":
                context['nom1']=nomniveau(request.session['NIVEAU1'])
                context['nom2']=nomniveau(request.session['NIVEAU2'])
                context['niveau1']=request.session['NIVEAU1']
                context['niveau2']=request.session['NIVEAU2']
                context['victoire1']=res
                context['victoire2']="Non"
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                #print(context) 
                return render(request, "machines.html", context)
        else:
            coup=coupmachine("X",request.session['NIVEAU2'],request.session['SEQUENCE'],
                             request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coup]
            request.session['GRILLE']=majgrille(coup,"X",request.session['GRILLE'])
            res = trouve_5(coup,"X",request.session['GRILLE'])
            if res != "Non":
                context['nom1']=nomniveau(request.session['NIVEAU1'])
                context['nom2']=nomniveau(request.session['NIVEAU2'])
                context['niveau1']=request.session['NIVEAU1']
                context['niveau2']=request.session['NIVEAU2']
                context['victoire2']=res
                context['victoire1']="Non"
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                #print(context) 
                return render(request, "machines.html", context)
        context['victoire1']="Non"
        context['victoire2']="Non"
        context['nom1']=nomniveau(request.session['NIVEAU1'])
        print(nomniveau(request.session['NIVEAU1']))
        context['nom2']=nomniveau(request.session['NIVEAU2'])    
        context['niveau1']=request.session['NIVEAU1']
        context['niveau2']=request.session['NIVEAU2']
        context['modejeu']=request.session['MODEJEU']
        request.session['TOUR']=len(request.session['SEQUENCE'])//2+1
        print(request.session['TOUR'])
        context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
        context['tour']=str(request.session['TOUR'])
        #print(context)    
        return render(request, "machines.html", context) 
    request.session['TOUR']=0
    request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
    request.session['SEQUENCE']=[] 
    return render(request, "machines.html", context) 

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