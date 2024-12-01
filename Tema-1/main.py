import Tema_1

import numpy as np
import cv2 as cv
import sys

print('Versiune Python: ', sys.version)
print('Versiune Numpy: ', np.__version__)
print('Versiune OpenCV-Python: ', cv.__version__)

tema_1 = Tema_1.Tema_1('fisiere/antrenare', 'fisiere/imagini_auxiliare/01.jpg', 4, 50, 'fisiere/iesire', 'fisiere/sabloane', True)
tema_1.ruleaza()


# TODO:


# de testat si restul jocurilor (inca 150 de imagini)
# de verificat ca structurile pentru celule deja ocupate si piese deja folosite se populeaza corect









