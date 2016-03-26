# SATsolverLVR
SATsolverLVR resi problem logicne izpolnjivosti

### Osnovni sat solver
##### Uporablja:
1) Unit clause (poisciNajmanjsoNepraznoMnozico)
2) Pure (poisciNajboljPureElement)
3) Pametno kopiranje strukture, samo kadar se veja

##### Mozne izboljsave:
4) Odstrani prazne mnozice in preindeksiraj
5) Odstrani podvojene mnozice (glej 4.)
6) Poisci razpadni element (nato razdeli problem na vec delov)
7) Poisci razpadno mnozico (nato razdeli problem na vec delov)

Pri tem je pomembno, da se tocke 4,5,6,7 smejo izvajati samno na <br />
vec iteracij in ne na vsako saj bi to porabilo prevec casa. <br />

Tocke je smiselno izvajati ob vejitvah, zato da imamo tudi minimalno <br />
stevilo kopij CNFproblem. <br />

### Navodila za uporabo: 
##### SATsolverDimacs
SATsolverDimacs(vhod,izhod="") <br />
Kot vhod podaj datoteko v Dimacs obliki, izhod bo resitev. <br />
Delovanje: <br />
Prebere datoteko podano kot vhod in jo pretvori v CNFproblem. <br />
resitev=solveSat(True,problemCNF,sezPrireditev,0,stSpr) <br />
resitev==True ce je problem resljiv <br />
potem je sezPrireditev prireditev za izpolnitev resitve <br />
prireditev se nato v ustrezni obliki zapise v datoteko izhod. <br />

##### CNFproblem
CNFproblem je struktura za zapis problema v CNF obliki. <br />
Zgrajena je iz treh seznamov in funkcij na le teh. <br />
self.sezAnd <br />
1. je problem zapisan v CNF obliki <br />
2. self.sezAnd sestavljajo mnozice katerih elementi so vezani z or <br />
3. med temi mnozicami pa imamo logicni veznik and <br />
self.lokacije... <br />
1. so lokacije elementov v self.sezAnd <br />
2. primer self.lokacijeNeg=[{},{4,77},{5}] <br />
3. pomeni da se -1 pojavi v 4tem in 77tem stavku, <br />
4. -2 pa v 5tem stavku (to je 5ti mnozici seznama). <br />
5. Prva mnozica je vedno prazna sej elementa 0 ni <br />

##### solveSat
Za testiranje ucinkovitosti algoritma je treba testirati to funkcijo, <br />
saj je tu problem ze v ustrezni obliki (za kar se porabi nekaj casa) <br />
in ta funkcija ne pise na disk <br />

### Popravljeni SAT solver
Je enak kot SAT solver razen: <br />
1. namesto solveSat imamo funkcijo resiSATwhile <br />
   ta resi problem namesto z uporabo rekurzije z while zanko <br />
   tako ne dobimo errora zaradi globine rekurzije <br />
2. smiselno so preimenovani nekateri izrazi <br />
   to je: izjva je spremenljivka s predznakom +- <br />
   tako izjava (-7) predstavlja spremenljivko 7 nastavljeno na vrednost False <br />
3. odstranjena je napaka pri najbolj pure (prej to ni ustrezno delovalo) <br />
4. resitev se kot seznam hrani v samem problemuCNF (in ne zunaj v SATsolverju)
   to je sicer prostorsko zahtevneje vendar bolj pregledno

##### Otezi resitev problema
Je program, ki za dan problem izracuna ekvivalenten problem v DIMACS obliki, <br />
ki pa ga je veliko tezje resiti. <br />

Tako h_sudoku2.txt predstavlja hudobni saduku, ki je tezje resljiv. <br />

Izbrani problem je h_sudoku2.txt <br />
