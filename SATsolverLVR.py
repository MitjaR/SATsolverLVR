import copy

class CNFproblem:
    def __init__(self,stSpr,stSta,sezAnd,lokPoz,lokNeg):
        self.sezAnd=sezAnd
        self.stSpremenljivk=stSpr
        self.stSprPlsEna=self.stSpremenljivk+1
        self.stStavkov=stSta
        self.lokacijePoz=lokPoz
        self.lokacijeNeg=lokNeg
        self.testOK()

    def __repr__(self):
        return str(((self.stSpremenljivk,self.stStavkov),self.sezAnd))

    def vrniStSprSta(self):
        return self.stSpremenljivk,self.stStavkov

    def testOK(self):
        if (len(self.sezAnd)!=self.stStavkov or
            len(self.lokacijePoz)!=self.stSprPlsEna or
            len(self.lokacijeNeg)!=self.stSprPlsEna):
            print("Napacni podatki (CNFproblem)")
            print(self)
            print(len(self.sezAnd),self.stStavkov)
            print(len(self.lokacijePoz),self.stSprPlsEna)
            print(len(self.lokacijeNeg),self.stSprPlsEna)
            print(self.lokacijePoz)
            1/0

    def __odstraniElement__(self,element):
        def pppIzpraznitevMnInLokacijGor(sezAnd,lok1,elementAbs):
            for indMn in list(lok1[elementAbs]):
                for elem in sezAnd[indMn]:
                    elemAbs=abs(elem)
                    ##print(elem)
                    ##print(indMn)
                    ##print(lok1[elemAbs])
                    lok1[elemAbs].remove(indMn)

                sezAnd[indMn]=set()
                
            if len(lok1[elementAbs])!=0:
                print("Napaka pri odstranjevanju"),1/0
                              
        def krZapis(sezAnd,lok1,lok2,elementAbs,element):
            pppIzpraznitevMnInLokacijGor(sezAnd,lok1,elementAbs)

            for z in lok2[elementAbs]:
                if len(sezAnd[z])==1:
                    ##neuspesno odstranjevanje
                    ##SAT se pri teh pogojih ne zadosti
                    return False
                ##print(z)
                ##print(sezAnd[z])
                ##print(element)
                sezAnd[z].remove(-element)

            lok2[elementAbs]=set()

            ##uspesna odstranitev (nikjer prazna mnozica)
            return True

        elementAbs=abs(element)
        lKonst=True
        if element>0:
            lKonst=lKonst and krZapis(self.sezAnd,self.lokacijePoz,self.lokacijeNeg,elementAbs,element)
        else:
            lKonst=lKonst and krZapis(self.sezAnd,self.lokacijeNeg,self.lokacijePoz,elementAbs,element)

        ##ce lKonst==False potem moramo prekiniti
        return lKonst

    def odstraniElementNaKopiji(self,element):
        kopijaCNF=copy.deepcopy(self)
        lKonst=kopijaCNF.__odstraniElement__(element)
        return lKonst,kopijaCNF

    def poisciNajmanjsoNepraznoMnozico(self):
        a=float("inf")
        minMnozica={0}##ce vrne to je napaka
        for i in range(1,len(self.sezAnd)):
            b=len(self.sezAnd[i])
            if b==1:
                return self.sezAnd[i]

            elif 0<b<a:
                a=b
                minMnozica=self.sezAnd[i]

        ##zakaj to ne dela
        ##return minMnozica.copy()         
        ##return copy.deepcopy(minMnozica)
        ##return set([z for z in minMnozica])
        return minMnozica

    def poisciNajboljPureElement(self):
        ##glej poisciNaj..Nepr..Mn
        def poisciNajPure(a,najboljPure,lokacije):
            for i in range(1,len(lokacije)):
                b=len(lokacije[i])
                if b==1:
                    return i

                elif 0<b<a:
                    a=b
                    najboljPure=i

            return najboljPure
            
        a=len(self.lokacijePoz)
        najboljPure=1
        najboljPure=poisciNajPure(a,najboljPure,self.lokacijePoz)
        najboljPure=-poisciNajPure(a,najboljPure,self.lokacijeNeg)

        return najboljPure,a

    ##poisci razpadni element

    ##poisci razpadno mnozico

    ##odstrani podvojene mnozice

    def vrniSteviloPozNeg(self,element):
        return self.lokacijePoz[element],self.lokacijeNeg[element]

