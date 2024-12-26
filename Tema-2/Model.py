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

        self.aspectRatiosUtilizabile = set()
        fisierAspectRatios = open(self.adresaHiperparametrii + '/' + self.numePersonaj + '_aspectRatiosClustered.txt', 'r')
        for linie in fisierAspectRatios:
            self.aspectRatiosUtilizabile.add(float(linie))
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



        def testeaza(self, adresaTestare: str, adresaPredictii: str):

            # TODO: de terminat

            for fisierImagine in os.listdir(adresaTestare):
                imagine = cv.imread(adresaTestare + '/' + fisierImagine)

                imagine = cv.resize(imagine, self.dimensiuneImagine)

                descriptori = feature.hog(imagine, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)

                for i in range(descriptori.shape[0]):
                    for j in range(descriptori.shape[1]):
                        descriptor = descriptori[i, j, :].flatten()
                        eticheta = self.modelInvatare.predict(descriptor.reshape(1, -1))

                        if eticheta == 1:
                            cv.rectangle(imagine, (j * self.pixeliPerCelula[0], i * self.pixeliPerCelula[1]), ((j + self.celulePerBloc[1]) * self.pixeliPerCelula[0], (i + self.celulePerBloc[0]) * self.pixeliPerCelula[1]), (0, 255, 0), 2)

                cv.imwrite(adresaPredictii + '/' + fisierImagine, imagine)



