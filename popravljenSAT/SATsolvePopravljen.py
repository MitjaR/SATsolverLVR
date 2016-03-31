import copy

class obProblemCNF:
    def __init__(self):
        self.sezAnd=[]
        self.lokPoz=[set()]
        self.lokNeg=[set()]
        ##spremenljivke so
        ##absulutne izjave
        self.stSpr=0
        self.stSta=0
        ##tega mi sicer ne bi bilo treba hraniti
        self.sezPrired=[]
        self.sezNeuporabljenih=[]

    def __repr__(self):
        return str(((self.stSpr,self.stSta),self.sezPrired,self.sezAnd))
    
##    def __str__(self):
##        sezNizov=[]
##        for mnozica in self.sezAnd:
##            sez=[int(z) for z in mnozica]
##            sez.sort(key=lambda x: abs(x))
##            ##sez=[str(z) for z in sez]
##            sez=[str(z) if z>0 else "not("+str(z)+")" for z in sez]
##            ##niz=" \/ ".join(sez)
##            niz=" or ".join(sez)
##            if len(mnozica)>1:
##                niz="("+niz+")"
##            sezNizov.append(niz)
##
##        ##return " /\ ".join(sezNizov)
##        return " and ".join(sezNizov)
    
    def narediCNF(self,sezAndSez):
        def testInStSpr(sezAndSez):
            """Vrne 0 ce je ujemanje neuspesno."""
            
            mnoSpr=set()
            maxSpr=0
            for sez in sezAndSez:
                for izjava in sez:
                    spremenljivka=abs(izjava)
                    mnoSpr.add(spremenljivka)
                    if spremenljivka>maxSpr:
                        maxSpr=spremenljivka

            if len(mnoSpr)!=maxSpr:
                print("Neskladni podatki (stSpremenljivk)")
                return 0

            return maxSpr

        self.stSpr=testInStSpr(sezAndSez)
        if self.stSpr==0:
            return

        self.lokPoz=[set() for _ in range(self.stSpr+1)]
        self.lokNeg=[set() for _ in range(self.stSpr+1)]
        self.sezAnd=[{z for z in sez} for sez in sezAndSez]
        self.stSta=len(self.sezAnd)

        for i,sez in enumerate(sezAndSez):
            for izjava in sez:
                spremenljivka=abs(izjava)
                if izjava>0:
                    self.lokPoz[spremenljivka].add(i)
                else:
                    self.lokNeg[spremenljivka].add(i)

    def vrniStStaStSpr(self):
        return self.stSta,self.stSpr

    def odstraniLokacijo(self,izjava,indMno):
        spremenljivka=abs(izjava)
        if izjava>0:
            self.lokPoz[spremenljivka].remove(indMno)
        else:
            self.lokNeg[spremenljivka].remove(indMno)

        if (len(self.lokNeg[spremenljivka])==0
            and len(self.lokPoz[spremenljivka])==0
            and spremenljivka!=abs(self.sezPrired[-1])):
            self.sezNeuporabljenih.append(spremenljivka)

    def potrdiIzjavo(self,izjava):
        ##potrdiIzjavo ce se da sicer vrne False
        self.sezPrired.append(izjava)
        spremenljivka=abs(izjava)
        if izjava>0:
            sezOdstraniMnoInd=[indMno for indMno in self.lokPoz[spremenljivka]]
            for indMno in sezOdstraniMnoInd:
                for izjavaOds in self.sezAnd[indMno]:
                    self.odstraniLokacijo(izjavaOds,indMno)

                self.sezAnd[indMno]=set()

            if len(self.lokPoz[spremenljivka])>0:
                print("Napaka pri odstranjevanju (potrdiIzjavo)"),1/0

            for indMno in self.lokNeg[spremenljivka]:
                if len(self.sezAnd[indMno])==1:
                    ##problem ni izpolnjiv
                    return False
                self.sezAnd[indMno].remove(-spremenljivka)

            self.lokNeg[spremenljivka]=set()

        else:
            sezOdstraniMnoInd=[indMno for indMno in self.lokNeg[spremenljivka]]##!!!
            for indMno in sezOdstraniMnoInd:
                for izjavaOds in self.sezAnd[indMno]:
                    self.odstraniLokacijo(izjavaOds,indMno)

                self.sezAnd[indMno]=set()

            if len(self.lokNeg[spremenljivka])>0:##!!!
                print("Napaka pri odstranjevanju (potrdiIzjavo)"),1/0

            for indMno in self.lokPoz[spremenljivka]:##!!!
                if len(self.sezAnd[indMno])==1:
                    ##problem ni izpolnjiv
                    return False
                self.sezAnd[indMno].remove(spremenljivka)

            self.lokPoz[spremenljivka]=set()##!!!

        return True

    def poisciNajmanjsoNepraznoMnozico(self):
        ##vrni pa seznam te mnozice

        minLen=float("inf")
        minMno={0}
        for mno in self.sezAnd:
            if 0<len(mno)<minLen:
                ##>a se to splaca?
                if len(mno)==1:
                    return list(mno)
                ##<
                minLen=len(mno)
                minMno=mno

        return list(minMno)

    def poisciNajboljPureSpr(self):
        pureSt=float("inf")
        najPureSpr=0
        for spremenljivka in range(1,self.stSpr+1):
            a=len(self.lokPoz[spremenljivka])
            b=len(self.lokNeg[spremenljivka])

            if (a==0 and b!=0) or (b==0 and a!=0):
                return spremenljivka
            else:
                if 0<min(a,b)<pureSt:
                    pureSt=min(a,b)
                    najPureSpr=spremenljivka
                
        return najPureSpr

    def steviloPojavitevSpremenljivkePozNeg(self,spremenljivka):
        return len(self.lokPoz[spremenljivka]),len(self.lokNeg[spremenljivka])

    def vrniSkrcenSezAnd(self):
        mnoProstihSpr=set([abs(izjava) for mno in self.sezAnd for izjava in mno])
        sezProstihSpr=list(mnoProstihSpr)
        sezProstihSpr.sort()

        slovarMenjav=dict(zip(sezProstihSpr,range(1,len(sezProstihSpr)+1)))
        novSezAnd=[{(-1 if izjava<0 else 1)*slovarMenjav[abs(izjava)]
                    for izjava in mno} for mno in self.sezAnd]

        return novSezAnd, slovarMenjav
	
    def vrniSezPotrjenih(self):
        return self.sezPrired

    def vrniNeuporabljene(self):
        return self.sezNeuporabljenih

    ##poisci razpadni element

    ##poisci razpadno mnozico

    ##odstrani podvojene mnozice: (je dodan se se ne uporablja)


