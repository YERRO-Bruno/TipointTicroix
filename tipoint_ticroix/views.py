from django.shortcuts import render
from django.conf import settings
from .functions import coupordi, coupmachine, majgrille, trouve_5

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