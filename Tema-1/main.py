import numpy as np
import cv2 as cv

import Task_1
import Task_2
import Task_3


task1 = Task_1.Task_1('fisiere/antrenare/', 'fisiere/imagini_auxiliare/01.jpg', 1, 50, 'fisiere/sabloane/', False)
task1.ruleaza()

# TODO:
# Task1 mai greseste celula nou pusa uneori (grilajul nu e gresit niciodata)

# de testat si restul jocurilor (inca 150 de imagini)

# de jucat putin mai mult la metoda cu prelucrarea sablonului (de exemplu de facut imaginea ori alb ori negru, fara gri)

# mai confunda 5 cu 13 de exemplu
# 6 cu 0
# 5 cu 80
# 10 confundat cu 18




'''
# Afisam Careu
cv.imshow('Careu', cv.resize(imgCareu, dimImgAfisare))
cv.waitKey(0)

# Identificam Coordonatele Celulelor din Careu
img = imgCareu.copy()
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.medianBlur(img, 7)
img = cv.GaussianBlur(img, (5, 5), 0)

img = cv.erode(img, np.ones((7, 7), np.uint8), iterations=1)
img = cv.Canny(img, 50, 100)
img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=1)

cv.imshow('Muchii Careu', cv.resize(img, dimImgAfisare))
cv.waitKey(0)

# Extragem Coordonatele Celulelor
imgCelule = np.zeros(img.shape, np.uint8)
contururi, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


for contur in contururi:
    arie = cv.contourArea(contur)
    if arie > 3250:
        xStangaSus, yStangaSus, latime, inaltime = cv.boundingRect(contur)
        # print(xStangaSus, yStangaSus, latime, inaltime)
        # cv.rectangle(imgCelule, (xStangaSus, yStangaSus), (xStangaSus + latime, yStangaSus + inaltime), (255, 255, 255), 10)
        for punct in contur:
             xPunct, yPunct = punct[0]
             cv.circle(imgCelule, (xPunct, yPunct), 3, (255, 255, 255), -1)

cv.imshow('Celule Careu', cv.resize(imgCelule, dimImgAfisare))
cv.waitKey(0)

cv.imshow('Celule Careu', cv.resize(imgCelule, dimImgAfisare))
cv.waitKey(0)

img = imgCareu.copy()
dimXCelula = int(imgCelule.shape[1] / 14)
dimYCelula = int(imgCelule.shape[0] / 14)

for i in range(15):
    for j in range(15):
        xStangaSus = i * dimXCelula
        yStangaSus = j * dimYCelula
        cv.circle(img, (xStangaSus, yStangaSus), 10, (0, 255, 0), -1)

cv.imshow('Celule Careu', cv.resize(img, dimImgAfisare))
cv.waitKey(0)


cv.destroyAllWindows()
'''