####Ni dobro zaradi globine rekurzije	
##def resiSAT(lKonst,problemCNF,trIndeks,stSpremenljivk,sezPotKonec):
##    if not(lKonst):
##        return False
##    if trIndeks==stSpremenljivk:
##        sezPotKonec.append(problemCNF.vrniSezPotrjenih())
##        return True
##            
##    pravilnaPot=False
##    
##    sez=problemCNF.poisciNajmanjsoNepraznoMnozico()
##    if len(sez)==1:
##        pravilnaPot=True
##        izjava=sez[0]
##        ##print(trIndeks,"mnI",izjava)
##            
##    else:
##        najPureSpr=problemCNF.poisciNajboljPureSpr()
##        stNeg,stPoz=problemCNF.steviloPojavitevSpremenljivkePozNeg(najPureSpr)
##        if min(stNeg,stPoz)==0:
##            pravilnaPot=True
##            if stPoz>stNeg:
##                izjava=najPureSpr
##            else:
##                izjava=-najPureSpr
##
##            ##print(trIndeks,"prI",izjava)
##        else:
##            ##pravilnaPot=False
##            izjava=sez[0]
##            ##print(trIndeks,"veI",izjava)
##                    
##    if pravilnaPot:
##        lKonst=problemCNF.potrdiIzjavo(izjava)
##
##        return resiSAT(lKonst,problemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)
##            
##    else:
##        novProblemCNF=copy.deepcopy(problemCNF)
##        lKonst=novProblemCNF.potrdiIzjavo(izjava)
##
##        if not(resiSAT(lKonst,novProblemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)):
##            lKonst=problemCNF.potrdiIzjavo(izjava)
##            resiSAT(lKonst,problemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)
		
