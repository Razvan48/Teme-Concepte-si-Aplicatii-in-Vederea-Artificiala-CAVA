import Utilitar

import SVMHogModel
import CNNModel
import ModelPreAntrenat


#Utilitar.genereazaHiperparametriFereastraGlisanta('fisiere/antrenare', 'fisiere/iesire/hiperparametrii')
#Utilitar.genereazaExempleNegative('fisiere/antrenare', 'fisiere/iesire/hiperparametrii', 'fisiere/iesire/exempleNegative', 20000)

# SVM HOG Model

#svmHogModel = SVMHogModel.SVMHogModel('unknown', 'fisiere/iesire/hiperparametrii')
#svmHogModel.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#svmHogModel.testeaza('fisiere/validare/validare', 'fisiere/iesire/testare')

# CNN Model

cnnModelUnknown = CNNModel.CNNModel('unknown', 'fisiere/iesire/hiperparametrii')
cnnModelUnknown.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

cnnModelUnknown.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

cnnModelUnknown.salveazaModel('fisiere/iesire/modele/CNNModel')

# CNN doar Dad

#cnnModelDad = CNNModel.CNNModel('dad', 'fisiere/iesire/hiperparametrii')
#cnnModelDad.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#cnnModelDad.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar DeeDee

#cnnModelDeeDee = CNNModel.CNNModel('deedee', 'fisiere/iesire/hiperparametrii')
#cnnModelDeeDee.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#cnnModelDeeDee.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar Dexter

#cnnModelDexter = CNNModel.CNNModel('dexter', 'fisiere/iesire/hiperparametrii')
#cnnModelDexter.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#cnnModelDexter.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar Mom

#cnnModelMom = CNNModel.CNNModel('mom', 'fisiere/iesire/hiperparametrii')
#cnnModelMom.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#cnnModelMom.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# Model Pre Antrenat

#modelPreAntrenat = ModelPreAntrenat.ModelPreAntrenat('unknown', 'fisiere/iesire/hiperparametrii')
#modelPreAntrenat.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#modelPreAntrenat.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')



# x-ul din adnotari e latimea imaginii, y-ul e inaltimea imaginii, iar originea este in coltul stanga sus

# TODO:

# de revazut tot codul daca e ok peste tot


# de facut documentatia (txt-ul) (momentan in documentatie trebuie scris doar ce module sunt necesare (nici asta nu e scris momentan))
# de facut latex-ul
