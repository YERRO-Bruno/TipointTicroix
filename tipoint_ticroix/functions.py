from django.conf import settings
from .models import User
import random
from django.contrib.auth import authenticate
import socket, sys

#FONCTIONS
#nom en fonction du niveau
def nomniveau(niv):
    if niv==1:
        return("Novice")
    if niv==2:
        return("Amateur")
    if niv==3:
        return("Pro")
    if niv==4:
        return("expert")

#coup ordinateur
def coupordi(marque):
    if settings.NIVEAU==1:
        return(coupordi1(marque))
    if settings.NIVEAU==2:
        return(coupordi2(marque))
    if settings.NIVEAU==3:
        return(coupordi3(marque))
    if settings.NIVEAU==4:
        return(coupordi4(marque))

def coupmachine(marque,niveau):
    if niveau==1:
        return(coupordi1(marque))
    if niveau==2:
        return(coupordi2(marque))
    if niveau==3:
        return(coupordi3(marque))
    if niveau==4:
        return(coupordi4(marque))

#coup ordi niveau0 (afin de test)
def coupordi0(marque):
    coup=str(settings.TOUR)+"/12"
    return(coup)

#coup ordinateur niveau1
def coupordi1(marque):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées()
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(settings.SEQUENCE)==0:
        coup="12/12"
        print("coup ordi1-0:",coup, marque)
        return(coup)

