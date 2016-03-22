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

Pri tem je pomembno, da se tocke 4,5,6,7 smejo izvajati samno na
vec iteracij in ne na vsako saj bi to porabilo prevec casa.

Tocke je smiselno izvajati ob vejitvah, zato da imamo tudi minimalno
stevilo kopij CNFproblem.
