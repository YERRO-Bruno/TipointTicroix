from .models import User
import random
from django.contrib.auth import authenticate


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
    if niv==5:
        return("chamion")

#coup ordinateur
def coupordi(marque,NIVEAU,SEQUENCE,GRILLE):
    if NIVEAU==1:
        return(coupordi1(marque,SEQUENCE,GRILLE))
    if NIVEAU==2:
        return(coupordi2(marque,SEQUENCE,GRILLE))
    if NIVEAU==3:
        return(coupordi3(marque,SEQUENCE,GRILLE))
    if NIVEAU==4:
        return(coupordi4(marque,SEQUENCE,GRILLE))
    if NIVEAU==5:
        return(coupordi5(marque,SEQUENCE,GRILLE))

def coupmachine(marque,niveau,SEQUENCE,GRILLE):
    if niveau==1:
        return(coupordi1(marque,SEQUENCE,GRILLE))
    if niveau==2:
        return(coupordi2(marque,SEQUENCE,GRILLE))
    if niveau==3:
        return(coupordi3(marque,SEQUENCE,GRILLE))
    if niveau==4:
        return(coupordi4(marque,SEQUENCE,GRILLE))
    if niveau==5:
        return(coupordi5(marque,SEQUENCE,GRILLE))


#coup ordinateur niveau1
def coupordi1(marque,SEQUENCE,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées(SEQUENCE)
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(SEQUENCE)==0:
        coup="12/12"
        print("coup ordi1-0:",coup, marque)
        return(coup)

#1er coup ordinateur quand il joue en 2eme
    imin=max(int(SEQUENCE[0].split("/")[1])-1,0)
    imax=min(int(SEQUENCE[0].split("/")[1])+1,24)
    jmin=max(int(SEQUENCE[0].split("/")[0])-1,0)
    jmax=min(int(SEQUENCE[0].split("/")[0])+1,24)
    if len(SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if GRILLE[i][j]=="-":
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    print("coup ordi1-2:",res[0], marque)
                    return(res[0])
    
    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5,GRILLE)
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
        for i in range(0,len(SEQUENCE)):
            if i%2==1:
                SEQO=SEQO+[SEQUENCE[i]]
    else:
        for i in range(0,len(SEQUENCE)):
            if i%2==0:
                SEQO=SEQO+[SEQUENCE[i]]   
    
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
                if GRILLE[i][j]=="-":
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                print("coup ordi1-6:",coup, marque)
                return(coup)
    
#coup ordinateur niveau2
def coupordi2(marque,SEQUENCE,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées(SEQUENCE)
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(SEQUENCE)==0:
        coup="12/12"
        print("coup ordi2-0:",coup, marque)
        return(coup)

    imin=max(int(SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if GRILLE[i][j]=="-":
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    print("coup ordi2-2:",coup)
                    return(coup)

    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seq=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù".replace("ù",marque),2,GRILLE)
                res=result[0]
                if res!= "Non":
                    seq=seq+[coup]
                result=cherche_size(coup,marque,"ùù-".replace("ù",marque),2,GRILLE)
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
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i]]
    else:
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i+1]]  
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
                if GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi2-10:",coup, seq)
            return(coup)

#coup ordinateur niveau3
def coupordi3(marque,SEQUENCE,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées(SEQUENCE)
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]

#1er coup ordinateur quand il joue en 1er
    if len(SEQUENCE)==0:
        coup="12/12"
        print("coup ordi3-0:",coup, marque)
        return(coup)

    imin=max(int(SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if GRILLE[i][j]=="-":
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ù-ùùù-ù".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùù-ù-ùùù".replace("ù",marque),6,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"ù-ùùù-ù".replace("ù",marque1),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù-ùùù".replace("ù",marque1),6,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ù-ùù-".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùù-ù-".replace("ù",marque),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùù-u".replace("ù",marque),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùù-".replace("ù",marque1),3,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"-ùùùù".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùùù-".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ù-ùùù".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù".replace("ù",marque1),4,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùùù&".replace("ù",marque).replace("&",marque1),2,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"&ùùù-".replace("ù",marque).replace("&",marque1),2,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùù-".replace("ù",marque1),2,GRILLE)
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
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i]]
    else:
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i+1]]  
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
                if GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi3-12:",coup, seq)
            return(coup)

