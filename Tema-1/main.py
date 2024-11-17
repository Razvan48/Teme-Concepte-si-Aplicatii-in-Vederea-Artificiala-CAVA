import numpy as np
import cv2 as cv

class Task_1:


    def __init__(self, adresaDirectorImagini : str, adresaImagineStart : str, nrJoc : int, nrImaginiPerJoc : int):
        self.adresaDirectorImagini = adresaDirectorImagini
        self.adresaImagineStart = adresaImagineStart
        self.nrJoc = nrJoc
        self.nrImaginiPerJoc = nrImaginiPerJoc
        self.dimImgAfisare = (512, 512)
        self.imaginiCareu = []


    def incarcaCareuImagine(self, nrImagine : int):
        if nrImagine == 0:
            imgInit = cv.imread(self.adresaImagineStart)
        elif nrImagine < 10:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_0{nrImagine}.jpg')
        else:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_{nrImagine}.jpg')

        img = imgInit.copy()
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.medianBlur(img, 7)
        img = cv.GaussianBlur(img, (5, 5), 0)

        img = cv.erode(img, np.ones((5, 5), np.uint8), iterations=2)
        img = cv.Canny(img, 200, 400)
        img = cv.dilate(img, np.ones((5, 5), np.uint8), iterations=2)

        # self.afiseazaImagine(img)

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

        # self.afiseazaImagine(imgCareu)

        self.imaginiCareu.append(imgCareu)


    def compara2Imagini(self, indexAnt : int, indexCrt : int):
        if indexAnt >= len(self.imaginiCareu) or indexCrt >= len(self.imaginiCareu):
            print('Nu sunt suficiente imagini')
            return

        # Copie ca sa putem modifica fara sa afectam imaginile originale
        imgAnt = self.imaginiCareu[indexAnt].copy()
        imgCrt = self.imaginiCareu[indexCrt].copy()

        latimeCelulaImgAnt = imgAnt.shape[1] / 14
        inaltimeCelulaImgAnt = imgAnt.shape[0] / 14
        latimeCelulaImgCrt = imgCrt.shape[1] / 14
        inaltimeCelulaImgCrt = imgCrt.shape[0] / 14

        # Doar pentru debug
        xStangaSusSol = -1.0
        yStangaSusSol = -1.0
        latimeSol = -1.0
        inaltimeSol = -1.0

        xPragProcent = 0.082
        yPragProcent = 0.082

        difMaxima = -1.0
        iMaxim = -1
        jMaxim = -1

        yImgAnt = 0.0
        yImgCrt = 0.0
        for i in range(14):
            xImgAnt = 0.0
            xImgCrt = 0.0

            for j in range(14):
                celulaImgAnt = imgAnt[int(yImgAnt):int(yImgAnt + inaltimeCelulaImgAnt), int(xImgAnt):int(xImgAnt + latimeCelulaImgAnt)].copy()
                celulaImgCrt = imgCrt[int(yImgCrt):int(yImgCrt + inaltimeCelulaImgCrt), int(xImgCrt):int(xImgCrt + latimeCelulaImgCrt)].copy()

                celulaImgAnt = cv.resize(celulaImgAnt, (int(latimeCelulaImgCrt), int(inaltimeCelulaImgCrt)))
                celulaImgAntFaraContur = celulaImgAnt[int(yPragProcent * inaltimeCelulaImgCrt):int((1.0 - yPragProcent) * inaltimeCelulaImgCrt), int(xPragProcent * latimeCelulaImgCrt):int((1.0 - xPragProcent) * latimeCelulaImgCrt)].copy()
                celulaImgCrtFaraContur = celulaImgCrt[int(yPragProcent * inaltimeCelulaImgCrt):int((1.0 - yPragProcent) * inaltimeCelulaImgCrt), int(xPragProcent * latimeCelulaImgCrt):int((1.0 - xPragProcent) * latimeCelulaImgCrt)].copy()
                difCurenta = cv.norm(celulaImgAntFaraContur, celulaImgCrtFaraContur, cv.NORM_L2)

                if difCurenta > difMaxima:
                    difMaxima = difCurenta
                    iMaxim = i
                    jMaxim = j

                    # Debug
                    xStangaSusSol = xImgCrt
                    yStangaSusSol = yImgCrt
                    latimeSol = latimeCelulaImgCrt
                    inaltimeSol = inaltimeCelulaImgCrt

                xImgAnt += latimeCelulaImgAnt
                xImgCrt += latimeCelulaImgCrt

            yImgAnt += inaltimeCelulaImgAnt
            yImgCrt += inaltimeCelulaImgCrt


        # Debug pentru a vedea care este celula care a dat cea mai mare diferenta (incluzand si procentul de micsorare)
        #cv.rectangle(imgAnt, (int(xStangaSusSol + xPragProcent * latimeSol), int(yStangaSusSol + yPragProcent * inaltimeSol)), (int(xStangaSusSol + (1.0 - xPragProcent) * latimeSol), int(yStangaSusSol + (1.0 - yPragProcent) * inaltimeSol)), (0, 0, 255), -1)
        #cv.rectangle(imgCrt, (int(xStangaSusSol + xPragProcent * latimeSol), int(yStangaSusSol + yPragProcent * inaltimeSol)), (int(xStangaSusSol + (1.0 - xPragProcent) * latimeSol), int(yStangaSusSol + (1.0 - yPragProcent) * inaltimeSol)), (0, 0, 255), -1)
        # self.afiseazaImagini([imgAnt, imgCrt])


        # iMaxim = rand, jMaxim = coloana
        return ''.join([str(1 + iMaxim), str(chr(jMaxim + ord('A')))])


    def afiseazaImagine(self, img):
        cv.imshow('Imagine', cv.resize(img, self.dimImgAfisare))
        cv.moveWindow("Imagine", 200, 200)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def afiseazaImagini(self, imagini : list):
        imaginiRedim = [cv.resize(img, self.dimImgAfisare) for img in imagini]
        cv.imshow('Imagine', np.hstack(imaginiRedim))
        cv.moveWindow("Imagine", 200, 200)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def ruleaza(self):
        self.incarcaCareuImagine(0)

        for i in range(1, self.nrImaginiPerJoc + 1):
            self.incarcaCareuImagine(i)

        for i in range(1, len(self.imaginiCareu)):
            print(f'Imaginea {i} - {self.compara2Imagini(i - 1, i)}')
            self.afiseazaImagini(self.imaginiCareu[i - 1:i + 1])



task1 = Task_1('fisiere/antrenare/', 'fisiere/imagini_auxiliare/01.jpg', 1, 10)
task1.ruleaza()


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


