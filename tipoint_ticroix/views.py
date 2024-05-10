from django.shortcuts import render
from django.conf import settings
from .functions import coupordi, majgrille, trouve_5

#from functions import coupordi
import json
# Create your views here.

#Teste si l'ordinateur à gagner
#si oui renvoie la sequences des 5 positions allignées
#sinon renvoie ""


#page accueil
def accueil(request):
    return render(request, "accueil.html")

#page tipointticroix
def tipointticroix(request):
    context = {}
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
            grid[ix][iy]=""
            ix=int(avantdercoup.split("/")[1])
            iy=int(avantdercoup.split("/")[0])
            grid[ix][iy]=""

            context['victoire']="Non"
            context['defaite']="Non"
            print(context)
            return render(request, "tipointticroix.html", context)
            
        #MAJ TABLEAU
        if settings.TOUR==0 :
            if request.POST["check-begin"]=="Non" :
                #le joueur ne commence pas - 1er COUP ORDINATEUR
                #settings.GRILLE[12][12]="X"
                majgrille("12/12","X")
                print("ordi : " + "12/12")
                settings.SEQUENCE=settings.SEQUENCE+["12/12"]
                context['begin']="Non"
                settings.BEGIN="Non"
            else:
                context['begin']="Oui"
                settings.BEGIN="Oui"
            
            context['tour']=str(settings.TOUR)
            context['victoire']="Non"
            context['defaite']="Non"
        else :
            context['begin']=settings.BEGIN
            context['victoire']="Non"
            context['defaite']="Non"
            #COUP JOUEUR
            settings.SEQUENCE=settings.SEQUENCE+[request.POST["coupjoueur"]]
            #settings.GRILLE=COUPDUJOUEUR
            majgrille(request.POST["coupjoueur"],"O")
            #victoire joueur
            res = trouve_5(request.POST["coupjoueur"],"O")
            if res != "Non":
                context['victoire']=res
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                print(context) 
                return render(request, "tipointticroix.html", context)

            #COUP ORDINATEUR
            coupordinateur=coupordi(settings.TOUR)
            print("ordi : " + coupordinateur)
            settings.SEQUENCE=settings.SEQUENCE+[coupordinateur]
            #settings.GRILLE=COUPORDINATEUR
            majgrille(coupordinateur,"X")
            res = trouve_5(coupordinateur,"X")
            if res != "Non":
                context['defaite']=res
                context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
                context['tour']=str(settings.TOUR)
                print(context) 
                return render(request, "tipointticroix.html", context)
        settings.TOUR=settings.TOUR+1 
        context['tour']=str(settings.TOUR)   
        context['sequence']=','.join([str(i) for i in settings.SEQUENCE])
        #print(settings.GRILLE)
        print(context) 
        return render(request, "tipointticroix.html", context)
    #Appel initial
    settings.TOUR=0
    settings.GRILLE = [[""] * 25 for _ in range(25)]
    settings.SEQUENCE=[]
    return render(request, "tipointticroix.html", context)