#coup ordinateur niveau4
def coupordi4(marque,SEQUENCE,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées(SEQUENCE)
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]
#1er coup ordinateur quand il joue en 1er
    if len(SEQUENCE)==0:
        coup="12/12"
        print("coup ordi4-0:",coup, marque)
        return(coup)

    imin=max(int(SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if GRILLE[i][j]=="-":
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5,GRILLE)
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
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                scor=score(coup,marque,GRILLE)
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
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i]]
    else:
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i+1]]  
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
                if GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi4-4:",coup, seq)
            return(coup)

#coup ordinateur niveau5
def coupordi5(marque,SEQUENCE,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    bornes=calculbornesjouées(SEQUENCE)
    ibmin=bornes[0]
    ibmax=bornes[1]
    jbmin=bornes[2]
    jbmax=bornes[3]
#1er coup ordinateur quand il joue en 1er
    if len(SEQUENCE)==0:
        coup="12/12"
        print("coup ordi5-0:",coup, marque)
        return(coup)

    imin=max(int(SEQUENCE[-1].split("/")[1])-1,0)
    imax=min(int(SEQUENCE[-1].split("/")[1])+1,24)
    jmin=max(int(SEQUENCE[-1].split("/")[0])-1,0)
    jmax=min(int(SEQUENCE[-1].split("/")[0])+1,24)

    #1er coup ordinateur quand le joueur commence
    seq=[]
    if len(SEQUENCE)==1:
        seq=[]
        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                if GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi5-1:",coup)
            return(coup)

    #recherche du coup entrainant la victoire soit ùùùùù
    seq=[]
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    print("coup ordi5-2:",coup)
                    return(coup)

    #recherche du coup de l'adversaire à contrer entrainant sa victoire soit ùùùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque1),5,GRILLE)
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
        print("coup ordi5-3 :",coup, seqmax)
        return(coup)
    
    ##recherche du coup entrainant -ùùùù- et ù-ùùù-u et ùùù-ù-ùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ù-ùùù-ù".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùù-ù-ùùù".replace("ù",marque),6,GRILLE)
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
        print("coup ordi5-4 :",coup, seqmax)
        return(coup)
    
    #recherche des coups entrainant -ùùùù et ùùùù- et ùùù-ù et ùù-ùùet ù-ùùù
    seqmax=[]
    seq4=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùù-ù".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùù-ùù".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
            if nb>0:
                
                seq4=seq4+[coup]
                if nb>nbmax:
                    seqmax=[coup]
                    coupmax=coup
                    nbmax=nb
            if nbmax>1:
                return(coupmax)
            
    #recherche récursive suite aux coups entrainant -ùùùù- et ù-ùùù-u et ùùù-ù-ùùù
    for coup4_0 in seq4:
        imin4_0=max(0,int(coup4_0.split("/")[1])-5)
        imax4_0=min(24,int(coup4_0.split("/")[1])+5)
        jmin4_0=max(0,int(coup4_0.split("/")[0])-5)
        jmax4_0=min(24,int(coup4_0.split("/")[0])+5)
        GRILLE4_0=[["-"] * 25 for _ in range(25)]
        for j in range(0,25):
            for i in range(0,25):
                GRILLE4_0[i][j]=GRILLE[i][j]
        GRILLE4_0=majgrille(coup4_0,marque,GRILLE4_0)
        #recherche du coup empêchant la victoire soit ùùùùù
        seqdef_0=[]
        for i in range(imin4_0,imax4_0+1):
            for j in range(jmin4_0,jmax4_0+1):
                if GRILLE4_0[i][j]=="-":
                    coup=str(j)+"/"+str(i)
                    result=cherche_size(coup,marque1,"ùùùùù".replace("ù",marque),5,GRILLE4_0)
                    res=result[0]
                    if res!= "Non":
                       seqdef_0=seqdef_0+[coup]
        testvictoire=False
        for coup4_1 in seqdef_0:
            imin4_1=max(0,int(coup4_1.split("/")[1])-5)
            imax4_1=min(24,int(coup4_1.split("/")[1])+5)
            jmin4_1=max(0,int(coup4_1.split("/")[0])-5)
            jmax4_1=min(24,int(coup4_1.split("/")[0])+5)
            GRILLE4_1=[["-"] * 25 for _ in range(25)]
            for j in range(0,25):
                for i in range(0,25):
                    GRILLE4_1[i][j]=GRILLE4_0[i][j]
            GRILLE4_1=majgrille(coup4_1,marque1,GRILLE4_1)
            seqdef_1=[]
            for i in range(imin4_1,imax4_1+1):
                for j in range(jmin4_1,jmax4_1+1):
                    testvictoire=False
                    #recherche du coup entrainat la victoire soit ùùùùù
                    if GRILLE4_1[i][j]=="-":
                        coup=str(j)+"/"+str(i)
                        result=cherche_size(coup,marque,"ùùùùù".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            testvictoire=True
            if testvictoire==False:
                break
        if testvictoire==True:
            print("coup ordi5-recur :",coup4_0)
            return(coup4_0)
        
        for coup4_1 in seqdef_0:
            imin4_1=max(0,int(coup4_1.split("/")[1])-5)
            imax4_1=min(24,int(coup4_1.split("/")[1])+5)
            jmin4_1=max(0,int(coup4_1.split("/")[0])-5)
            jmax4_1=min(24,int(coup4_1.split("/")[0])+5)
            GRILLE4_1=[["-"] * 25 for _ in range(25)]
            for j in range(0,25):
                for i in range(0,25):
                    GRILLE4_1[i][j]=GRILLE4_0[i][j]
            GRILLE4_1=majgrille(coup4_1,marque1,GRILLE4_1)
            seqdef_1=[]
            nbmax=0
            for i in range(imin4_1,imax4_1+1):
                for j in range(jmin4_1,jmax4_1+1):
                    ##recherche des coup  entrainant -ùùùù ou ùùùù- ou ùùù-u ou ù-ùùù ou -ùùù-
                    nb=0
                    if GRILLE4_1[i][j]=="-":
                        coup=str(j)+"/"+str(i)
                        result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            nb=nb+result[1]
                        result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            nb=nb+result[1]
                        result=cherche_size(coup,marque,"ùùù-ù".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            nb=nb+result[1]
                        result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            nb=nb+result[1]
                        result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),5,GRILLE4_1)
                        res=result[0]
                        if res!= "Non":
                            seqdef_1=seqdef_1+[coup]
                            nb=nb+result[1]
                        if nb>nbmax:
                            nbmax=nb
                            coupmax=coup
            if nbmax>1:
                print("coup ordi5-recur :",coup4_0)
                return(coup4_0)                
                    
    #recherche des coup de  l'adversaire entrainant -ùùùù- et ù-ùùù-u et ùùù-ù-ùùù
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"ù-ùùù-ù".replace("ù",marque1),6,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù-ùùù".replace("ù",marque1),6,GRILLE)
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
        print("coup ordi5-5 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ùùù- ou -ùùùù ou ùùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
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
        print("coup ordi5-6 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ù-ùù- ou -ùù-ù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ù-ùù-".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùù-ù-".replace("ù",marque),4,GRILLE)
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
        print("coup ordi5-6bis :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant -ùùùù ou ùùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùùùù".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùùù-".replace("ù",marque),4,GRILLE)
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
        print("coup ordi5-7 :",coup, seqmax)
        return(coup)
    
    ##recherche des coup  entrainant ùùù-ù ou ù-ùùù ou -ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"ùùù-ù".replace("ù",marque),4,GRILLE)
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
        print("coup ordi5-8 :",coup, seqmax)
        return(coup)
    
    ##recherche du coup de l'adversaire entrainant -ùùùù ou uuuu- ou ù-ùùù ou ùùù-ù -ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùùù-".replace("ù",marque1),3,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque1,"-ùùùù".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùùù-".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ù-ùùù".replace("ù",marque1),4,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=nb+result[1]
                result=cherche_size(coup,marque1,"ùùù-ù".replace("ù",marque1),4,GRILLE)
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
        print("coup ordi5-9:",coup, seqmax)
        return(coup)
        
    ##recherche du coup du joueur entrainant -ùù- -ùùù& &ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"-ùùù&".replace("ù",marque).replace("&",marque1),2,GRILLE)
                res=result[0]
                if res!= "Non":
                    nb=result[1]
                result=cherche_size(coup,marque,"&ùùù-".replace("ù",marque).replace("&",marque1),2,GRILLE)
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
        print("coup ordi5-10:",coup, seqmax)
        return(coup)
    
    ##recherche du coup de l'adversaire entrainant -ùù- -ùùù& &ùùù-
    seqmax=[]
    nbmax=0
    for i in range(ibmin,ibmax+1):
        for j in range(jbmin,jbmax+1):
            nb=0
            if GRILLE[i][j]=="-":
                coup=str(j)+"/"+str(i)
                result=cherche_size(coup,marque1,"-ùù-".replace("ù",marque1),2,GRILLE)
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
        print("coup ordi5-11:",coup, seqmax)
        return(coup)
                    

    
    #Recherche des coups adjacents au dernier coup de l'adversaire.
    #Un des coups est choisi aléatoirement. Si pas de coup trouvé on passe au coup précédent.
    SEQO=[]
    if marque=="X":
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i]]
    else:
        for i in range(0,len(SEQUENCE),2):
            SEQO=SEQO+[SEQUENCE[i+1]]  
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
                if GRILLE[i][j]=="-":
                    seq=seq+[str(j)+"/"+str(i)]
        if seq!=[]:
            random.shuffle(seq)
            coup=seq[0]
            print("coup ordi5-12:",coup, seq)
            return(coup)

def score(coup,marque,GRILLE):
    if marque=="X":
        marque1="O"
    else:
        marque1="X"
    nb=0
    #joueur :-ùùùù- ù-ùùù-ù ùùù-ù-ùùù
    result=cherche_size(coup,marque,"-ùùùù-".replace("ù",marque),5,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ù-ùùù-ù".replace("ù",marque),6,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ùùù-ù-ùùù".replace("ù",marque),6,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb1=nb
    #adversaire :-ùùùù- ù-ùùù-ù ùùù-ù-ùùù
    nb=0
    result=cherche_size(coup,marque1,"-ùùùù-".replace("ù",marque1),5,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ù-ùùù-ù".replace("ù",marque1),6,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ùùù-ù-ùùù".replace("ù",marque1),6,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb1d=nb
    #joueur -ùùù- ùùùù- ùùùù- 
    nb=0
    result=cherche_size(coup,marque,"-ùùù-".replace("ù",marque),3,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"-ùùùù&".replace("ù",marque).replace("&",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"&ùùùù-".replace("ù",marque).replace("&",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2=nb
    if nb2>=2:
        print("nb2",nb2,coup)
    
    #joueur ù-ùùù ùùù-ù -ù-ùù- -ùù-ù-
    nb=0
    result=cherche_size(coup,marque,"-ù-ùù-".replace("ù",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"-ùu-ù-".replace("ù",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ù-ùùù".replace("ù",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"ùùù-u".replace("ù",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2bis=nb
    if nb2bis>=3:
        print("nb2bis",nb2bis,coup)
    
    #adversairejoueur -ùùù- ùùùù- ùùùù- 
    nb=0
    result=cherche_size(coup,marque1,"-ùùù-".replace("ù",marque1),3,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque1,"&ùùùù-".replace("ù",marque1).replace("&",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"-ùùùù&".replace("ù",marque1).replace("&",marque),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2d=nb
    if nb2d>=3:
        print("nb2d",nb2d,coup)
    
    #adversairejoueur ù-ùùù ùùù-ù -ù-ùù- -ùù-ù-
    nb=0
    result=cherche_size(coup,marque1,"-ù-ùù-".replace("ù",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"-ùu-ù-".replace("ù",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ù-ùùù".replace("ù",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"ùùù-u".replace("ù",marque1),4,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb2dbis=nb
    if nb2dbis>=2:
        print("nb2dbis",nb2dbis,coup)

    #joueur -ùù- &ùùù- -ùùù&
    nb=0
    result=cherche_size(coup,marque,"-ùù-".replace("ù",marque),2,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque,"-ùùù&".replace("ù",marque).replace("&",marque1),2,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque,"&ùùù-".replace("ù",marque).replace("&",marque1),2,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    nb3=nb
    #adversaire -ùù- &ùùù- -ùùù&
    nb=0
    result=cherche_size(coup,marque1,"-ùù-".replace("ù",marque1),2,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=result[1]
    result=cherche_size(coup,marque1,"-ùùù&".replace("ù",marque1).replace("&",marque),2,GRILLE)
    res=result[0]
    if res!= "Non":
        nb=nb+result[1]
    result=cherche_size(coup,marque1,"&ùùù-".replace("ù",marque1).replace("&",marque),2,GRILLE)
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
def majgrille(coup,marque,GRILLE):
    y=int(coup.split("/")[0])
    i=int(coup.split("/")[1])
    GRILLE[i][y]=marque
    return(GRILLE)

def trouve_5(coup,marque,GRILLE):
    marque5=marque*5
    grid=GRILLE
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

def cherche_size(coup,marque,rech,size,GRILLE):
    grid=[["-"] * 25 for _ in range(25)]
    for j in range(0,25):
        for i in range(0,25):
            grid[i][j]=GRILLE[i][j]
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
def calculbornesjouées(seq):
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

def nbtour(SEQUENCE):
    res=len(SEQUENCE)
    return((res//2)+1)

















