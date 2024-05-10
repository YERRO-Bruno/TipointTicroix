from django.conf import settings

#FONCTIONS

#Coup ordinateur
def coupordi(tour):
    coup=""
    #while (settings.GRILLE[1][tour] !="" and tour<25):
    #    tour=tour+1
    coup=str(tour)+"/1"
    return(coup)

#MAJ GRILLE avec le coup joué
def majgrille(coup,marque):
    y=int(coup.split("/")[0])
    i=int(coup.split("/")[1])
    settings.GRILLE[i][y]=marque

#A t-on 5 marques allignés avec le coup joué?
def trouve_5save(coup,marque):
    #ligne horizontale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    imin=i0-4
    imax=i0+4
    ligneH=""
    for k in range(0,10):
        if imin+k > -1 or imin+k<25:
            ligneH=ligneH + settings.GRILLE[imin+k][j0].replace("","-")
    ret=ligneH.find("OOOOO")
    print("imin : "+str(imin)+" - imax : "+str(imax) +" - j0 : "+str(j0)+" - h : "+ligneH, ret)
    
    if ret != -1:
        iwin0 = imin + ret
        sequencewin=[]
        for i in range(iwin0,iwin0+5):
            idx=str(j0)+"/"+str(i)
            sequencewin = sequencewin + [idx]
        print("5 alignés trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)
    
    #ligne verticale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    jmin=j0-4
    jmax=j0+4
    ligneV=""
    for k in range(0,10):
        if jmin+k > -1 or jmin+k<25:
            ligneV=ligneV + settings.GRILLE[i0][jmin+k]
    ret=ligneV.find("OOOOO")
    print("imin : "+str(jmin)+" - imax : "+str(jmax) +" - i0 : "+str(i0)+" - h : "+ligneV, ret)
    
    if ret != -1:
        jwin0 = jmin + ret
        sequencewin=[]
        for j in range(jwin0,jwin0+5):
            idx=str(j)+"/"+str(i0)
            sequencewin = sequencewin + [idx]
        print("5 alignés trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)
    
    #ligne oblique / de 9 caractères avec coup au millieu (moins si bordure atteinte)
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    imin=i0-4
    imax=i0+4
    jmin=j0-4
    jmax=j0+4
    ligneV=""
    #if imin+k > -1 or jmax+k or jmin+k > -1 or jmax+k>25:
    return("Non")

def trouve_5(coup,marque):
    marque5=marque*5
    #ligne horizontale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    grid=settings.GRILLE
    for i in range(0,25):
        for j in range(0,25):
            if grid[i][j]=="":
                grid[i][j]="-"
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    imin=max(i0-4,0)
    imax=min(i0+4,24)
    ligneH=""
    for i in range(imin,imax+1):
        ligneH=ligneH + grid[i][j0]
    ret=ligneH.find(marque5)
    print("imin : "+str(imin)+" - imax : "+str(imax) +" - j0 : "+str(j0)+" - H : "+ligneH, ret)
    
    if ret != -1:
        iwin0 = imin + ret
        sequencewin=[]
        for i in range(iwin0,iwin0+5):
            idx=str(j0)+"/"+str(i)
            sequencewin = sequencewin + [idx]
        print("5 alignés horizontal trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)
    
#ligne verticale de 9 caractères avec coup au millieu (moins si bordure atteinte)
    grid=settings.GRILLE
    for i in range(0,25):
        for j in range(0,25):
            if grid[i][j]=="":
                grid[i][j]="-"
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    jmin=max(j0-4,0)
    jmax=min(j0+4,24)
    ligneV=""
    for j in range(jmin,jmax+1):
        ligneV=ligneV + grid[i0][j]
    ret=ligneV.find(marque5)
    print("jmin : "+str(jmin)+" - jmax : "+str(jmax) +" - i0 : "+str(i0)+" - V : "+ligneV, ret)
    
    if ret != -1:
        jwin0 = jmin + ret
        sequencewin=[]
        for j in range(jwin0,jwin0+5):
            idx=str(j)+"/"+str(i0)
            sequencewin = sequencewin + [idx]
        print("5 alignés vertical trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)

#ligne oblique / (slach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    grid=settings.GRILLE
    for i in range(0,25):
        for j in range(0,25):
            if grid[i][j]=="":
                grid[i][j]="-"
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    jmin=max(j0-4,0)
    jmax=min(j0+4,24)
    imin=max(i0-4,0)
    imax=min(i0+4,24)
    ligneS=""
    for k in range(0,10):
        if i0-4+k>0 and i0-4+k<25 and j0+4-k>0 and j0+4-k<24 :
            ligneS=ligneS + grid[i0-4+k][j0+4-k]
    ret=ligneS.find(marque5)
    print("/ : "+ligneS, ret)
    
    if ret != -1:
        sequencewin=[]
        for k in range(0,5):
            idx=str(jmax-k-ret)+"/"+str(imin+k+ret)
            sequencewin = sequencewin + [idx]
        print("5 alignés vertical trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)
    
#ligne oblique \ (antislach) de 9 caractères avec coup au millieu (moins si bordure atteinte)
    grid=settings.GRILLE
    for i in range(0,25):
        for j in range(0,25):
            if grid[i][j]=="":
                grid[i][j]="-"
    j0=int(coup.split("/")[0])
    i0=int(coup.split("/")[1])
    jmin=max(j0-4,0)
    jmax=min(j0+4,24)
    imin=max(i0-4,0)
    imax=min(i0+4,24)
    ligneA=""
    for k in range(0,10):
        if i0-4+k>0 and i0-4+k<25 and j0-4+k>0 and j0-4+k<25 :
            ligneA=ligneA + grid[i0-4+k][j0-4+k]
    ret=ligneA.find(marque5)
    print("\ : "+ligneA, ret)
    
    if ret != -1:
        sequencewin=[]
        for k in range(0,5):
            idx=str(jmin+k+ret)+"/"+str(imin+k+ret)
            sequencewin = sequencewin + [idx]
        print("5 alignés vertical trouvés : ",sequencewin)
        win=','.join([str(i) for i in sequencewin])
        return(win)

    return("Non")