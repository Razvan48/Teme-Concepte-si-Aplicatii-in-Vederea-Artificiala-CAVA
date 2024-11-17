import numpy as np
import cv2 as cv
import os

import utilitar


class EvaluatorSabloane:


    def __init__(self,):
        self.colectiiSabloane = dict()


    def genereazaSiIncarcaSabloane(self, adresaDirectorImagini: str, extensieImagini: str, adresaDirectorSabloane: str):
        fisiere = sorted(os.listdir(adresaDirectorImagini))

        for fisier in fisiere:

            if fisier.endswith(extensieImagini):

                imgInit = cv.imread(f'{adresaDirectorImagini}/{fisier}')
                imgCareu = utilitar.extrageCareuImagine(imgInit)

                cv.imshow('Imagine', cv.resize(imgCareu, (512, 512)))
                cv.waitKey(0)

                fisierSolutieImagine = open(adresaDirectorImagini + '/' + fisier[:fisier.rfind('.')] + '.txt', 'rt') # rt = read text

                continutFisierSolutieImagine = fisierSolutieImagine.readline()

                fisierSolutieImagine.close()

                pozitionareSablonInImagine = continutFisierSolutieImagine.split(' ')[0]
                if len(pozitionareSablonInImagine) == 2:
                    iSablon = int(pozitionareSablonInImagine[0]) - 1
                    jSablon = int(ord(pozitionareSablonInImagine[1]) - ord('A'))
                elif len(pozitionareSablonInImagine) == 3:
                    iSablon = int(pozitionareSablonInImagine[0:2]) - 1
                    jSablon = int(ord(pozitionareSablonInImagine[2]) - ord('A'))
                else:
                    print('Pozitionare sablon incorecta')
                    return

                etichetaSablon = int(continutFisierSolutieImagine.split(' ')[1])

                latimeSablon = imgCareu.shape[1] / 14
                inaltimeSablon = imgCareu.shape[0] / 14

                iPragProcent = 0.082
                jPragProcent = 0.082

                imgSablon = imgCareu[int((iSablon + iPragProcent) * inaltimeSablon):int((iSablon + 1 - iPragProcent) * inaltimeSablon), int((jSablon + jPragProcent) * latimeSablon):int((jSablon + 1 - jPragProcent) * latimeSablon)].copy()

                if etichetaSablon not in self.colectiiSabloane:
                    self.colectiiSabloane[etichetaSablon] = []
                self.colectiiSabloane[etichetaSablon].append(imgSablon)

                print(iSablon, jSablon)
                cv.imshow('Sablon', cv.resize(imgSablon, (512, 512)))
                cv.waitKey(0)

                os.makedirs(adresaDirectorSabloane + '/' + str(etichetaSablon), exist_ok=True)
                cv.imwrite(adresaDirectorSabloane + '/' + str(etichetaSablon) + '/' + fisier, imgSablon)

                print(f'Generat si incarcat sablon cu eticheta {etichetaSablon} din imaginea {fisier}')


    def incarcaSabloane(self, adresaDirectorSabloane: str):
        self.colectiiSabloane = dict()
        etichete = sorted(os.listdir(adresaDirectorSabloane))

        for eticheta in etichete:
            sabloane = sorted(os.listdir(adresaDirectorSabloane + '/' + eticheta))

            for sablon in sabloane:
                imgSablon = cv.imread(adresaDirectorSabloane + '/' + eticheta + '/' + sablon)

                if int(eticheta) not in self.colectiiSabloane:
                    self.colectiiSabloane[int(eticheta)] = []
                self.colectiiSabloane[int(eticheta)].append(imgSablon)

                print(f'Incarcat sablon cu eticheta {eticheta} din imaginea {sablon}')


    def _distantaImagini(self, img, sablon):
        sablon = cv.resize(sablon, (img.shape[1], img.shape[0]))
        return np.mean(np.abs(img - sablon))


    def evalueazaImagine(self, img):
        etichetaSolutie = -1
        distantaMinima = float('inf')

        for eticheta, sabloane in self.colectiiSabloane.items():
            distanceSablon = []
            for sablon in sabloane:
                distanceSablon.append(self._distantaImagini(img, sablon))

            distantaCurenta = np.mean(distanceSablon)

            if distantaCurenta < distantaMinima:
                distantaMinima = distantaCurenta
                etichetaSolutie = eticheta

        return etichetaSolutie





