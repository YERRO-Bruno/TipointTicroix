from .models import User, VerifUser, Game
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .functions import coupordi,coupmachine,majgrille,trouve_5, estconnecté
from .functions import nomniveau, nbtour, finpartie
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
import bcrypt
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Count, Sum, Case, When, IntegerField, FloatField
from django.db.models.functions import Cast
from django.conf import settings

def error_404(request, exception):
    return render(request, '404.html', status=404)

#page internet (PvP)
def internet(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
        if request.method == 'POST':
            if request.POST['etape'] =="début":
                print("etape début")
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
                if request.session['MATCH']==1:
                    request.session['SCORE1']=0
                    request.session['SCORE2']=0
                if request.session['MATCH']==2:
                    sc2=request.session['SCORE1']
                    request.session['SCORE1']=request.session['SCORE2']
                    request.session['SCORE2']=sc2
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
                        finpartie(connec[1],"H",False)
                        context['victoire']="Non"
                        if request.session['PREMIER']==request.POST['joueur']:
                            request.session['SCORE2']=request.session['SCORE2']+1
                            context['score2']=request.session['SCORE2']
                        else:
                            request.session['SCORE1']=request.session['SCORE1']+1
                            context['score1']=request.session['SCORE1']
                    else:
                        context['defaite']="Non"
                        context['victoire']=res
                        finpartie(connec[1],"H",True)
                        if request.session['PREMIER']==request.POST['joueur']:
                            request.session['SCORE1']=request.session['SCORE1']+1
                            context['score1']=request.session['SCORE1']
                        else:
                            request.session['SCORE2']=request.session['SCORE2']+1
                            context['score2']=request.session['SCORE2']
                    context['finmanche']="Oui"
                    if request.session['MATCH']==2:
                        context['finpartie']="Oui"
                if len(request.session['SEQUENCE'])==625:
                    context['pat']="Oui"
                    context["begin"]=request.session['BEGIN']
                    context['joueur']=request.POST['joueur']
                    context['adversaire']=request.POST['adversaire']
                    context["premier"]=request.session['PREMIER']
                    context["second"]=request.session['SECOND']
                    request.session['SCORE1']=request.session['SCORE1']+0.5
                    request.session['SCORE2']=request.session['SCORE2']+0.5
                    if request.session['SCORE1']%2==0:
                        context["score1"]= round(request.session['SCORE1'],0)
                    else:
                        context["score1"]="{:.1f}".format(request.session['SCORE1'])
                    if request.session['SCORE2']%2==0:
                        context["score2"]= round(request.session['SCORE2'],0)
                    else:
                        context["score2"]="{:.1f}".format(request.session['SCORE2'])
                    context["match"]=request.session['MATCH']
                    request.session['TOUR']=request.session['TOUR']+1 
                    context['tour']=str(request.session['TOUR'])   
                    context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                    context["etape"]="nouveautour"
                    context['finmanche']="Oui"
                    if request.session['MATCH']==2:
                        context['finpartie']="Oui"
                    return render(request, "internet.html", context)
                context['jeton']=request.POST['jeton']
                context['joueur']=request.POST['joueur']
                context['adversaire']=request.POST['adversaire']
                context["match"]=request.session['MATCH']
                context["begin"]=request.session['BEGIN']
                context["premier"]=request.session['PREMIER']
                context["second"]=request.session['SECOND']
                if isinstance(request.session['SCORE1'],int):
                    context["score1"]= round(request.session['SCORE1'],0)
                else:
                    context["score1"]="{:.1f}".format(request.session['SCORE1'])
                if isinstance(request.session['SCORE1'],int):
                    context["score2"]= round(request.session['SCORE2'],0)
                else:
                    context["score2"]="{:.1f}".format(request.session['SCORE2'])
                context["etape"]="nouveautour"
                return render(request, "internet.html", context)
        else:    
            context["etape"]="connexion"
            request.session['MATCH']=0
            return render(request, "internet.html", context)
    else:
        context["connexion"]="Non"
        return redirect('/connect',context)

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
    if settings.DEBUG==True:
        context['debug']= "True"
    else:
        context['debug']= "False"  
    if request.method == 'POST':
        request.session['orientation']=request.POST['orientation']
        context["orientation"]=request.session['orientation']
        if request.session['orientation']=="portrait":
            return render(request, "accueilportrait.html", context)
        else:
            return render(request, "accueilpaysage.html", context)
    else:     
        return render(request, "accueil.html", context)

#desinscription
def desinscription(request):
    connec=estconnecté(request)
    userx=User.objects.get(pseudo=connec[1])
    userx.delete()
    return redirect("/")


#déconnexion
def logout_view(request):
    logout(request)
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
                print('mail error',error)
                return render(request,'register.html',{'email':emailx,'errorVerif':"error Mailing"})
            request.session['EMAIL']=emailx
            return redirect('/register')
        return render(request, 'preregister.html',
                      {'errorVerif': "Email déjà existant", 'email': emailx})

    else:
        return render(request, 'preregister.html')

#Inscription
def register(request):
    if request.method == 'POST':
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
                    try:
                        userx = User.objects.create_user(email=emailx, password=passwordx)
                        userx.pseudo=pseudox
                        userx.save()
                        verifuser.delete()
                    except Exception as error:
                        print(error)
                    return redirect('/connect')       
        else:
            return render(request, 'register.html',
                        {'errorinscription': "Code inexact", 'email': emailx})
    else:
       return render(request, 'register.html',{'email':request.session['EMAIL'],'pseudo':"",'password':""})

#Demande de code pour changement de mot de passe en cas d'oubli
def prepassword(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        userx=User.objects.filter(email=emailx)
        if len(userx)>0:
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
                print('mail error',error)
                return render(request,'register.html',{'email':emailx,'errorVerif':"error Mailing"})
            request.session['EMAIL']=emailx
            return redirect('/modifpassword')
        return render(request, 'prepassword.html',
                      {'errorVerif': "Email inexistant", 'email': emailx})
    else:
        return render(request, 'prepassword.html')
    
#changement mot de passe
def modifpassword(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        passwordx = request.POST['password']
        verifx = request.POST['verification']
        userx=User.objects.filter(email=emailx)        
        if len(userx)>0:
            #récupération et test code verification
            verifuser=VerifUser.objects.get(email=emailx)
            if verifuser is not None:
                    if bcrypt.checkpw(verifx.encode('utf-8'),verifuser.codeverif.encode('utf-8')):
                        print("code ok",emailx)
                        try:
                            userx=User.objects.get(email=emailx)
                            userx.set_password(passwordx)
                            userx.save()
                            verifuser.delete()
                        except Exception as error:
                            print(error)
                        return redirect('/connect')       
            else:
                return render(request, 'register.html',
                            {'errorinscription': "Code inexact", 'email': emailx})
        else:
            return render(request, 'register.html',
                        {'errorinscription': "Email déjà existant", 'email': emailx})

    else:
       return render(request, 'modifpassword.html',{'email':request.session['EMAIL'],'pseudo':"",'password':""})

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
            return redirect('/')
        else:
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
    if request.method == 'POST':
        if request.POST["debut"]=="Oui":
            #Appel initial
            request.session["stat"]="Oui"
            request.session['TOUR']=0
            request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
            request.session['SEQUENCE']=[]
            context["orientation"]=request.POST['orientation']
            context["tour"]="0"
            request.session['orientation']=request.POST['orientation']
            if request.POST['orientation']=="paysage":
                return render(request, "tipointticroixpaysage.html", context)
            else:
                return render(request, "tipointticroixportrait.html", context)

        print("tour : " + str(request.session['TOUR']))
        print("joueur : " + request.POST["coupjoueur"])
        if request.POST["annuler"]=="Oui":
            request.session["stat"]="Non"
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
            context['pat']="Non"
            context["orientation"]=request.POST['orientation']
            request.session['orientation']=request.POST['orientation']
            if request.POST['orientation']=="paysage":
                return render(request, "tipointticroixpaysage.html", context)
            else:
                return render(request, "tipointticroixportrait.html", context)
        if request.POST["charger"]=="Oui":
            print("charger : " + request.POST["charger"])
            request.session['SEQUENCE']=request.POST['sequence'].split(",")
            marque="O"
            request.session['GRILLE']=[["-"] * 25 for _ in range(25)]
            if len(request.POST['sequence'])>0:
                for coup in request.session['SEQUENCE']:
                    request.session['GRILLE']=majgrille(coup,marque,request.session['GRILLE'])
                    if marque=="O":
                        marque="X"
                    else:
                        marque="O"
            marqueordi=request.session['MARQUEORDI']
            marquejoueur=request.session['MARQUEJOUEUR']
            context['marquevous']=marquejoueur
            context['marqueordi']=marqueordi
            context['nom1']=nomniveau(request.session['NIVEAU'])
            context['niveau']=request.session['NIVEAU']
            context['begin']=request.session['BEGIN']
            context['pat']=request.POST["pat"]
            context['victoire']=request.POST["victoire"]
            context['defaite']=request.POST["defaite"]
            context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
            request.session['TOUR']=len(request.session['SEQUENCE'])//2+1
            context['tour']=str(request.session['TOUR'])
            context["orientation"]=request.POST['orientation']
            request.session['orientation']=request.POST['orientation']    
            if request.POST['orientation']=="paysage":
                request.session['orientation']="paysage"
                return render(request, "tipointticroixpaysage.html", context)
            else:
                request.session['orientation']="portrait"
                return render(request, "tipointticroixportrait.html", context)
        #MAJ TABLEAU
        if request.session['TOUR']==0:
            request.session['orientation']=request.POST['orientation']
            request.session['TOUR']=0
            request.session['SEQUENCE']=[]
            request.session['NIVEAU']=int(request.POST["niveau"])
            if request.POST["check-begin"]=="Non" :
                marqueordi="O"
                marquejoueur="X"
                #le joueur ne commence pas - 1er COUP ORDINATEUR
                request.session['GRILLE']=majgrille("12/12",marqueordi,request.session['GRILLE'])
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
            context['pat']="Non"
        else :
            marqueordi=request.session['MARQUEORDI']
            marquejoueur=request.session['MARQUEJOUEUR']
            context['nom1']=nomniveau(request.session['NIVEAU'])
            context['niveau']=request.session['NIVEAU']
            context['begin']=request.session['BEGIN']
            context['victoire']="Non"
            context['defaite']="Non"
            context['pat']="Non"
            #COUP JOUEUR
            request.session['SEQUENCE']=request.session['SEQUENCE']+[request.POST["coupjoueur"]]        
            request.session['GRILLE']=majgrille(request.POST["coupjoueur"],marquejoueur,request.session['GRILLE'])
            #easter egg
            if marquejoueur=="O":
                if len(request.session['SEQUENCE'])==7:
                    if request.session['GRILLE'][0][0]=='O': 
                        if request.session['GRILLE'][24][0]=='O':
                            if request.session['GRILLE'][0][24]=='O':
                                if request.session['GRILLE'][24][24]=='O':
                                    return render(request, "easteregg.html")
            else:
                if len(request.session['SEQUENCE'])==8:
                    if request.session['GRILLE'][0][0]=='X': 
                        if request.session['GRILLE'][24][0]=='X':
                            if request.session['GRILLE'][0][24]=='X':
                                if request.session['GRILLE'][24][24]=='X':
                                    return render(request, "easteregg.html")
            #victoire joueur
            res = trouve_5(request.POST["coupjoueur"],marquejoueur,request.session['GRILLE'])
            if res != "Non":
                context['victoire']=res
                if request.session["stat"]=="Oui":
                    if connec[0]:
                        finpartie(connec[1],str(request.session['NIVEAU']),True)
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                context["orientation"]=request.POST['orientation']
                request.session['orientation']=request.POST['orientation']
                if request.POST['orientation']=="paysage":
                    return render(request, "tipointticroixpaysage.html", context)
                else:
                    return render(request, "tipointticroixportrait.html", context)
            if len(request.session['SEQUENCE'])==625:
                context['pat']="Oui"
                context['marquevous']=marquejoueur
                context['marqueordi']=marqueordi
                request.session['TOUR']=request.session['TOUR']+1 
                context['tour']=str(request.session['TOUR'])   
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context["orientation"]=request.POST['orientation']
                request.session['orientation']=request.POST['orientation']
                if request.POST['orientation']=="paysage":
                    return render(request, "tipointticroixpaysage.html", context)
                else:
                    return render(request, "tipointticroixportrait.html", context)
            #COUP ORDINATEUR
            coupordinateur=coupordi(marqueordi,request.session['NIVEAU'],
                request.session['SEQUENCE'],request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coupordinateur]
            
            #GRILLE=COUPORDINATEUR
            request.session['GRILLE']=majgrille(coupordinateur,marqueordi,request.session['GRILLE'])
            res = trouve_5(coupordinateur,marqueordi,request.session['GRILLE'])
            if res != "Non":
                context['defaite']=res
                if connec[0]:
                    finpartie(connec[1],str(request.session['NIVEAU']),False)
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                context["orientation"]=request.POST['orientation']
                request.session['orientation']=request.POST['orientation']
                if request.POST['orientation']=="paysage":
                    return render(request, "tipointticroixpaysage.html", context)
                else:
                    return render(request, "tipointticroixportrait.html", context)
            if len(request.session['SEQUENCE'])==625:
                context['pat']="Oui"
                context['marquevous']=marquejoueur
                context['marqueordi']=marqueordi
                request.session['TOUR']=request.session['TOUR']+1 
                context['tour']=str(request.session['TOUR'])   
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context["orientation"]=request.POST['orientation']
                request.session['orientation']=request.POST['orientation']
                if request.POST['orientation']=="paysage":
                    return render(request, "tipointticroixpaysage.html", context)
                else:
                    return render(request, "tipointticroixportrait.html", context)
        context['marquevous']=marquejoueur
        context['marqueordi']=marqueordi
        request.session['TOUR']=request.session['TOUR']+1 
        context['tour']=str(request.session['TOUR'])   
        context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
        context["orientation"]=request.POST['orientation']
        request.session['orientation']=request.POST['orientation']
        if request.POST['orientation']=="paysage":
            request.session['orientation']="paysage"
            return render(request, "tipointticroixpaysage.html", context)
        else:
            request.session['orientation']="portrait"
            return render(request, "tipointticroixportrait.html", context)
    #Appel initial
    request.session['TOUR']=0
    request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
    request.session['SEQUENCE']=[]
    
    if request.session['orientation']=="paysage":
        return render(request, "tipointticroixpaysage.html", context)
    else:
        return render(request, "tipointticroixportrait.html", context)

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
            return render(request, "machines.html", context)
        if request.POST["charger"]=="Oui":
            print("charger : " + request.POST["charger"])
            request.session['SEQUENCE']=request.POST['sequence'].split(",")
            marque="O"
            request.session['GRILLE']=[["-"] * 25 for _ in range(25)]
            for coup in request.session['SEQUENCE']:
                request.session['GRILLE']=majgrille(coup,marque,request.session['GRILLE'])
                if marque=="O":
                    marque="X"
                else:
                    marque="O"
            context['victoire1']="Non"
            context['victoire2']="Non"
            context['nom1']=nomniveau(request.session['NIVEAU1'])
            context['nom2']=nomniveau(request.session['NIVEAU2'])    
            context['niveau1']=request.session['NIVEAU1']
            context['niveau2']=request.session['NIVEAU2']
            context['modejeu']=request.session['MODEJEU']
            context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
            request.session['TOUR']=len(request.session['SEQUENCE'])//2+1
            print(request.session['TOUR'])
            context['tour']=str(request.session['TOUR'])   
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
        context['pat']="Non"
        context['modejeu']=request.session['MODEJEU']
        if nbcoup%2==0:
            coup=coupmachine("O",request.session['NIVEAU1'],
                             request.session['SEQUENCE'],request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coup]
            request.session['GRILLE']=majgrille(coup,"O",request.session['GRILLE'])
            res = trouve_5(coup,"O",request.session['GRILLE'])
            context['nom1']=nomniveau(request.session['NIVEAU1'])
            context['nom2']=nomniveau(request.session['NIVEAU2'])
            context['niveau1']=request.session['NIVEAU1']
            context['niveau2']=request.session['NIVEAU2']
            if res != "Non":
                nbO=0
                nbX=0
                for j in range(0,25):
                    for i in range(0,25):
                        if request.session['GRILLE'][i][j]=="O":
                            nbO=nbO+1
                        if request.session['GRILLE'][i][j]=="X":
                            nbX=nbX+1
                context['nom1']=nomniveau(request.session['NIVEAU1'])
                context['nom2']=nomniveau(request.session['NIVEAU2'])
                context['niveau1']=request.session['NIVEAU1']
                context['niveau2']=request.session['NIVEAU2']
                context['victoire1']=res
                context['victoire2']="Non"
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                return render(request, "machines.html", context)
            if len(request.session['SEQUENCE'])==625:
                context['pat']="Oui"
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                return render(request,"machines.html", context)
        else:
            coup=coupmachine("X",request.session['NIVEAU2'],request.session['SEQUENCE'],
                             request.session['GRILLE'])
            request.session['SEQUENCE']=request.session['SEQUENCE']+[coup]
            request.session['GRILLE']=majgrille(coup,"X",request.session['GRILLE'])
            res = trouve_5(coup,"X",request.session['GRILLE'])
            context['nom1']=nomniveau(request.session['NIVEAU1'])
            context['nom2']=nomniveau(request.session['NIVEAU2'])
            context['niveau1']=request.session['NIVEAU1']
            context['niveau2']=request.session['NIVEAU2']
            if res != "Non":
                nbO=0
                nbX=0
                for j in range(0,25):
                    for i in range(0,25):
                        if request.session['GRILLE'][i][j]=="O":
                            nbO=nbO+1
                        if request.session['GRILLE'][i][j]=="X":
                            nbX=nbX+1
                context['nom1']=nomniveau(request.session['NIVEAU1'])
                context['nom2']=nomniveau(request.session['NIVEAU2'])
                context['niveau1']=request.session['NIVEAU1']
                context['niveau2']=request.session['NIVEAU2']
                context['victoire2']=res
                context['victoire1']="Non"
                context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
                context['tour']=str(request.session['TOUR'])
                return render(request, "machines.html", context)
        request.session['TOUR']=len(request.session['SEQUENCE'])//2+1
        context['sequence']=','.join([str(i) for i in request.session['SEQUENCE']])
        context['tour']=str(request.session['TOUR'])
        context['victoire1']="Non"
        context['victoire2']="Non"
        context['nom1']=nomniveau(request.session['NIVEAU1'])
        context['nom2']=nomniveau(request.session['NIVEAU2'])    
        context['niveau1']=request.session['NIVEAU1']
        context['niveau2']=request.session['NIVEAU2']
        print(request.session['TOUR'])    
        return render(request, "machines.html", context) 
    request.session['TOUR']=0
    request.session['GRILLE'] = [["-"] * 25 for _ in range(25)]
    request.session['SEQUENCE']=[] 
    return render(request, "machines.html", context) 

def statistics(request):
    context = {}
    connec=estconnecté(request)
    if connec[0]:
        context["connexion"]="Oui"
        context["connec"]=connec[1]
        userx=User.objects.get(pseudo=connec[1])
        results = Game.objects.filter(user_id=userx.id).values('type').annotate(
            total=Count('id'),
            victories=Sum(Case(When(victoire=True, then=1), default=0, output_field=IntegerField())),
            victoire_percentage=Cast(Sum(Case(When(victoire=True, then=1), default=0, output_field=IntegerField())) * 100.0 / Count('id'), FloatField())
        ).order_by('type')

        context['results'] = results
        return render(request, 'statistics.html', context)
    else:
        context["connexion"]="Non"
        return redirect('/connect',context)

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