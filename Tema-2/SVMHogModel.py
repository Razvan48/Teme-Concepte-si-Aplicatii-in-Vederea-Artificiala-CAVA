import os
import copy
import datetime

import sklearn.svm as svm
import skimage.feature as feature
import numpy as np
import cv2 as cv

import pickle



import Utilitar



class SVMHogModel:



    def __init__(self, numePersonaj: str, adresaHiperparametrii: str): # numePersonaj trebuie sa fie 'unknown' in cazul task-ului 1
        self.numePersonaj = numePersonaj
        self.adresaHiperparametrii = adresaHiperparametrii

        self.pixeliPerCelula = (12, 12)
        self.celulePerBloc = (2, 2)
        self.celulePerImagine = (8, 8)
        self.numOrientari = 9

        self.dimensiuneImagine = (self.pixeliPerCelula[0] * self.celulePerImagine[0], self.pixeliPerCelula[1] * self.celulePerImagine[1])

        self.parametriiRegularizare = [(10 ** x) for x in range(-6, 6)]
        self.NUMAR_ITERATII_ANTRENARE = 100

        self.modelInvatare = None
        self.descriptoriPozitivi = []
        self.descriptoriNegativi = []

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

                imagineOriginala = cv.imread(adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)
                imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

                if self.numePersonaj == numePersonaj or self.numePersonaj == 'unknown':  # self.numePersonaj si numePersonaj nu sunt aceleasi mereu
                    print('Antrenare Exemple Pozitive: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:
                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriPozitivi.append(descriptori.flatten())

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.fliplr(imagineDeInteres), self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriPozitivi.append(descriptori.flatten())
                else:
                    print('Antrenare Exemple Negative: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:
                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriNegativi.append(descriptori.flatten())

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.fliplr(imagineDeInteres), self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriNegativi.append(descriptori.flatten())

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.flipud(imagineDeInteres), self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriNegativi.append(descriptori.flatten())

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.flipud(np.fliplr(imagineDeInteres)), self.dimensiuneImagine)
                        descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                        self.descriptoriNegativi.append(descriptori.flatten())


        # exemple negative
        for fisierImagine in os.listdir(adresaAntrenareExempleNegative):
            print('Antrenare Exemple Negative: ', adresaAntrenareExempleNegative + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaAntrenareExempleNegative + '/' + fisierImagine)
            imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

            imagine = cv.resize(imagineOriginala, self.dimensiuneImagine)
            descriptori = feature.hog(imagine, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataOrizontal = cv.resize(np.fliplr(imagineOriginala), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataOrizontal, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataVertical = cv.resize(np.flipud(imagineOriginala), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataVertical, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())

            imagineInversataVerticalOrizontal = cv.resize(np.flipud(np.fliplr(imagineOriginala)), self.dimensiuneImagine)
            descriptori = feature.hog(imagineInversataVerticalOrizontal, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
            self.descriptoriNegativi.append(descriptori.flatten())


        self.descriptoriPozitivi = np.array(self.descriptoriPozitivi)
        self.descriptoriNegativi = np.array(self.descriptoriNegativi)



        acurateteMaxima = -1.0

        for parametruRegularizare in self.parametriiRegularizare:

            modelInvatare = svm.LinearSVC(C=parametruRegularizare, max_iter=self.NUMAR_ITERATII_ANTRENARE)
            totiDescriptorii = np.concatenate((self.descriptoriPozitivi, self.descriptoriNegativi), axis=0)
            toateEtichetele = np.concatenate((np.ones(self.descriptoriPozitivi.shape[0]), np.zeros(self.descriptoriNegativi.shape[0])))
            modelInvatare.fit(totiDescriptorii, toateEtichetele)

            acurateteCurenta = modelInvatare.score(totiDescriptorii, toateEtichetele)
            print('Acuratete Model: ', acurateteCurenta)
            if acurateteCurenta > acurateteMaxima:
                acurateteMaxima = acurateteCurenta
                self.modelInvatare = copy.deepcopy(modelInvatare)

        print('Acuratete Maxima Model: ', acurateteMaxima)



    def testeaza(self, adresaTestare: str, adresaPredictiiRezultate: str):

        os.makedirs(adresaPredictiiRezultate, exist_ok=True)

        if self.numePersonaj == 'unknown':
            os.makedirs(adresaPredictiiRezultate + '/352_Capatina_Razvan/task1', exist_ok=True)
        else:
            os.makedirs(adresaPredictiiRezultate + '/352_Capatina_Razvan/task2', exist_ok=True)

        detectii = []
        numeFisiere = []
        scoruri = []

        for fisierImagine in sorted(os.listdir(adresaTestare)):
            print('Testare: ', adresaTestare + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaTestare + '/' + fisierImagine)
            imagineRezultat = imagineOriginala.copy()
            imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2GRAY)

            zoneDeInteres = []

            for inaltimeFereastra in self.inaltimiFereastraUtilizabile:
                for aspectRatio in self.aspectRatiosUtilizabili:
                    if int(aspectRatio * inaltimeFereastra) > imagineOriginala.shape[1]:
                        continue

                    # print('Inaltime Fereastra: ', inaltimeFereastra, ' Aspect Ratio: ', aspectRatio)

                    latimeFereastra = int(aspectRatio * inaltimeFereastra)

                    saltXFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * latimeFereastra)
                    saltYFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * inaltimeFereastra)

                    for yMin in range(0, imagineOriginala.shape[0] - int(inaltimeFereastra) + 1, saltYFereastra):
                        for xMin in range(0, imagineOriginala.shape[1] - latimeFereastra + 1, saltXFereastra):
                            xMax = xMin + latimeFereastra - 1
                            yMax = yMin + int(inaltimeFereastra) - 1

                            imagineDeInteres = imagineOriginala[yMin:yMax + 1, xMin:xMax + 1].copy()
                            imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)

                            descriptori = feature.hog(imagineDeInteres, orientations=self.numOrientari, pixels_per_cell=self.pixeliPerCelula, cells_per_block=self.celulePerBloc, feature_vector=False)
                            descriptori = descriptori.flatten().reshape(1, -1)

                            scorPredictie = self.modelInvatare.decision_function(descriptori)

                            if scorPredictie > self.PRAG_PREDICTIE_POZITIVA_SVM:
                                zoneDeInteres.append((xMin, yMin, xMax, yMax, scorPredictie))


            zoneDeInteres = Utilitar.suprimareNonMaxime(zoneDeInteres)

            for zonaDeInteres in zoneDeInteres:
                detectii.append([zonaDeInteres[0], zonaDeInteres[1], zonaDeInteres[2], zonaDeInteres[3]])
                numeFisiere.append(fisierImagine)
                scoruri.append(zonaDeInteres[4])

            print('Scoruri Predictii: ')
            for zonaDeInteres in zoneDeInteres:
                print(zonaDeInteres[4])

            # Salvare Imagine cu Predictiile Evidentiate
            '''
            os.makedirs(adresaPredictiiRezultate + '/352_Capatina_Razvan/imagini_' + self.numePersonaj, exist_ok=True)
            for zonaDeInteres in zoneDeInteres:
                cv.rectangle(imagineRezultat, (zonaDeInteres[0], zonaDeInteres[1]), (zonaDeInteres[2], zonaDeInteres[3]), (0, 0, 255), 2) # BGR

            cv.imwrite(adresaPredictiiRezultate + '/352_Capatina_Razvan/imagini_' + self.numePersonaj + '/' + fisierImagine, imagineRezultat)
            '''


        # Salvare

        if self.numePersonaj == 'unknown':
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task1/detections_all_faces.npy', np.array(detectii))
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task1/file_names_all_faces.npy', np.array(numeFisiere))
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task1/scores_all_faces.npy', np.array(scoruri))
        else:
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task2/detections_' + self.numePersonaj + '.npy', np.array(detectii))
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task2/file_names_' + self.numePersonaj + '.npy', np.array(numeFisiere))
            np.save(adresaPredictiiRezultate + '/352_Capatina_Razvan/task2/scores_' + self.numePersonaj + '.npy', np.array(scoruri))



    def salveazaModel(self, adresaSalvareModel: str):
        os.makedirs(adresaSalvareModel, exist_ok=True)
        data = datetime.datetime.now()
        pickle.dump(self.modelInvatare, open(adresaSalvareModel + '/' + self.numePersonaj + '_SVMHogModel_' + str(data.year) + '_' + str(data.month) + '_' + str(data.day) + '_' + str(data.hour) + '_' + str(data.minute) + '_' + str(data.second) + '.pkl', 'wb'))



    def incarcaModel(self, adresaIncarcareModel: str):
        self.modelInvatare = pickle.load(open(adresaIncarcareModel, 'rb'))





