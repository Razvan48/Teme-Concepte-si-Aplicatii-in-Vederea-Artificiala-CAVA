import numpy as np
import cv2 as cv
import os
import shutil

import Utilitar


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
        fisiere = sorted(os.listdir(adresaDirectorImagini + '/'))

        if os.path.exists(adresaDirectorSabloane):
            shutil.rmtree(adresaDirectorSabloane)

        iPragProcent = 0.095
        jPragProcent = 0.095
        unghiMaximRotire = 3

        for fisier in fisiere:

            if fisier.endswith(extensieImagini):

                imgInit = cv.imread(f'{adresaDirectorImagini}/{fisier}')
                imgCareu = Utilitar.extrageCareuImagine(imgInit)

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

                imgSablonIntreg = imgCareu[int(iSablon * inaltimeSablon):int((iSablon + 1) * inaltimeSablon), int(jSablon * latimeSablon):int((jSablon + 1) * latimeSablon)].copy()

                for unghiRotit in range(-unghiMaximRotire, unghiMaximRotire + 1):

                    imgSablonIntregRotit = cv.warpAffine(imgSablonIntreg, cv.getRotationMatrix2D((imgSablonIntreg.shape[1] / 2, imgSablonIntreg.shape[0] / 2), unghiRotit, 1.0), (imgSablonIntreg.shape[1], imgSablonIntreg.shape[0]))

                    imgSablon = imgSablonIntregRotit[int(iPragProcent * imgSablonIntregRotit.shape[0]):int((1 - iPragProcent) * imgSablonIntregRotit.shape[0]), int(jPragProcent * imgSablonIntregRotit.shape[1]):int((1 - jPragProcent) * imgSablonIntregRotit.shape[1])].copy()

                    imgSablonPrelucrat = Utilitar.prelucreazaSablon(imgSablon)

                    if etichetaSablon not in self.colectiiSabloane:
                        self.colectiiSabloane[etichetaSablon] = []
                    self.colectiiSabloane[etichetaSablon].append(imgSablonPrelucrat)

                    os.makedirs(adresaDirectorSabloane + '/' + str(etichetaSablon), exist_ok=True)
                    cv.imwrite(adresaDirectorSabloane + '/' + str(etichetaSablon) + '/' + fisier[:fisier.rfind('.')] + '_' + str(unghiRotit + unghiMaximRotire) + extensieImagini, imgSablonPrelucrat)

                    print(f'Generat si incarcat sablon cu eticheta {etichetaSablon} din imaginea {fisier} cu unghiul {unghiRotit}')


        sabloaneSuplimentare = dict()
        sabloaneSuplimentare['03.jpg'] = []
        sabloaneSuplimentare['03.jpg'].append([(5, 4), 0])
        sabloaneSuplimentare['03.jpg'].append([(5, 5), 1])
        sabloaneSuplimentare['03.jpg'].append([(5, 6), 2])
        sabloaneSuplimentare['03.jpg'].append([(5, 7), 3])
        sabloaneSuplimentare['03.jpg'].append([(5, 8), 4])
        sabloaneSuplimentare['03.jpg'].append([(5, 9), 5])
        sabloaneSuplimentare['03.jpg'].append([(5, 10), 6])
        sabloaneSuplimentare['03.jpg'].append([(5, 11), 7])
        sabloaneSuplimentare['03.jpg'].append([(6, 4), 8])
        sabloaneSuplimentare['03.jpg'].append([(6, 5), 9])
        sabloaneSuplimentare['03.jpg'].append([(6, 6), 10])
        sabloaneSuplimentare['03.jpg'].append([(6, 7), 11])
        sabloaneSuplimentare['03.jpg'].append([(6, 8), 12])
        sabloaneSuplimentare['03.jpg'].append([(6, 9), 13])
        sabloaneSuplimentare['03.jpg'].append([(6, 10), 14])
        sabloaneSuplimentare['03.jpg'].append([(6, 11), 15])
        sabloaneSuplimentare['03.jpg'].append([(7, 4), 16])
        sabloaneSuplimentare['03.jpg'].append([(7, 5), 17])
        sabloaneSuplimentare['03.jpg'].append([(7, 6), 18])
        sabloaneSuplimentare['03.jpg'].append([(7, 7), 19])
        sabloaneSuplimentare['03.jpg'].append([(7, 8), 20])
        sabloaneSuplimentare['03.jpg'].append([(7, 9), 21])
        sabloaneSuplimentare['03.jpg'].append([(7, 10), 24])
        sabloaneSuplimentare['03.jpg'].append([(7, 11), 25])
        sabloaneSuplimentare['03.jpg'].append([(8, 4), 27])
        sabloaneSuplimentare['03.jpg'].append([(8, 5), 28])
        sabloaneSuplimentare['03.jpg'].append([(8, 6), 30])
        sabloaneSuplimentare['03.jpg'].append([(8, 7), 32])
        sabloaneSuplimentare['03.jpg'].append([(8, 8), 35])
        sabloaneSuplimentare['03.jpg'].append([(8, 9), 36])
        sabloaneSuplimentare['03.jpg'].append([(8, 10), 40])
        sabloaneSuplimentare['03.jpg'].append([(8, 11), 42])
        sabloaneSuplimentare['03.jpg'].append([(9, 4), 45])
        sabloaneSuplimentare['03.jpg'].append([(9, 5), 48])
        sabloaneSuplimentare['03.jpg'].append([(9, 6), 49])
        sabloaneSuplimentare['03.jpg'].append([(9, 7), 50])
        sabloaneSuplimentare['03.jpg'].append([(9, 8), 54])
        sabloaneSuplimentare['03.jpg'].append([(9, 9), 56])
        sabloaneSuplimentare['03.jpg'].append([(9, 10), 60])
        sabloaneSuplimentare['03.jpg'].append([(9, 11), 63])
        sabloaneSuplimentare['03.jpg'].append([(10, 4), 64])
        sabloaneSuplimentare['03.jpg'].append([(10, 5), 70])
        sabloaneSuplimentare['03.jpg'].append([(10, 6), 72])
        sabloaneSuplimentare['03.jpg'].append([(10, 7), 80])
        sabloaneSuplimentare['03.jpg'].append([(10, 8), 81])
        sabloaneSuplimentare['03.jpg'].append([(10, 9), 90])

        sabloaneSuplimentare['04.jpg'] = []
        sabloaneSuplimentare['04.jpg'].append([(0, 0), 0])
        sabloaneSuplimentare['04.jpg'].append([(0, 2), 1])
        sabloaneSuplimentare['04.jpg'].append([(0, 4), 2])
        sabloaneSuplimentare['04.jpg'].append([(0, 6), 3])
        sabloaneSuplimentare['04.jpg'].append([(0, 8), 4])
        sabloaneSuplimentare['04.jpg'].append([(0, 10), 5])
        sabloaneSuplimentare['04.jpg'].append([(0, 12), 6])
        sabloaneSuplimentare['04.jpg'].append([(2, 0), 7])
        sabloaneSuplimentare['04.jpg'].append([(2, 2), 8])
        sabloaneSuplimentare['04.jpg'].append([(2, 4), 9])
        sabloaneSuplimentare['04.jpg'].append([(2, 6), 10])
        sabloaneSuplimentare['04.jpg'].append([(2, 8), 11])
        sabloaneSuplimentare['04.jpg'].append([(2, 10), 12])
        sabloaneSuplimentare['04.jpg'].append([(2, 12), 13])
        sabloaneSuplimentare['04.jpg'].append([(4, 0), 14])
        sabloaneSuplimentare['04.jpg'].append([(4, 2), 15])
        sabloaneSuplimentare['04.jpg'].append([(4, 4), 16])
        sabloaneSuplimentare['04.jpg'].append([(4, 6), 17])
        sabloaneSuplimentare['04.jpg'].append([(4, 8), 18])
        sabloaneSuplimentare['04.jpg'].append([(4, 10), 19])
        sabloaneSuplimentare['04.jpg'].append([(4, 12), 20])
        sabloaneSuplimentare['04.jpg'].append([(6, 0), 21])
        sabloaneSuplimentare['04.jpg'].append([(6, 2), 24])
        sabloaneSuplimentare['04.jpg'].append([(6, 4), 25])
        sabloaneSuplimentare['04.jpg'].append([(6, 6), 27])
        sabloaneSuplimentare['04.jpg'].append([(6, 8), 28])
        sabloaneSuplimentare['04.jpg'].append([(6, 10), 30])
        sabloaneSuplimentare['04.jpg'].append([(6, 12), 32])
        sabloaneSuplimentare['04.jpg'].append([(8, 0), 35])
        sabloaneSuplimentare['04.jpg'].append([(8, 2), 36])
        sabloaneSuplimentare['04.jpg'].append([(8, 4), 40])
        sabloaneSuplimentare['04.jpg'].append([(8, 6), 42])
        sabloaneSuplimentare['04.jpg'].append([(8, 8), 45])
        sabloaneSuplimentare['04.jpg'].append([(8, 10), 48])
        sabloaneSuplimentare['04.jpg'].append([(8, 12), 49])
        sabloaneSuplimentare['04.jpg'].append([(10, 0), 50])
        sabloaneSuplimentare['04.jpg'].append([(10, 2), 54])
        sabloaneSuplimentare['04.jpg'].append([(10, 4), 56])
        sabloaneSuplimentare['04.jpg'].append([(10, 6), 60])
        sabloaneSuplimentare['04.jpg'].append([(10, 8), 63])
        sabloaneSuplimentare['04.jpg'].append([(10, 10), 64])
        sabloaneSuplimentare['04.jpg'].append([(10, 12), 70])
        sabloaneSuplimentare['04.jpg'].append([(12, 0), 72])
        sabloaneSuplimentare['04.jpg'].append([(12, 2), 80])
        sabloaneSuplimentare['04.jpg'].append([(12, 4), 81])
        sabloaneSuplimentare['04.jpg'].append([(12, 6), 90])


        adresaDirectorSabloaneSuplimentare = 'fisiere/imagini_auxiliare'
        indexImagine = 0
        # Adaugam sabloanele suplimentare
        for adresaFisierSabloane, infoSabloane in sabloaneSuplimentare.items():
            imgInit = cv.imread(adresaDirectorSabloaneSuplimentare + '/' + adresaFisierSabloane)
            imgCareu = Utilitar.extrageCareuImagine(imgInit)

            latimeSablon = imgCareu.shape[1] / 14
            inaltimeSablon = imgCareu.shape[0] / 14

            indexSablonAceeasiImagine = 0

            for sablon in infoSabloane:
                iSablon = sablon[0][0]
                jSablon = sablon[0][1]
                etichetaSablon = sablon[1]

                imgSablonIntreg = imgCareu[int(iSablon * inaltimeSablon):int((iSablon + 1) * inaltimeSablon), int(jSablon * latimeSablon):int((jSablon + 1) * latimeSablon)].copy()

                for unghiRotit in range(-unghiMaximRotire, unghiMaximRotire + 1):

                    imgSablonIntregRotit = cv.warpAffine(imgSablonIntreg, cv.getRotationMatrix2D((imgSablonIntreg.shape[1] / 2, imgSablonIntreg.shape[0] / 2), unghiRotit, 1.0), (imgSablonIntreg.shape[1], imgSablonIntreg.shape[0]))

                    imgSablon = imgSablonIntregRotit[int(iPragProcent * imgSablonIntregRotit.shape[0]):int((1 - iPragProcent) * imgSablonIntregRotit.shape[0]), int(jPragProcent * imgSablonIntregRotit.shape[1]):int((1 - jPragProcent) * imgSablonIntregRotit.shape[1])].copy()

                    imgSablonPrelucrat = Utilitar.prelucreazaSablon(imgSablon)

                    if etichetaSablon not in self.colectiiSabloane:
                        self.colectiiSabloane[etichetaSablon] = []
                    self.colectiiSabloane[etichetaSablon].append(imgSablonPrelucrat)

                    os.makedirs(adresaDirectorSabloane + '/' + str(etichetaSablon), exist_ok=True)
                    cv.imwrite(adresaDirectorSabloane + '/' + str(etichetaSablon) + '/' + 'extra' + '_' + str(indexImagine) + '_' + str(indexSablonAceeasiImagine) + '_' + str(unghiRotit + unghiMaximRotire) + extensieImagini, imgSablonPrelucrat)

                    print(f'Generat si incarcat sablon suplimentar cu eticheta {etichetaSablon} din imaginea {adresaFisierSabloane} cu unghiul {unghiRotit}')

                    indexSablonAceeasiImagine += 1

            indexImagine += 1




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


    def evalueazaImagine(self, img, sabloaneAcceptabile: set):
        imgPrelucrat = Utilitar.prelucreazaSablon(img)

        etichetaSolutie = -1
        distantaMinima = float('inf')

        for eticheta, sabloane in self.colectiiSabloane.items():

            if (eticheta not in self.pieseIncaFolosibile) or (eticheta not in sabloaneAcceptabile):
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





