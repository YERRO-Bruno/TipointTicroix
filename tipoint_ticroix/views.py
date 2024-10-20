from .models import User, VerifUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from .functions import coupordi, coupmachine, majgrille, trouve_5, estconnecté
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
import bcrypt
from django.core.mail import send_mail
import smtplib

#from functions import coupordi
import json
# Create your views here.

#Teste si l'ordinateur à gagner
#si oui renvoie la sequences des 5 positions allignées
#sinon renvoie ""


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
    print(context)
    return render(request, "accueil.html", context)

#déconnexion
def logout_view(request):
    logout(request)
    #messages.add_message(request, messages.INFO, "Vous êtes déconnecté")
    return redirect("/")

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
        verifuser=VerifUser.objects.get(email=emailx)
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
            return redirect('/')
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
            context['niveau']=settings.NIVEAU
            context['tour']=str(settings.TOUR)
            context['victoire']="Non"
            context['defaite']="Non"
        else :
            marqueordi=settings.MARQUEORDI
            marquejoueur=settings.MARQUEJOUEUR
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
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
        return render(request, "internet.html", context)
    else:
        return redirect('/tipointticroix/connect')
