import numpy as np
import cv2 as cv


def extrageCareuImagine(imgInit):
    latimeImplicita = 3072
    inaltimeImplicita = 4080

    imgInit = cv.resize(imgInit, (latimeImplicita, inaltimeImplicita))

    img = imgInit.copy()
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(img, 7)
    img = cv.GaussianBlur(img, (5, 5), 0)

    img = cv.erode(img, np.ones((5, 5), np.uint8), iterations=2)
    img = cv.Canny(img, 200, 400)
    img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=2)

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


    xMinImplicit = 873
    xMaxImplicit = 2333
    yMinImplicit = 1776
    yMaxImplicit = 3243
    pragExtragereCareuX = 25
    pragExtragereCareuY = 25
    if xMin > xMax or yMin > yMax or abs((xMax - xMin) - (xMaxImplicit - xMinImplicit)) > pragExtragereCareuX or abs((yMax - yMin) - (yMaxImplicit - yMinImplicit)) > pragExtragereCareuY:
        xMin = xMinImplicit
        xMax = xMaxImplicit
        yMin = yMinImplicit
        yMax = yMaxImplicit


    imgCareu = imgInit[yMin:yMax, xMin:xMax].copy()

    return imgCareu


def prelucreazaSablon(imgInit):
    #imgInit = cv.cvtColor(imgInit, cv.COLOR_BGR2GRAY)

    img = cv.medianBlur(imgInit, 7)
    img = cv.GaussianBlur(img, (5, 5), 0)

    #img = cv.erode(img, np.ones((5, 5), np.uint8), iterations=2)
    img = cv.Canny(img, 200, 400)
    #img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=2)

    #cv.imshow('Imagine Gradient Utilitar Sablon', img)
    #cv.waitKey(0)

    contururi, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contururi) > 0:
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

        imgSablonPrelucrat = imgInit[yMin:yMax, xMin:xMax].copy()
    else:
        imgSablonPrelucrat = imgInit.copy()

    #_, imgSablonPrelucrat = cv.threshold(imgSablonPrelucrat, 127, 255, cv.THRESH_BINARY)
    imgSablonPrelucrat = cv.resize(imgSablonPrelucrat, (64, 64))

    return imgSablonPrelucrat


