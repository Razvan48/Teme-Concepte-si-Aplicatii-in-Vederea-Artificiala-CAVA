import Utilitar

import CNNModel


# CNN Model

cnnModelUnknown = CNNModel.CNNModel('unknown', 'fisiere/iesire/hiperparametrii')

#cnnModelUnknown.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegativeExtinse')
#cnnModelUnknown.salveazaModel('fisiere/iesire/modele/CNNModel')

cnnModelUnknown.incarcaModel('fisiere/iesire/modele/CNNModel/unknown_CNNModel_2025_1_20_0_4_49.h5')

cnnModelUnknown.testeaza('fisiere/testare', 'fisiere/iesire')

# CNN doar Dad

cnnModelDad = CNNModel.CNNModel('dad', 'fisiere/iesire/hiperparametrii')

#cnnModelDad.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegativeOriginal')
#cnnModelDad.salveazaModel('fisiere/iesire/modele/CNNModel')

cnnModelDad.incarcaModel('fisiere/iesire/modele/CNNModel/dad_CNNModel_2025_1_18_0_20_2.h5')

cnnModelDad.testeaza('fisiere/testare', 'fisiere/iesire')

# CNN doar DeeDee

cnnModelDeeDee = CNNModel.CNNModel('deedee', 'fisiere/iesire/hiperparametrii')

#cnnModelDeeDee.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegativeOriginal')
#cnnModelDeeDee.salveazaModel('fisiere/iesire/modele/CNNModel')

cnnModelDeeDee.incarcaModel('fisiere/iesire/modele/CNNModel/deedee_CNNModel_2025_1_18_18_56_49.h5')

cnnModelDeeDee.testeaza('fisiere/testare', 'fisiere/iesire')

# CNN doar Dexter

cnnModelDexter = CNNModel.CNNModel('dexter', 'fisiere/iesire/hiperparametrii')

#cnnModelDexter.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegativeOriginal')
#cnnModelDexter.salveazaModel('fisiere/iesire/modele/CNNModel')

cnnModelDexter.incarcaModel('fisiere/iesire/modele/CNNModel/dexter_CNNModel_2025_1_18_19_20_29.h5')

cnnModelDexter.testeaza('fisiere/testare', 'fisiere/iesire')

# CNN doar Mom

cnnModelMom = CNNModel.CNNModel('mom', 'fisiere/iesire/hiperparametrii')

#cnnModelMom.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegativeExtinse')
#cnnModelMom.salveazaModel('fisiere/iesire/modele/CNNModel')

cnnModelMom.incarcaModel('fisiere/iesire/modele/CNNModel/mom_CNNModel_2025_1_20_22_15_39.h5')

cnnModelMom.testeaza('fisiere/testare', 'fisiere/iesire')


