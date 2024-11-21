import numpy as np
import cv2 as cv

import Task_1
import Task_2
import Task_3


task1 = Task_1.Task_1('fisiere/antrenare/', 'fisiere/imagini_auxiliare/01.jpg', 1, 50, 'fisiere/sabloane/', False)
task1.ruleaza()

# TODO:
# Task1 mai greseste celula nou pusa uneori (grilajul nu e gresit niciodata) (pare sa o greseasca cand e ft sus celula respectiva)

# de testat si restul jocurilor (inca 150 de imagini)

# de jucat putin mai mult la metoda cu prelucrarea sablonului (de exemplu de facut imaginea ori alb ori negru, fara gri)



