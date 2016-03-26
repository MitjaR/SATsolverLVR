def preberiDimacsVrniHudobniDimacs(vhod, izhod=""):
    sezAnd=[]
    with open(vhod, "r") as f:
        beremGlavo=True
        for vrstica in f:
            sez=vrstica.split()
            if beremGlavo:
                if sez[0]=="c":
                    print(" ".join(sez[1:]))
                elif sez[0]=="p":
                    stSpremenljivk=int(sez[2])
                    stStavkov=int(sez[3])
                    beremGlavo=False
                else:
                    print("Napacen format.")
                    1/0

            else:
                ##pripnemo generator
                if sez[-1]=="0":
                    sezAnd.append(list(map(int,sez[:-1])))
                else:
                    print(sez)
                    print("Napacen format.")
                    1/0


    sezS1=[]
    sezS2=[]
    sezS3=[]
    d=stSpremenljivk+51
    for gen in sezAnd:
        ##2*stSpremenljivk+2
        ####2x kopija problema z dodanim x/-x
        ####1x kopija problema z dodano y (resi takoj ce potrdi y sicer... traja)
        sez1=[z+51 if z>0 else (0 if z==0 else z-51) for z in gen]
        sez1.append(51)
        sez1.sort(key=lambda x: abs(x))
        sez1=sez1+[0]
        sezS1.append(sez1)
        sez2=[z+51 if z>0 else (0 if z==0 else z-51) for z in gen]
        sez2.append(-51)
        sez2.sort(key=lambda x: abs(x))
        sez2=sez2+[0]
        sezS2.append(sez2)
        sez3=[z+d if z>0 else (0 if z==0 else z-d) for z in gen]
        sez3.append(stSpremenljivk+d+1)
        sez3.sort(key=lambda x: abs(x))
        sez3=sez3+[0]
        sezS3.append(sez3)

    ##50
    s11=[i for i in range(1,11)]+[0]
    s21=[-i for i in range(11,21)]+[0]
    s31=[i for i in range(21,31)]+[0]
    s41=[-i for i in range(31,37)]+[0]
    s51=[i for i in range(37,41)]+[0]
    s61=[-i for i in range(41,45)]+[0]
    s71=[i for i in range(45,51)]+[0]
    sezP1=[s11,s21,s31,s41,s51,s61,s71]

    d=2*stSpremenljivk+50+2
    ##50
    s10=[i for i in range(d+1,d+11)]+[0]
    s20=[-i for i in range(d+11,d+21)]+[0]
    s30=[i for i in range(d+21,d+31)]+[0]
    s40=[-i for i in range(d+31,d+37)]+[0]
    s50=[i for i in range(d+37,d+41)]+[0]
    s60=[-i for i in range(d+41,d+45)]+[0]
    s70=[i for i in range(d+45,d+51)]+[0]
    sezP2=[s10,s20,s30,s40,s50,s60,s70]

    novSezAnd=sezS1+sezS2+sezS3+sezP1+sezP2
    novSezAnd.sort(key=lambda x: len(x))
    novStSpremenljivk=2*stSpremenljivk+50+50+2
    novStStavkov=len(novSezAnd)

    if izhod=="":
        izhod="h_"+vhod
    with open(izhod, "w") as g:
        niz="c hudobni_"+vhod
        g.write(niz+"\n")
        niz="p cnf {0} {1} 0".format(novStSpremenljivk,novStStavkov)
        g.write(niz+"\n")
        for sez in novSezAnd:
            niz=" ".join([str(z) for z in sez])
            g.write(niz+"\n")
            
        
preberiDimacsVrniHudobniDimacs("sudoku2.txt", izhod="")
    
