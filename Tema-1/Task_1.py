import numpy as np
import cv2 as cv

import EvaluatorSabloane
import utilitar


class Task_1:


    def __init__(self, adresaDirectorImagini : str, adresaImagineStart : str, nrJoc : int, nrImaginiPerJoc : int):
        self.adresaDirectorImagini = adresaDirectorImagini
        self.adresaImagineStart = adresaImagineStart
        self.nrJoc = nrJoc
        self.nrImaginiPerJoc = nrImaginiPerJoc

        self.evaluatorSabloane = EvaluatorSabloane.EvaluatorSabloane(adresaDirectorImagini, '.jpg')

        self.dimImgAfisare = (512, 512)
        self.imaginiCareu = []


    def incarcaCareuImagine(self, nrImagine : int):
        if nrImagine == 0:
            imgInit = cv.imread(self.adresaImagineStart)
        elif nrImagine < 10:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_0{nrImagine}.jpg')
        else:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_{nrImagine}.jpg')

        imgCareu = utilitar.extrageCareuImagine(imgInit)

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

        # Debug
        xStangaSusSol = -1.0
        yStangaSusSol = -1.0
        latimeSol = -1.0
        inaltimeSol = -1.0

        xPragProcent = 0.082
        yPragProcent = 0.082

        difMaxima = -1.0
        iMaxim = -1
        jMaxim = -1
        imgCelulaMaximaFaraContur = None

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
                    imgCelulaMaximaFaraContur = celulaImgCrtFaraContur

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
        #self.afiseazaImagini([imgAnt, imgCrt])


        # iMaxim = rand, jMaxim = coloana
        return str(1 + iMaxim) + str(chr(jMaxim + ord('A'))) + ' ' + str(self.evaluatorSabloane.evalueazaImagine(imgCelulaMaximaFaraContur))


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


