import copy
import os
import sklearn.svm as svm
import skimage.feature as feature
import numpy as np
import cv2 as cv

import Utilitar



class Model:


    def __init__(self, numePersonaj: str, adresaHiperparametrii: str): # numePersonaj trebuie sa fie 'unknown' in cazul task-ului 1
        self.numePersonaj = numePersonaj
        self.adresaHiperparametrii = adresaHiperparametrii

        self.pixeliPerCelula = (8, 8)
        self.celulePerBloc = (2, 2)
        self.celulePerImagine = (12, 12)

        self.dimensiuneImagine = (self.pixeliPerCelula[0] * self.celulePerImagine[0], self.pixeliPerCelula[1] * self.celulePerImagine[1])

        self.parametriiRegularizare = [(10 ** x) for x in range(-6, 0)]

        self.modelInvatare = None
        self.descriptoriPozitivi = []
        self.descriptoriNegativi = []

        self.PRAG_INTERSECTION_OVER_UNION = 0.3
        self.PROCENT_SALT_FEREASTRA_GLISANTA = 0.2
        self.PRAG_PREDICTIE_POZITIVA_SVM = 0.0

        self.aspectRatiosUtilizabili = set()
        fisierAspectRatios = open(self.adresaHiperparametrii + '/' + self.numePersonaj + '_aspectRatiosClustered.txt', 'r')
        for linie in fisierAspectRatios:
            self.aspectRatiosUtilizabili.add(float(linie))
        fisierAspectRatios.close()

        self.inaltimiFereastraUtilizabile = set()
        fisierInaltimiFereastra = open(self.adresaHiperparametrii + '/' + self.numePersonaj + '_inaltimiFereastraClustered.txt', 'r')
        for linie in fisierInaltimiFereastra:
            self.inaltimiFereastraUtilizabile.add(float(linie))
        fisierInaltimiFereastra.close()

        # aici mai pot adauga valori hardcodate pentru aspectRatios si inaltimiFereastra



    def antreneaza(self, adresaAntrenareExemplePozitive: str, adresaAntrenareExempleNegative: str):
        numePersonaje = ['dad', 'deedee', 'dexter', 'mom'] # 'unknown' nu trebuie inclus aici

        # exemple pozitive
        for numePersonaj in numePersonaje:
            if self.numePersonaj == numePersonaj or self.numePersonaj == 'unknown': # self.numePersonaj si numePersonaj nu sunt aceleasi mereu

                fisierAdnotari = open(adresaAntrenareExemplePozitive + '/' + numePersonaj + '_annotations.txt', 'r')
                zoneDeInteres = dict()

                for linie in fisierAdnotari:
                    cuvinte = linie.split(' ')

                    # elimina \n
                    if cuvinte[-1][-1] == '\n':
                        cuvinte[-1] = cuvinte[-1][:-1]

                    if cuvinte[5] == numePersonaj:
                        if cuvinte[0] not in zoneDeInteres:
                            zoneDeInteres[cuvinte[0]] = []

                        xMin = int(cuvinte[1])
                        yMin = int(cuvinte[2])
                        xMax = int(cuvinte[3])
                        yMax = int(cuvinte[4])

                        zoneDeInteres[cuvinte[0]].append((xMin, yMin, xMax, yMax))

                fisierAdnotari.close()

                for fisierImagine in os.listdir(adresaAntrenareExemplePozitive + '/' + numePersonaj):
                    print('Antrenare Exemple Pozitive: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    imagineOriginala = cv.imread(adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)
                    imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriPozitivi.append(descriptori.flatten())

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.fliplr(imagineDeInteres), self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriPozitivi.append(descriptori.flatten())

        self.descriptoriPozitivi = np.array(self.descriptoriPozitivi)

        # exemple negative
        for fisierImagine in os.listdir(adresaAntrenareExempleNegative):
            print('Antrenare Exemple Negative: ', adresaAntrenareExempleNegative + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaAntrenareExempleNegative + '/' + fisierImagine)
            imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

            imagine = cv.resize(imagineOriginala, self.dimensiuneImagine)
            descriptori = feature.hog(imagine, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataOrizontal = cv.resize(np.fliplr(imagineOriginala), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataOrizontal, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataVertical = cv.resize(np.flipud(imagineOriginala), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataVertical, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataVerticalOrizontal = cv.resize(np.flipud(np.fliplr(imagineOriginala)), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataVerticalOrizontal, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

        self.descriptoriNegativi = np.array(self.descriptoriNegativi)


        # antrenare # TODO: de testat cu alte modele de invatare

        acurateteMaxima = -1.0

        for parametruRegularizare in self.parametriiRegularizare:

            modelInvatare = svm.LinearSVC(C=parametruRegularizare)
            totiDescriptorii = np.concatenate((self.descriptoriPozitivi, self.descriptoriNegativi), axis=0)
            toateEtichetele = np.concatenate((np.ones(self.descriptoriPozitivi.shape[0]), np.zeros(self.descriptoriNegativi.shape[0])))
            modelInvatare.fit(totiDescriptorii, toateEtichetele)

            acurateteCurenta = modelInvatare.score(totiDescriptorii, toateEtichetele)
            if acurateteCurenta > acurateteMaxima:
                acurateteMaxima = acurateteCurenta
                self.modelInvatare = copy.deepcopy(modelInvatare)



    def suprimareNonMaxime(self, zoneDeInteres: list):
        zoneDeInteres.sort(key=(lambda x: x[4]), reverse=True)

        zoneCeRaman = [True for _ in range(len(zoneDeInteres))]

        for i in range(len(zoneDeInteres) - 1):
            if zoneCeRaman[i] == False:
                continue

            for j in range(i + 1, len(zoneDeInteres)):
                if zoneCeRaman[j] == False:
                    continue

                xMin1 = zoneDeInteres[i][0]
                yMin1 = zoneDeInteres[i][1]
                xMax1 = zoneDeInteres[i][2]
                yMax1 = zoneDeInteres[i][3]

                xMin2 = zoneDeInteres[j][0]
                yMin2 = zoneDeInteres[j][1]
                xMax2 = zoneDeInteres[j][2]
                yMax2 = zoneDeInteres[j][3]

                if Utilitar.intersectionOverUnion(xMin1, yMin1, xMax1, yMax1, xMin2, yMin2, xMax2, yMax2) > self.PRAG_INTERSECTION_OVER_UNION:
                    zoneCeRaman[j] = False

        return [zoneDeInteres[i] for i in range(len(zoneDeInteres)) if zoneCeRaman[i]]



    def testeaza(self, adresaTestare: str, adresaPredictiiRezultate: str):

        os.makedirs(adresaPredictiiRezultate, exist_ok=True)

        for fisierImagine in os.listdir(adresaTestare):
            print('Testare: ', adresaTestare + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaTestare + '/' + fisierImagine)
            imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

            zoneDeInteres = []

            for inaltimeFereastra in self.inaltimiFereastraUtilizabile:
                for aspectRatio in self.aspectRatiosUtilizabili:
                    if int(aspectRatio * inaltimeFereastra) > imagineOriginala.shape[1]:
                        continue

                    latimeFereastra = int(aspectRatio * inaltimeFereastra)

                    saltXFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * latimeFereastra)
                    saltYFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * inaltimeFereastra)

                    for xMin in range(0, imagineOriginala.shape[1] - latimeFereastra + 1, saltXFereastra):
                        for yMin in range(0, imagineOriginala.shape[0] - inaltimeFereastra + 1, saltYFereastra):
                            xMax = xMin + latimeFereastra - 1
                            yMax = yMin + inaltimeFereastra - 1

                            imagineDeInteres = imagineOriginala[yMin:yMax + 1, xMin:xMax + 1].copy()
                            imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)

                            descriptori = feature.hog(imagineDeInteres, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                            descriptori = descriptori.flatten().shape(1, -1)

                            scorPredictie = self.modelInvatare.decision_function(descriptori)

                            if scorPredictie > self.PRAG_PREDICTIE_POZITIVA_SVM:
                                zoneDeInteres.append((xMin, yMin, xMax, yMax, scorPredictie))


            zoneDeInteres = self.suprimareNonMaxime(zoneDeInteres)

            # Salvare Imagine cu Predictiile Evidentiate
            imagineRezultat = imagineOriginala.copy()

            for zonaDeInteres in zoneDeInteres:
                cv.rectangle(imagineRezultat, (zonaDeInteres[0], zonaDeInteres[1]), (zonaDeInteres[2], zonaDeInteres[3]), (255, 0, 0), 2)

            cv.imwrite(adresaPredictiiRezultate + '/' + fisierImagine, imagineRezultat)