def preberiDimacsVrniCNF(vhod):
    def vrniLokacijeInSezAnd(sezAndGen,stSpremenljivk):
        sezAnd=list()
        stSprPlsEna=stSpremenljivk+1
        lokacijePoz=[set() for _ in range(stSprPlsEna)]
        lokacijeNeg=[set() for _ in range(stSprPlsEna)]
        
        for (i, gen) in enumerate(sezAndGen):
            sez=list(gen)
            sezAnd.append(set(sez))
            for z in sez:
                if z>0:
                    lokacijePoz[z].add(i)
                else:
                    lokacijeNeg[abs(z)].add(i)

        return lokacijePoz,lokacijeNeg,sezAnd
                    
        
    sezAndGen=[]
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
                    sezAndGen.append(map(int,sez[:-1]))
                else:
                    print(sez)
                    print("Napacen format.")
                    1/0
    
    lokPoz,lokNeg,sezAnd=vrniLokacijeInSezAnd(sezAndGen,stSpremenljivk)
                
    return CNFproblem(stSpremenljivk, stStavkov, sezAnd, lokPoz, lokNeg)


def solveSat(lKonst,problemCNF,sezPrireditev,stPriTre,stPriKon):
    sigurnoPravilnaPot=False
    ##print(stPriTre)
##    print(problemCNF)
    ##POZOR: sezPrireditev;; copy...
    if not(lKonst):
        return False

    if stPriTre==stPriKon:
        return True
    
    zacMno=problemCNF.poisciNajmanjsoNepraznoMnozico()
    ##tole je zelo cudno
    mno=set([z for z in zacMno])
##    print(mno)
    if len(mno)==1:
        element=mno.pop()
        sigurnoPravilnaPot=True

    else:
        element,stPure=problemCNF.poisciNajboljPureElement()
        if stPure==1:
            print("Algoritem je v pure.")
            sigurnoPravilnaPot=True
            ##element je ze pravilno nastavljen
            ##glej par vrstic zgoraj
            pass
        else:
            print("Algoritem se veja.", len(mno))
            ##print(mno)
            element=mno.pop()
            ##element=-list(mno)[1]##TESTI ZA PRAVILNOST DELOVANJA
            ##print(element)

##    print(problemCNF)
##    print(stPriTre)
    ##print(sezPrireditev)
##    print(element)
##    eval("1"+input())
    sezPrireditev[stPriTre]=element
    if sigurnoPravilnaPot==True:
        problemCNF.__odstraniElement__(element)
        return solveSat(lKonst,problemCNF,sezPrireditev,stPriTre+1,stPriKon)
    else:
        lKonst,novProblemCNF=problemCNF.odstraniElementNaKopiji(element)
        if solveSat(lKonst,novProblemCNF,sezPrireditev,stPriTre+1,stPriKon):
            return True
        else:
            element=-element
            sezPrireditev[stPriTre]=element
            lKonst,novProblemCNF=problemCNF.odstraniElementNaKopiji(element)
            return solveSat(lKonst,novProblemCNF,sezPrireditev,stPriTre+1,stPriKon)


##def main():
##    problemCNF=preberiDimacsVrniCNF("sudoku1.txt")
##    stSpr,_=problemCNF.vrniStSprSta()
##    sezPrireditev=[0 for _ in range(stSpr)]
##    return solveSat(True,problemCNF,sezPrireditev,0,stSpr),sezPrireditev
##
##main()

##problemCNF=preberiDimacsVrniCNF("sudoku1.txt")
##stSpr,_=problemCNF.vrniStSprSta()
##sezPrireditev=[0 for _ in range(stSpr)]
##resitev=solveSat(True,problemCNF,sezPrireditev,0,stSpr)
##print(sezPrireditev)

def SATsolverDimacs(vhod,izhod=""):
    problemCNF=preberiDimacsVrniCNF(vhod)
    stSpr,_=problemCNF.vrniStSprSta()
    sezPrireditev=[0 for _ in range(stSpr)]
    resitev=solveSat(True,problemCNF,sezPrireditev,0,stSpr)
    print("Naloga je resljiva:", resitev)
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
    return sez1==sez2
            
##SATsolverDimacs("sudoku1.txt",izhod="")
##testProblemov("sudoku1.txt","sudoku1_solution.txt")

##SATsolverDimacs("sudoku2.txt",izhod="")
testProblemov("sudoku2.txt","sudoku2_solution.txt")
