import numpy as np
import cv2 as cv

dimImgAfisare = (512, 512)

# Citire Imagine
imgInit = cv.imread('fisiere/antrenare/4_50.jpg')

cv.imshow('Imagine Initiala', cv.resize(imgInit, dimImgAfisare))
cv.waitKey(0)

# Aplicam Filtrul Median si Gaussian
img = imgInit.copy()
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.medianBlur(img, 7)
img = cv.GaussianBlur(img, (5, 5), 0)

cv.imshow('Imagine Filtrata', cv.resize(img, dimImgAfisare))
cv.waitKey(0)


# Eroziune + Identificare Muchii + Dilatare
img = cv.erode(img, np.ones((5, 5), np.uint8), iterations=2)
img = cv.Canny(img, 200, 400)
img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=2)

cv.imshow('Muchii Imagine', cv.resize(img, dimImgAfisare))
cv.waitKey(0)


# Identificare Contur Careu Joc
contururi, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

xMin = imgInit.shape[1] - 1
yMin = imgInit.shape[0] - 1
xMax = 0
yMax = 0
for contur in contururi:
    xStangaSus, yStangaSus, latime, inaltime = cv.boundingRect(contur)
    xMin = min(xMin, xStangaSus)
    yMin = min(yMin, yStangaSus)
    xMax = max(xMax, xStangaSus + latime)
    yMax = max(yMax, yStangaSus + inaltime)

# Decupam Careul
imgCareu = imgInit[yMin:yMax, xMin:xMax].copy()

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


