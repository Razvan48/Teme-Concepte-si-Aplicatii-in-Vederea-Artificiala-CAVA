import numpy as np
import cv2 as cv
import os
import shutil

import utilitar


class EvaluatorSabloane:


    def __init__(self,):
        self.colectiiSabloane = dict()
        self.pieseIncaFolosibile = dict()


    def reseteazaPieseIncaFolosibile(self):
        self.pieseIncaFolosibile = dict()

        self.pieseIncaFolosibile[0] = 1
        self.pieseIncaFolosibile[1] = 7
        self.pieseIncaFolosibile[2] = 7
        self.pieseIncaFolosibile[3] = 7
        self.pieseIncaFolosibile[4] = 7
        self.pieseIncaFolosibile[5] = 7
        self.pieseIncaFolosibile[6] = 7
        self.pieseIncaFolosibile[7] = 7
        self.pieseIncaFolosibile[8] = 7
        self.pieseIncaFolosibile[9] = 7
        self.pieseIncaFolosibile[10] = 7
        self.pieseIncaFolosibile[11] = 1
        self.pieseIncaFolosibile[12] = 1
        self.pieseIncaFolosibile[13] = 1
        self.pieseIncaFolosibile[14] = 1
        self.pieseIncaFolosibile[15] = 1
        self.pieseIncaFolosibile[16] = 1
        self.pieseIncaFolosibile[17] = 1
        self.pieseIncaFolosibile[18] = 1
        self.pieseIncaFolosibile[19] = 1
        self.pieseIncaFolosibile[20] = 1
        self.pieseIncaFolosibile[21] = 1
        self.pieseIncaFolosibile[24] = 1
        self.pieseIncaFolosibile[25] = 1
        self.pieseIncaFolosibile[27] = 1
        self.pieseIncaFolosibile[28] = 1
        self.pieseIncaFolosibile[30] = 1
        self.pieseIncaFolosibile[32] = 1
        self.pieseIncaFolosibile[35] = 1
        self.pieseIncaFolosibile[36] = 1
        self.pieseIncaFolosibile[40] = 1
        self.pieseIncaFolosibile[42] = 1
        self.pieseIncaFolosibile[45] = 1
        self.pieseIncaFolosibile[48] = 1
        self.pieseIncaFolosibile[49] = 1
        self.pieseIncaFolosibile[50] = 1
        self.pieseIncaFolosibile[54] = 1
        self.pieseIncaFolosibile[56] = 1
        self.pieseIncaFolosibile[60] = 1
        self.pieseIncaFolosibile[63] = 1
        self.pieseIncaFolosibile[64] = 1
        self.pieseIncaFolosibile[70] = 1
        self.pieseIncaFolosibile[72] = 1
        self.pieseIncaFolosibile[80] = 1
        self.pieseIncaFolosibile[81] = 1
        self.pieseIncaFolosibile[90] = 1


    def genereazaSiIncarcaSabloane(self, adresaDirectorImagini: str, extensieImagini: str, adresaDirectorSabloane: str):
        fisiere = sorted(os.listdir(adresaDirectorImagini))

        if os.path.exists(adresaDirectorSabloane):
            shutil.rmtree(adresaDirectorSabloane)

        for fisier in fisiere:

            if fisier.endswith(extensieImagini):

                imgInit = cv.imread(f'{adresaDirectorImagini}/{fisier}')
                imgCareu = utilitar.extrageCareuImagine(imgInit)

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

                imgSablonPrelucrat = utilitar.prelucreazaSablon(imgSablon)

                if etichetaSablon not in self.colectiiSabloane:
                    self.colectiiSabloane[etichetaSablon] = []
                self.colectiiSabloane[etichetaSablon].append(imgSablonPrelucrat)

                os.makedirs(adresaDirectorSabloane + '/' + str(etichetaSablon), exist_ok=True)
                cv.imwrite(adresaDirectorSabloane + '/' + str(etichetaSablon) + '/' + fisier, imgSablonPrelucrat)

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


    def __distantaImagini(self, img, sablon):
        #return np.mean((img - sablon) ** 2)
        return cv.norm(img, sablon, cv.NORM_L2)
        #return np.mean(np.abs(img - sablon))
        #_, valoareMaxima, _, _ = cv.minMaxLoc(cv.matchTemplate(img, sablon, cv.TM_CCOEFF_NORMED))
        #return -valoareMaxima


    def evalueazaImagine(self, img):
        imgPrelucrat = utilitar.prelucreazaSablon(img)

        etichetaSolutie = -1
        distantaMinima = float('inf')

        for eticheta, sabloane in self.colectiiSabloane.items():

            if eticheta not in self.pieseIncaFolosibile:
                continue

            distanceSablon = []
            for sablon in sabloane:
                distanceSablon.append(self.__distantaImagini(imgPrelucrat, sablon))

            distantaCurenta = np.mean(distanceSablon)

            if distantaCurenta < distantaMinima:
                distantaMinima = distantaCurenta
                etichetaSolutie = eticheta


        self.pieseIncaFolosibile[etichetaSolutie] -= 1
        if self.pieseIncaFolosibile[etichetaSolutie] == 0:
            del self.pieseIncaFolosibile[etichetaSolutie]
        return etichetaSolutie