####def testIzgradnje():
####    sezAnd=[{1,2,3},{-1,2,4},{-1,2,-3,-4}]
####    SATproblem=problemCNF()
####    SATproblem.narediCNF(sezAnd)
####    print(SATproblem)
####
####
####testIzgradnje()
        
####sezAnd=[{1,2,3},{-1,2,4},{-1,2,-3,-4}]
####SATproblem=obProblemCNF()
####SATproblem.narediCNF(sezAnd)
####print(SATproblem)
####x0=SATproblem.poisciNajmanjsoNepraznoMnozico()
####x1=SATproblem.poisciNajboljPureSpr()
####x2=SATproblem.potrdiIzjavo(-2)
####print(SATproblem)
####x3=SATproblem.vrniSkrcenSezAnd()


def preberiDimacsVrniSezAnd(vhod):
    sezAndSez=[]
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
                    sezAndSez.append(list(map(int,sez[:-1])))
                else:
                    print(sez)
                    print("Napacen format.")
                    1/0
    
    return sezAndSez,stSpremenljivk,stStavkov

####def prederiDimascInResiSAT(vhod):
####    sezAndSez,stSpremenljivk,stStavkov=preberiDimacsVrniSezAnd(vhod)
####    problemCNF=obProblemCNF()
####    problemCNF.narediCNF(sezAndSez)
####    _,stSpremenljivk=problemCNF.vrniStStaStSpr()
####    sezPotKonec=list()
####    lKonst=resiSAT(True,problemCNF,1,stSpremenljivk,sezPotKonec)
####    return sezPotKonec

def prederiDimascInResiSATwhile(vhod):
    sezAndSez,stSpr,stSta=preberiDimacsVrniSezAnd(vhod)
    problemCNF=obProblemCNF()
    problemCNF.narediCNF(sezAndSez)
    _,stSpremenljivk=problemCNF.vrniStStaStSpr()
    sezPotKonec=list()
    if stSpr!=stSpremenljivk:
        print("Napacna stevilo spremenljivk DIMACS."),1/0
    lKonst=resiSATwhile(True,problemCNF,0,stSpremenljivk,sezPotKonec)
    return lKonst,sezPotKonec

def resiSATwhile(lKonst,problemCNF,trIndeks,stSpremenljivk,sezPotKonec):
    ## trIndeks mora biti na zacetku 0
    while True:
        if not(lKonst):
            return False
        if trIndeks==stSpremenljivk:
            sezPotKonec.append(problemCNF.vrniSezPotrjenih())
            if len(sezPotKonec[0])!=stSpremenljivk:
                print("Kriticna napaka.")
                print("Ali st spr. pravilno:",len(sezPotKonec[0]),stSpremenljivk)
            return True
                
        pravilnaPot=False
        
        sez=problemCNF.poisciNajmanjsoNepraznoMnozico()
        if len(sez)==1:
            pravilnaPot=True
            izjava=sez[0]
##            print(trIndeks,"mnI",izjava)
                
        else:
            najPureSpr=problemCNF.poisciNajboljPureSpr()
            stPoz,stNeg=problemCNF.steviloPojavitevSpremenljivkePozNeg(najPureSpr)
            if min(stNeg,stPoz)==0:
                pravilnaPot=True
                if stPoz>stNeg:
                    izjava=najPureSpr
                else:
                    izjava=-najPureSpr

