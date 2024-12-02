import Tema_1

import numpy as np
import cv2 as cv
import sys

print('Versiune Python: ', sys.version)
print('Versiune Numpy: ', np.__version__)
print('Versiune OpenCV-Python: ', cv.__version__)

tema_1 = Tema_1.Tema_1('fisiere/antrenare', 'fisiere/imagini_auxiliare/01.jpg', 5, 50, 'fisiere/iesire', 'fisiere/sabloane', True)
tema_1.ruleaza()


# TODO:

# nu stiu daca merita, dar cand construim dataset-ul de templates am putea lua din imagine fiecare numar, nu doar cel nou aparut
# (ca poate apar mici diferente de luminozitate, etc.)

# de completat mod utilizare/documentatie in readme

# de verificat pdf-ul cu documentatia
# de adaugat pdf-ul cu documentatia in repository

# de rotit cu mai putine grade imaginile? (2 in loc de 3 de exemplu)

# de testat inclusiv testul 5
# de testat si restul jocurilor (inca 150 de imagini)
# de verificat ca structurile pentru celule deja ocupate si piese deja folosite se populeaza corect









