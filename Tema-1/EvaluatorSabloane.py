import numpy as np
import cv2 as cv
import os

import utilitar


class EvaluatorSabloane:


    def __init__(self, adresaDirectorImagini : str, extensieImagini : str):
        self.adresaDirectorImagini = adresaDirectorImagini
        self.extensieImagini = extensieImagini

        self.colectiiSabloane = dict()

        self._genereazaSabloane()


    def _genereazaSabloane(self):
        fisiere = sorted(os.listdir(self.adresaDirectorImagini))

        for fisier in fisiere:

            if fisier.endswith(self.extensieImagini):

                imgInit = cv.imread(f'{self.adresaDirectorImagini}/{fisier}')
                imgCareu = utilitar.extrageCareuImagine(imgInit)

                fisierSolutieImagine = open(self.adresaDirectorImagini + '/' + fisier[:fisier.rfind('.')] + '.txt', 'rt') # rt = read text

                continutFisierSolutieImagine = fisierSolutieImagine.readline()

                fisierSolutieImagine.close()

                pozitionareSablonInImagine = continutFisierSolutieImagine.split(' ')[0]
                if len(pozitionareSablonInImagine) == 2:
                    xSablon = int(pozitionareSablonInImagine[0]) - 1
                    ySablon = int(ord(pozitionareSablonInImagine[1]) - ord('A'))
                elif len(pozitionareSablonInImagine) == 3:
                    xSablon = int(pozitionareSablonInImagine[0:2]) - 1
                    ySablon = int(ord(pozitionareSablonInImagine[2]) - ord('A'))
                else:
                    print('Pozitionare sablon incorecta')
                    return

                etichetaSablon = int(continutFisierSolutieImagine.split(' ')[1])

                latimeSablon = imgCareu.shape[1] / 14
                inaltimeSablon = imgCareu.shape[0] / 14

                xPragProcent = 0.082
                yPragProcent = 0.082

                imgSablon = imgCareu[int((ySablon + yPragProcent) * inaltimeSablon):int((ySablon + 1 - yPragProcent) * inaltimeSablon), int((xSablon + xPragProcent) * latimeSablon):int((xSablon + 1 - xPragProcent) * latimeSablon)].copy()

                if etichetaSablon not in self.colectiiSabloane:
                    self.colectiiSabloane[etichetaSablon] = []
                self.colectiiSabloane[etichetaSablon].append(imgSablon)

                print(f'Incarcat sablon cu eticheta {etichetaSablon} din imaginea {fisier}')


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