##                print(trIndeks,"prI",izjava)
            else:
                ##pravilnaPot=False
                izjava=sez[0]
##                print(trIndeks,"veI",izjava)

        if izjava==0:
            ##print("Pozor!!!")
            sezPotrjenih=problemCNF.vrniSezPotrjenih()
            sezNeuporabljenih=problemCNF.vrniNeuporabljene()
            if len(sezNeuporabljenih)+len(sezPotrjenih)==stSpremenljivk:
                sezPotKonec.append(sezPotrjenih+sezNeuporabljenih)
                return True
            else:
                print(len(sezNeuporabljenih),len(sezPotrjenih),stSpremenljivk)
                print(sezNeuporabljenih)
                print(sezPotrjenih)
                print("Napaka 0."),1/0
            
        if pravilnaPot:
            lKonst=problemCNF.potrdiIzjavo(izjava)

            ##return resiSAT(lKonst,problemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)
            trIndeks=trIndeks+1
            continue
                
        else:
            novProblemCNF=copy.deepcopy(problemCNF)
            lKonst=novProblemCNF.potrdiIzjavo(izjava)

            if not(resiSATwhile(lKonst,novProblemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)):
                lKonst=problemCNF.potrdiIzjavo(-izjava)
                ##resiSAT(lKonst,problemCNF,trIndeks+1,stSpremenljivk,sezPotKonec)
                trIndeks=trIndeks+1
                continue

            else:
                return True

def SATsolverDimacs(vhod,izhod=""):
    lkonst,sezPotKonec=prederiDimascInResiSATwhile(vhod)
    sezPrireditev=sezPotKonec[0]
    if lkonst:
        print("Naloga je resljiva.")
    else:
        print("Naloga ni resljiva.")
        return
    
    if izhod=="":
        izhod="res_"+vhod

    sezPrireditev.sort(key=lambda x: abs(x))
    with open(izhod, "w") as g:
        ##niz=" ".join([str(z) for z in sezPrireditev])
        niz=" ".join(map(str,sezPrireditev))
        g.write(niz)

def testProblemov(vhodDimacs,vhodResitev):
    def vrniSez(vhod):
        with open(vhod, "r") as f:
            for vrstica in f:
                sez=vrstica.split()
                return sez

    izhod="test_pravilnosti.txt"   
    SATsolverDimacs(vhodDimacs,izhod)
    sez1=vrniSez(izhod)
    sez2=vrniSez(vhodResitev)

    sez1.sort()
    sez2.sort()
    if sez1==sez2:
        print("Resitvi se ujemata.")
        ##print("Pozor. Problem je lahko pravilno resen a se resitvi ne ujemata.")
        ##print("Kaksni problemi imajo namrec vec resitev.")
    else:
        print("Resitvi se ne ujemata.")
        print("Pozor. Problem je lahko pravilno resen a se resitvi ne ujemata.")
        print("Kaksni problemi imajo namrec vec resitev.")

        print(sez1)
        print(sez2)

##SATsolverDimacs("sudoku1.txt",izhod="")
##testProblemov("sudoku1.txt","sudoku1_solution.txt")

##SATsolverDimacs("sudoku2.txt",izhod="")
testProblemov("sudoku2.txt","sudoku2_solution.txt")

print()
####print("""prederiDimascInResiSAT("h_sudoku1.txt")""")
####print("""prederiDimascInResiSAT("h_sudoku2.txt")""")
####print("""prederiDimascInResiSAT("sudoku2.txt")""")
##print("""prederiDimascInResiSATwhile("h_sudoku1.txt")""")
print("""prederiDimascInResiSATwhile("h_sudoku2.txt")""")
##print("""prederiDimascInResiSATwhile("sudoku2.txt")""")

print("""prederiDimascInResiSATwhile("neresljiv.txt")""")
