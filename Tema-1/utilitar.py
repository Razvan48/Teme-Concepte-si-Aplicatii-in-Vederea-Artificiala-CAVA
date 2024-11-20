import numpy as np
import cv2 as cv


def extrageCareuImagine(imgInit):
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

    imgCareu = imgInit[yMin:yMax, xMin:xMax].copy()

    return imgCareu


def prelucreazaSablon(imgInit):
    imgInitGray = cv.cvtColor(imgInit, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(imgInitGray, 7)
    img = cv.GaussianBlur(img, (5, 5), 0)

    #img = cv.erode(img, np.ones((5, 5), np.uint8), iterations=2)
    img = cv.Canny(img, 200, 400)
    #img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=2)

    #cv.imshow('Imagine Gradient Utilitar Sablon', img)
    #cv.waitKey(0)

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

    imgSablonPrelucrat = imgInitGray[yMin:yMax, xMin:xMax].copy()
    imgSablonPrelucrat = cv.resize(imgSablonPrelucrat, (16, 16))

    return imgSablonPrelucrat


