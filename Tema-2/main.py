import Utilitar

import SVMHogModel
import CNNModel
import YOLOModel


#Utilitar.genereazaHiperparametriFereastraGlisanta('fisiere/antrenare', 'fisiere/iesire/hiperparametrii')
#Utilitar.genereazaExempleNegative('fisiere/antrenare', 'fisiere/iesire/hiperparametrii', 'fisiere/iesire/exempleNegative', 10000)

# SVM HOG Model

#svmHogModel = SVMHogModel.SVMHogModel('unknown', 'fisiere/iesire/hiperparametrii')
#svmHogModel.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#svmHogModel.testeaza('fisiere/validare/validare', 'fisiere/iesire/testare')

# CNN Model

#cnnModel = CNNModel.CNNModel('unknown', 'fisiere/iesire/hiperparametrii')
#cnnModel.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

#cnnModel.testeaza('fisiere/validare/validare', 'fisiere/iesire/testare')

# YOLO Model

yoloModel = YOLOModel.YOLOModel('unknown')
yoloModel.antreneaza('fisiere/antrenare', 'fisiere/iesire/exempleNegative')

yoloModel.testeaza('fisiere/validare/validare', 'fisiere/iesire/testare')



# x-ul din adnotari e latimea imaginii, y-ul e inaltimea imaginii, iar originea este in coltul stanga sus

# De incercat:

# micsorare numar hiperparametrii
# de revenit la pragurile de dinainte la iou

# TODO:

# de revazut tot codul daca e ok peste tot

# in clasa model: metode de salvat descriptorii si ponderile modelului antrenat + posibilitatea de a incarca descriptorii si ponderile
# de stabilit unde salvez predictiile + descriptorii + ponderile

# graficul precision-recall


# de facut documentatia (txt-ul) (momentan in documentatie trebuie scris doar ce module sunt necesare (nici asta nu e scris momentan))
# de facut latex-ul
