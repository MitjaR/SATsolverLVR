# SATsolverLVR
SATsolverLVR resi problem logicne izpolnjivosti

### Osnovni sat solver
##### Uporablja:
1. Unit clause (poisciNajmanjsoNepraznoMnozico)
2. Pure (poisciNajboljPureElement)
3. Pametno kopiranje strukture, samo kadar se veja

##### Mozne izboljsave:
4. Odstrani prazne mnozice in preindeksiraj
5. Odstrani podvojene mnozice (glej 4.)
6. Poisci razpadni element (nato razdeli problem na vec delov)
7. Poisci razpadno mnozico (nato razdeli problem na vec delov)

Pri tem je pomembno, da se tocke 4,5,6,7 smejo izvajati samno na <br />
vec iteracij in ne na vsako saj bi to porabilo prevec casa. <br />

Tocke je smiselno izvajati ob vejitvah, zato da imamo tudi minimalno <br />
stevilo kopij CNFproblem. <br />

### Navodila za uporabo: 
##### SATsolverDimacs
SATsolverDimacs(vhod,izhod="") <br />
Prebere datoteko podano kot vhod in jo pretvori v CNFproblem. <br />
CNFproblem je strukturo za zapis problema v CNF obliki. <br />
resitev=solveSat(True,problemCNF,sezPrireditev,0,stSpr) <br />
resitev==True ce je problem resljiv <br />
potem je sezPrireditev prireditev za izpolnitev resitve <br />
prireditev se nato v ustrezni obliki zapise v datoteko izhod.