#1er coup ordinateur quand il joue en 2eme
    imin=max(int(settings.SEQUENCE[0].split("/")[1])-1,0)
    imax=min(int(settings.SEQUENCE[0].split("/")[1])+1,24)
    jmin=max(int(settings.SEQUENCE[0].split("/")[0])-1,0)
    jmax=min(int(settings.SEQUENCE[0].split("/")[0])+1,24)
    if len(settings.SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi1-1:",coup, marque)
            return(coup)
        
    #recherche du coup entrainant la victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    print("coup ordi1-2:",res[0], marque)
                    return(res[0])
    
    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    print("coup ordi1-3:",res[0], marque)
                    return(res[0])
    
    #recherche du coup entrainant -ùùùù-
    seq=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                    nb=nb+1
            if nb>nbmax:
                nbmax=nb
                coupmax=coup
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi1-4:",coup, seq, marque)
        return(coup)
        
    #Recherche des coups adjacents au dernier coup du joueur. Un des coups est choisi aléatoirement
    #si pas de coup trouvé on passe au coup du joueur précédent
    SEQO=[]
    if marque=="O":
        for i in range(0,len(settings.SEQUENCE)):
            if i%2==1:
                SEQO=SEQO+[settings.SEQUENCE[i]]
    else:
        for i in range(0,len(settings.SEQUENCE)):
            if i%2==0:
                SEQO=SEQO+[settings.SEQUENCE[i]]   
    
    for i in range(len(SEQO)-1,-1,-1):
        i0=int(SEQO[i].split("/")[1])
        j0=int(SEQO[i].split("/")[0])
        imin=max(i0-1,0)
        imax=min(i0+1,24)
        jmin=max(j0-1,0)
        jmax=min(j0+1,24)
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi1-5:",coup, seq, marque)
            return(coup)
    
    #Recherche des coups possibles dans la zone jouable. c'est à dire le carré formé horizontalemet 
    #entre la plus ptite abcisse jouée +1 et la plus grande abcisse jouée +1  et verticalement entre
    #la plus petite ordonnée jouée +1 et la plus grande ordonnée jouée +1. Cette zone est contenue 
    #en abcisse et ordonée entre 0 et 24.
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                print("coup ordi1-6:",coup, marque)
                return(coup)
    
#coup ordinateur niveau2
def coupordi2(marque):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées()
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(settings.SEQUENCE)==0:
        coup="12/12"
        print("coup ordi2-0:",coup, marque)
        return(coup)

    imin=max(int(settings.SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(settings.SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(settings.SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(settings.SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(settings.SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi2-1:",coup)
            return(coup)

    #recherche du coup entrainant la victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    print("coup ordi2-2:",coup)
                    return(coup)

    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seq=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-3 :",coup, seq)
        return(coup)
    
    ##recherche du coup entrainant -ùùùù-
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-4 :",coup, seq)
        return(coup)
    
    #recherche des coup de  l'adversaire entrainant -ùùùù-
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    seq=seq+res
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-5 :",coup, seq)
        return(coup)
    
    ##recherche des coup  entrainant -ùùùù$ ou $uuuu- ou -ùùù-
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-6 :",coup, seq)
        return(coup)
    
    ##recherche du coup du joueur entrainant -ùùù-
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-7:",coup, seq)
        return(coup)
        
    ##recherche du coup du joueur entrainant -ùù-
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-8:",coup, seq)
        return(coup)
    
    ##recherche du coup du joueur entrainant -ùù ou -ùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù".replace("ù",marque),2)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"ùù-".replace("ù",marque),2)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
    if seq!=[]:
        random.shuffle(seq)
        coup=seq[0]
        print("coup ordi2-9:",coup, seq)
        return(coup)

    #Recherche des coups adjacents au dernier coup de l'adversaire. Un des coups est choisi aléatoirement
    #si pas de coup trouvé on passe au coup du joueur précédent
    SEQO=[]
    if marque=="X":
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i]]
    else:
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i+1]]  
    for i in range(len(SEQO)-1,-1,-1):
        i0=int(SEQO[i].split("/")[1])
        j0=int(SEQO[i].split("/")[0])
        imin=max(i0-1,0)
        imax=min(i0+1,24)
        jmin=max(j0-1,0)
        jmax=min(j0+1,24)
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi2-10:",coup, seq)
            return(coup)

#coup ordinateur niveau3
def coupordi3(marque):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées()
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(settings.SEQUENCE)==0:
        coup="12/12"
        print("coup ordi3-0:",coup, marque)
        return(coup)

    imin=max(int(settings.SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(settings.SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(settings.SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(settings.SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(settings.SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi3-1:",coup)
            return(coup)

    #recherche du coup entrainant la victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    print("coup ordi3-2:",coup)
                    return(coup)

    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                    if nb==nbmax:
                        seqmax=seqmax+[coup]
                    if nb>nbmax:
                        seqmax=[coup]
                        nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-3 :",coup, seqmax)
        return(coup)
    
    ##recherche du coup entrainant -ùùùù- et ù-ùùù-u et ùùù-ù-ùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ù-ùùù-ù".replace("ù",marque),6)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùù-ù-ùùù".replace("ù",marque),6)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-4 :",coup, seqmax)
        return(coup)
    
    #recherche des coup de  l'adversaire entrainant -ùùùù- et ù-ùùù-u et ùùù-ù-ùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"ù-ùùù-ù".replace("ù",marque1),6)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù-ùùù".replace("ù",marque1),6)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-5 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ùùù- ou -ùùùù ou ùùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-6 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ù-ùù- ou -ùù-ù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ù-ùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùù-ù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seq)
        coup=seqmax[0]
        print("coup ordi3-6bis :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ùùùù ou ùùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seq)
        coup=seqmax[0]
        print("coup ordi3-7 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant ùùù-u ou ù-ùùù ou -ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùù-u".replace("ù",marque),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-8 :",coup, seqmax)
        return(coup)
    
    ##recherche du coup de l'adversaire entrainant -ùùùù ou uuuu- ou ù-ùùù ou ùùù-ù -ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùù-".replace("ù",marque1),3)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"-ùùùù".replace("ù",marque1),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùùù-".replace("ù",marque1),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ù-ùùù".replace("ù",marque1),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù".replace("ù",marque1),4)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-9:",coup, seqmax)
        return(coup)
        
    ##recherche du coup du joueur entrainant -ùù- -ùùù& &ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùùù&".replace("ù",marque).replace("&",marque1),2)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"&ùùù-".replace("ù",marque).replace("&",marque1),2)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-10:",coup, seqmax)
        return(coup)
    
    ##recherche du coup de l'adversaire entrainant -ùù- -ùùù& &ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùù-".replace("ù",marque1),2)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
            if nb>0:
                if nb==nbmax:
                    seqmax=seqmax+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi3-11:",coup, seqmax)
        return(coup)

    #Recherche des coups adjacents au dernier coup de l'adversaire.
    #Un des coups est choisi aléatoirement. Si pas de coup trouvé on passe au coup précédent.
    SEQO=[]
    if marque=="X":
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i]]
    else:
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i+1]]  
    for i in range(len(SEQO)-1,-1,-1):
        i0=int(SEQO[i].split("/")[1])
        j0=int(SEQO[i].split("/")[0])
        imin=max(i0-1,0)
        imax=min(i0+1,24)
        jmin=max(j0-1,0)
        jmax=min(j0+1,24)
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi3-12:",coup, seq)
            return(coup)

#coup ordinateur niveau4
def coupordi4(marque):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées()
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]
#1er coup ordinateur quand il joue en 1er
    if len(settings.SEQUENCE)==0:
        coup="12/12"
        print("coup ordi4-0:",coup, marque)
        return(coup)

    imin=max(int(settings.SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(settings.SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(settings.SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(settings.SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(settings.SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi4-1:",coup)
            return(coup)

    #recherche du coup entrainant la victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5)
                res=result[0]
                if res!= "Non":
                    print("coup ordi4-2:",coup)
                    return(coup)

    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                    if nb==nbmax:
                        seqmax=seqmax+[coup]
                    if nb>nbmax:
                        seqmax=[coup]
                        nbmax=nb
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi4-3 :",coup, seqmax)
        return(coup)
    
    #recherche du meilleur coup avec la fonction score(i,j,marque)
    scormax=0
    seqmax=[]
    grid=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if settings.GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                scor=score(coup,marque)
                if scor>0:
                    if scor==scormax:
                        coup=str(j)+"/"+str(i)
                        seqmax=seqmax+[coup]
                        scormax=scor
                    if scor>scormax:
                        coup=str(j)+"/"+str(i)
                        seqmax=[coup]
                        scormax=scor
    if seqmax!=[]:
        random.shuffle(seqmax)
        coup=seqmax[0]
        print("coup ordi4-3 :",coup, scormax, seqmax)
        return(coup)
    
    #Recherche des coups adjacents au dernier coup de l'adversaire.
    #Un des coups est choisi aléatoirement. Si pas de coup trouvé on passe au coup précédent.
    SEQO=[]
    if marque=="X":
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i]]
    else:
        for i in range(0,len(settings.SEQUENCE),2):
            SEQO=SEQO+[settings.SEQUENCE[i+1]]  
    for i in range(len(SEQO)-1,-1,-1):
        i0=int(SEQO[i].split("/")[1])
        j0=int(SEQO[i].split("/")[0])
        imin=max(i0-1,0)
        imax=min(i0+1,24)
        jmin=max(j0-1,0)
        jmax=min(j0+1,24)
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if settings.GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi4-4:",coup, seq)
            return(coup)

def score(coup,marque):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    nb=0
    #joueur :-ùùùù- ù-ùùù-ù ùùù-ù-ùùù
    result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ù-ùùù-ù".replace("ù",marque),6)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ùùù-ù-ùùù".replace("ù",marque),6)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb1=nb
    #adversaire :-ùùùù- ù-ùùù-ù ùùù-ù-ùùù
    nb=0
    result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ù-ùùù-ù".replace("ù",marque1),6)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ùùù-ù-ùùù".replace("ù",marque1),6)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb1d=nb
    #joueur -ùùù- ùùùù- ùùùù- 
    nb=0
    result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"-ùùùù&".replace("ù",marque).replace("&",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"&ùùùù-".replace("ù",marque).replace("&",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2=nb
    if nb2>=2:
        print("nb2",nb2,coup)
    
    #joueur ù-ùùù ùùù-ù -ù-ùù- -ùù-ù-
    nb=0
    result=cherche_size(coup,marque,"-ù-ùù-".replace("ù",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"-ùu-ù-".replace("ù",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ùùù-u".replace("ù",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2bis=nb
    if nb2bis>=3:
        print("nb2bis",nb2bis,coup)
    
    #adversairejoueur -ùùù- ùùùù- ùùùù- 
    nb=0
    result=cherche_size(coup,marque1,"-ùùù-".replace("ù",marque1),3)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque1,"&ùùùù-".replace("ù",marque1).replace("&",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"-ùùùù&".replace("ù",marque1).replace("&",marque),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2d=nb
    if nb2d>=3:
        print("nb2d",nb2d,coup)
    
    #adversairejoueur ù-ùùù ùùù-ù -ù-ùù- -ùù-ù-
    nb=0
    result=cherche_size(coup,marque1,"-ù-ùù-".replace("ù",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"-ùu-ù-".replace("ù",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ù-ùùù".replace("ù",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ùùù-u".replace("ù",marque1),4)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2dbis=nb
    if nb2dbis>=2:
        print("nb2dbis",nb2dbis,coup)

    #joueur -ùù- &ùùù- -ùùù&
    nb=0
    result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque,"-ùùù&".replace("ù",marque).replace("&",marque1),2)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"&ùùù-".replace("ù",marque).replace("&",marque1),2)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb3=nb
    #adversaire -ùù- &ùùù- -ùùù&
    nb=0
    result=cherche_size(coup,marque1,"-ùù-".replace("ù",marque1),2)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque1,"-ùùù&".replace("ù",marque1).replace("&",marque),2)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"&ùùù-".replace("ù",marque1).replace("&",marque),2)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb3d=nb

    #calcul score
    score=0
    if nb1>0:
        return(120)
    if nb1d>0:
        return(100)
    if nb2+nb2bis>1:
        return(20+nb2*20+nb2bis*18+nb3+nb3d)
    if nb2d+nb2dbis>1:
        return(15+nb2d*20+nb2dbis*18+nb3+nb3d)
    if nb2+nb2bis>0 and nb2d+nb2dbis>0:
        return(15+nb2*20+nb2bis*18+nb2d*19+nb2dbis*17+nb3+nb3d)
    score=nb2*20+nb2bis*18+nb2d*19+nb2dbis*17+nb3+nb3d
    return(score)

#MAJ GRILLE avec le coup joué
def majgrille(coup,marque):
    y=int(coup.split("/")[0])
    i=int(coup.split("/")[1])
    settings.GRILLE[i][y]=marque

def trouve_5(coup,marque):
    marque5=marque*5
    grid=settings.GRILLE
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    imin=max(i0-4,0)
    imax=min(i0+4,24)
    jmin=max(j0-4,0)
    jmax=min(j0+4,24)
    
    #ligne horizontale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=winH(i0,imin,imax,j0,jmin,jmax,grid,marque5)
    if ret !="Non":
        return(ret)
    
#   ligne verticale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=winV(i0,imin,imax,j0,jmin,jmax,grid,marque5)
    if ret !="Non":
        return(ret)
    
#ligne oblique / (slach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=winS(i0,j0,grid,marque5)
    if ret !="Non":
        return(ret)
   
#ligne oblique \ (antislach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=winA(i0,j0,grid,marque5)
    if ret !="Non":
        return(ret)
    
    #les recherches sont négatives
    return("Non")

def cherche_size(coup,marque,rech,size):
    grid=[["-"] * 25 for _ in range(25)]
    for i in range(0,24):
        for j in range(0,24):
            grid[i][j]=settings.GRILLE[i][j]
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    grid[i0][j0]=marque
    imin=max(i0-size,0)
    imax=min(i0+size,24)
    jmin=max(j0-size,0)
    jmax=min(j0+size,24)
    seq=[]
    nb=0
    #ligne horizontale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=rechercheH(i0,imin,imax,j0,jmin,jmax,grid,rech)
    if ret !="Non":
        nb=nb+1
        seq=seq+[ret]
    
#   ligne verticale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=rechercheV(i0,imin,imax,j0,jmin,jmax,grid,rech)
    if ret !="Non":
        nb=nb+1
        seq=seq+[ret]
    
#ligne oblique / (slach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=rechercheS(i0,j0,grid,4,rech)
    if ret !="Non":
        nb=nb+1
        seq=seq+[ret]
   
#ligne oblique \ (antislach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    ret=rechercheA(i0,j0,grid,4,rech)
    if ret !="Non":
        nb=nb+1
        seq=seq+[ret]
    if seq==[]:
        return(["Non"])
    else:
        return(seq,nb)

#recherche d'un motif, horizontalement sur un segment comprenant un point d'abcisse i0 et 
#d'ordonnée j0 en son millieu. Ne sont pas pris en compte les points en dehors de la grille (25x25).
# imin, imax, jmin, jmax : abcisse minimale, maximale, ordonnée minimale et maximale du segment.
# grid : grille des coups joués. rech : motif recherché.
def winH(i0,imin,imax,j0,jmin,jmax,grid,rech):
    ligne=""
    for i in range(imin,imax+1):
        ligne=ligne + grid[i][j0]
    ret=ligne.find(rech)
    if ret != -1:
        iwin0 = imin + ret
        sequencewin=[]
        for i in range(iwin0,iwin0+5):
            idx=str(j0)+"/"+str(i)
            sequencewin = sequencewin + [idx]
        win=','.join([str(i) for i in sequencewin])
        return(win)
    return("Non")

def rechercheH(i0,imin,imax,j0,jmin,jmax,grid,rech):
    ligne=""
    for i in range(imin,imax+1):
        ligne=ligne + grid[i][j0]
    ret=ligne.find(rech)
    if ret != -1:
        return(str(j0)+"/"+str(i0))
    return("Non")

#recherche d'un motif, verticalement sur un segment comprenant un point d'abcisse i0 et 
#d'ordonnée j0 en son millieu. Ne sont pas pris en compte les points en dehors de la grille (25x25).
# imin, imax, jmin, jmax : abcisse minimale, maximale, ordonnée minimale et maximale du segment.
# grid : grille des coups joués. rech : motif recherché.
def winV(i0,imin,imax,j0,jmin,jmax,grid,rech):
    ligne=""
    for j in range(jmin,jmax+1):
        ligne=ligne + grid[i0][j]
    ret=ligne.find(rech)
    if ret != -1:
        jwin0 = jmin + ret
        sequencewin=[]
        for j in range(jwin0,jwin0+5):
            idx=str(j)+"/"+str(i0)
            sequencewin = sequencewin + [idx]
        win=','.join([str(i) for i in sequencewin])
        return(win)
    return("Non")

def rechercheV(i0,imin,imax,j0,jmin,jmax,grid,rech):
    ligne=""
    for j in range(jmin,jmax+1):
        ligne=ligne + grid[i0][j]
    ret=ligne.find(rech)
    if ret != -1:
        return(str(j0)+"/"+str(i0))
    return("Non")

#recherche d'un motif, oblique / sur un segment comprenant un point d'abcisse i0 et 
#d'ordonnée j0 en son millieu. Ne sont pas pris en compte les points en dehors de la grille (25x25).
# imin, imax, jmin, jmax : abcisse minimale, maximale, ordonnée minimale et maximale du segment.
# grid : grille des coups joués. rech : motif recherché.
def winS(i0,j0,grid,rech):
    ligne=""
    deb=False
    for k in range(0,10):
        if i0-4+k>-1 and i0-4+k<25 and j0+4-k>-1 and j0+4-k<25 :
            ligne=ligne + grid[i0-4+k][j0+4-k]
            if deb==False:
                ideb=i0-4+k
                jdeb=j0+4-k
                deb=True
    ret=ligne.find(rech)
    if ret != -1:
        sequencewin=[]
        for k in range(0,5):
                idx=str(jdeb-k-ret)+"/"+str(ideb+k+ret)
                sequencewin = sequencewin + [idx]
        win=','.join([str(i) for i in sequencewin])
        return(win)
    return("Non")

def rechercheS(i0,j0,grid,nbcar,rech):
    ligne=""
    for k in range(0,10):
        if i0-nbcar+k>-1 and i0-nbcar+k<25 and j0+nbcar-k>-1 and j0+nbcar-k<25 :
            ligne=ligne + grid[i0-nbcar+k][j0+nbcar-k]
    ret=ligne.find(rech)
    if ret != -1:
        return(str(j0)+"/"+str(i0))
    return("Non")

#recherche d'un motif, oblique \ sur un segment comprenant un point d'abcisse i0 et 
#d'ordonnée j0 en son millieu. Ne sont pas pris en compte les points en dehors de la grille (25x25).
# imin, imax, jmin, jmax : abcisse minimale, maximale, ordonnée minimale et maximale du segment.
# grid : grille des coups joués. rech : motif recherché.
def winA(i0,j0,grid,rech):
    ligne=""
    deb=False
    for k in range(0,10):
        if i0-4+k>-1 and i0-4+k<25 and j0-4+k>-1 and j0-4+k<25 :
            ligne=ligne + grid[i0-4+k][j0-4+k]
            if deb==False:
                ideb=i0-4+k
                jdeb=j0-4+k
                deb=True
    ret=ligne.find(rech)
    if ret != -1:
        sequencewin=[]
        for k in range(0,5):
            idx=str(jdeb+k+ret)+"/"+str(ideb+k+ret)
            sequencewin = sequencewin + [idx]
        win=','.join([str(i) for i in sequencewin])
        return(win)
    return("Non")    

def rechercheA(i0,j0,grid,nbcar,rech):
    ligne=""
    for k in range(0,10):
        if i0-nbcar+k>-1 and i0-nbcar+k<25 and j0-nbcar+k>-1 and j0-nbcar+k<25 :
            ligne=ligne + grid[i0-nbcar+k][j0-nbcar+k]
    ret=ligne.find(rech)
    if ret != -1:
        return(str(j0)+"/"+str(i0))
    return("Non")    

#calcul les abcisses et les ordonnées minimum et maximum jouées soit la zone jouable.
def calculbornesjouées():
    seq=settings.SEQUENCE
    ibornemin=24
    ibornemax=0
    jbornemin=24
    jbornemax=0
    for i in range(0,len(seq)):
        if int(seq[i].split("/")[1])<ibornemin:
            ibornemin=int(seq[i].split("/")[1])
        if int(seq[i].split("/")[1])>ibornemax:
            ibornemax=int(seq[i].split("/")[1])
        if int(seq[i].split("/")[0])<jbornemin:
            jbornemin=int(seq[i].split("/")[0])
        if int(seq[i].split("/")[0])>jbornemax:
            jbornemax=int(seq[i].split("/")[0])
    ibornemin=max(0,ibornemin-2)
    ibornemax=min(24,ibornemax+2)
    jbornemin=max(0,jbornemin-2)
    jbornemax=min(24,jbornemax+2)
    print("bornes : ",ibornemin,ibornemax,jbornemin,jbornemax)
    return([ibornemin,ibornemax,jbornemin,jbornemax])

#Actions si le joueur est connecté ou pas
def estconnecté(req):
    emailx=req.session.get('email')
    passwordx=req.session.get('password')
    userConnected = authenticate(email=emailx, password=passwordx)
    if userConnected is not None:
        userx=User.objects.get(email=emailx)
        pseudox=userx.pseudo
        return(True,pseudox)
    else:
        return(False,"")

#version asynchrone de estconnecté()
from asgiref.sync import sync_to_async

async def estconnecté_async(req):
    emailx = await sync_to_async(req.session.get)('email')
    passwordx = await sync_to_async(req.session.get)('password')
    userConnected = await sync_to_async(authenticate)(email=emailx, password=passwordx)
    if userConnected is not None:
        userx = await sync_to_async(User.objects.get)(email=emailx)
        pseudox = userx.pseudo
        return (True, pseudox)
    else:
        return (False, "")

def serveursocket (host):
    # Définition d'un serveur réseau rudimentaire
# Ce serveur attend la connexion d'un client, pour entamer un dialogue avec lui

    PORT = 50000
    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) liaison du socket à une adresse précise :
    try:
        mySocket.bind((host, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()

    while 1:
        # 3) Attente de la requête de connexion d'un client :
        print("Serveur prêt, en attente de requêtes ...")
        mySocket.listen(5)

        # 4) Etablissement de la connexion :
        connexion, adresse = mySocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

        # 5) Dialogue avec le client :
        connexion.send("Vous êtes connecté au serveur Marcel. Envoyez vos messages.")
        msgClient = connexion.recv(1024)
        while 1:
            print("C>", msgClient)
            if msgClient.upper() == "FIN" or msgClient =="":
                break
            msgServeur = input("S> ")
            connexion.send(msgServeur)
            msgClient = connexion.recv(1024)

        # 6) Fermeture de la connexion :
        connexion.send("Au revoir !")
        print("Connexion interrompue.")
        connexion.close()

        ch = input("<R>ecommencer <T>erminer ? ")
        if ch.upper() =='T':
            break

def connecserveur (host,pseudo):
    # Définition d'un serveur réseau rudimentaire
# Ce serveur attend la connexion d'un client, pour entamer un dialogue avec lui

    import asyncio
    from websockets.server import serve
    port = 8765
    msg=""
    webs=""
    async def echo(websocket):
        async for message in websocket:
            print("received from {}:{} : ".format(websocket.remote_address[0],websocket.remote_address[1]) + message)
            await websocket.send(pseudo)
            msg=message
            webs=websocket
    async def main():
        print("Server is activated on ws://{}:{}".format(host,port))
        #async with serve(echo, "localhost", 8765):
        async with serve(echo, host, port):
                await asyncio.Future()  # run forever
    asyncio.run(main())
    return(msg)

def connecserveur1 (host,pseudo):
    # Définition d'un serveur réseau rudimentaire
# Ce serveur attend la connexion d'un client, pour entamer un dialogue avec lui

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    print("ip",ipaddress)
    PORT = 8765
    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) liaison du socket à une adresse précise :
    try:
        mySocket.bind((host, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.", socket.error)
        sys.exit()

    while 1:
        # 3) Attente de la requête de connexion d'un client :
        print("Serveur prêt, en attente de requêtes ...")
        mySocket.listen()

        # 4) Etablissement de la connexion :
        connexion, adresse = mySocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

        connexion.send(pseudo.encode('utf-8'))
        msgClient = connexion.recv(1024)
        return(msgClient.decode('utf-8'),connexion)

def clientsocket(host):
    # Définition d'un client réseau rudimentaire
    # Ce client dialogue avec un serveur ad hoc
    PORT = 50000

    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) envoi d'une requête de connexion au serveur :
    try:
        mySocket.connect((host, PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")

    # 3) Dialogue avec le serveur :
    msgServeur = mySocket.recv(1024)

    while 1:
        if msgServeur.upper() == "FIN" or msgServeur =="":
            break
        print("S>", msgServeur)
        msgClient = input("C> ")
        mySocket.send(msgClient)
        msgServeur = mySocket.recv(1024)

    # 4) Fermeture de la connexion :
    print("Connexion interrompue.")
    mySocket.close()

async def connecclienty(host,pseudo):
    # Définition d'un client réseau rudimentaire
    # Ce client dialogue avec un serveur ad hoc
    
    import asyncio
    import websockets
    from websockets.sync.client import connect
    #with connect("ws://"+host+":8765") as websocket:
    async with connect("ws://77.37.125.25:8765",pseudo) as websocket:
        await websocket.send(pseudo)
        message = await websocket.recv
        
        print(f"Received from server : {message}")
        return(websocket,message)

async def connecclient(host, pseudo):
    import websockets
    import json

    async with websockets.connect(f"wss://77.37.125.25:8765/ws/chat/") as websocket:
        print("connect")
        await websocket.send(json.dumps({"message": pseudo}))
        message= await websocket.recv()
        print("recu de server : ",message)
        return websocket, message
    
def connecclientX(host,pseudo):
    # Définition d'un client réseau rudimentaire
    # Ce client dialogue avec un serveur ad hoc
    
    import asyncio
    import websockets
    from websockets.sync.client import connect
    #with connect("ws://"+host+":8765") as websocket:
    with connect("ws://77.37.125.25:8765") as websocket:
        #while True:
        #message = websocket.recv()
        #print(message)
        websocket.send(pseudo)
        websocket.close
        #print(f"Received from server : {message}")
        return(websocket,"testok")
    
    
def connecclient1(host,pseudo):
    # Définition d'un client réseau rudimentaire
    # Ce client dialogue avec un serveur ad hoc
    PORT = 50000

    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) envoi d'une requête de connexion au serveur :
    try:
        mySocket.connect((host, 8765))
    except socket.error:
        print("La connexion a échoué.", socket.error)
        sys.exit()
    print("Connexion établie avec le serveur.")
    msgServeur = mySocket.recv(1024)
    mySocket.send(pseudo.encode('utf-8'))
    return(msgServeur.decode('utf-8'),mySocket)

def nbtour():
    res=len(settings.SEQUENCE)
    return((res//2)+1)

















