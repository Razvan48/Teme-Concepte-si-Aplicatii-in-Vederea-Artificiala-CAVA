import Utilitar
import Model


Utilitar.genereazaHiperparametriFereastraGlisanta('fisiere/antrenare', 'fisiere/iesire/hiperparametrii')

Utilitar.genereazaExempleNegative('fisiere/antrenare', 'fisiere/iesire/hiperparametrii', 'fisiere/iesire/exempleNegative', 10)



# x-ul din adnotari e latimea imaginii, y-ul e inaltimea imaginii, iar originea este in coltul stanga sus

# TODO:

# in clasa model: metode de salvat descriptorii si ponderile modelului antrenat + posibilitatea de a incarca descriptorii si ponderile
# de adaugat in constructorul clasei model posibilitatea de a mentiona ce tip de model de invatare sa fie folosit (svm, rnc, etc) (de schimbat si in functia de antrenare)
# de stabilit unde salvez predictiile + descriptorii + ponderile

# descriptori hog/sift (de vazut)




# de facut documentatia (txt-ul) (momentan in documentatie trebuie scris doar ce module sunt necesare (nici asta nu e scris momentan))
# de facut latex-ul
