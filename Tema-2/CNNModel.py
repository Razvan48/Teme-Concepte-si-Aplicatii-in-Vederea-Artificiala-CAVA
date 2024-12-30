import copy
import os
import numpy as np
import cv2 as cv

import tensorflow as tf


import Utilitar



class CNNModel:



    def __init__(self, numePersonaj: str, adresaHiperparametrii: str): # numePersonaj trebuie sa fie 'unknown' in cazul task-ului 1
        self.numePersonaj = numePersonaj
        self.adresaHiperparametrii = adresaHiperparametrii

        self.dimensiuneImagine = (64, 64)

        self.modelInvatare = None
        self.imaginiPozitive = []
        self.imaginiNegative = []

        self.PROCENT_SALT_FEREASTRA_GLISANTA = 0.15
        self.PRAG_PREDICTIE_POZITIVA_CNN = 0.85

        self.SCALAR_NORMALIZARE = 255.0

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

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiPozitive.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.fliplr(imagineDeInteres), self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiPozitive.append(imagineDeInteres)

        self.imaginiPozitive = np.array(self.imaginiPozitive)

        # exemple negative
        for fisierImagine in os.listdir(adresaAntrenareExempleNegative):
            print('Antrenare Exemple Negative: ', adresaAntrenareExempleNegative + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaAntrenareExempleNegative + '/' + fisierImagine)

            imagine = cv.resize(imagineOriginala, self.dimensiuneImagine)
            imagine = imagine.astype(np.float32)
            imagine /= self.SCALAR_NORMALIZARE
            self.imaginiNegative.append(imagine)

            imagineInversataOrizontal = cv.resize(np.fliplr(imagineOriginala), self.dimensiuneImagine)
            imagineInversataOrizontal = imagineInversataOrizontal.astype(np.float32)
            imagineInversataOrizontal /= self.SCALAR_NORMALIZARE
            self.imaginiNegative.append(imagineInversataOrizontal)

            imagineInversataVertical = cv.resize(np.flipud(imagineOriginala), self.dimensiuneImagine)
            imagineInversataVertical = imagineInversataVertical.astype(np.float32)
            imagineInversataVertical /= self.SCALAR_NORMALIZARE
            self.imaginiNegative.append(imagineInversataVertical)

            imagineInversataVerticalOrizontal = cv.resize(np.flipud(np.fliplr(imagineOriginala)), self.dimensiuneImagine)
            imagineInversataVerticalOrizontal = imagineInversataVerticalOrizontal.astype(np.float32)
            imagineInversataVerticalOrizontal /= self.SCALAR_NORMALIZARE
            self.imaginiNegative.append(imagineInversataVerticalOrizontal)

        self.imaginiNegative = np.array(self.imaginiNegative)


        # Construire Model

        self.modelInvatare = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.dimensiuneImagine[0], self.dimensiuneImagine[1], 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        self.modelInvatare.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        '''
        self.modelInvatare = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.dimensiuneImagine[0], self.dimensiuneImagine[1], 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.BatchNormalization(),

            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.BatchNormalization(),

            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.BatchNormalization(),

            tf.keras.layers.GlobalAveragePooling2D(),

            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.5),

            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        self.modelInvatare.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        '''


        # Antrenare Model

        toateImaginile = np.concatenate((self.imaginiPozitive, self.imaginiNegative), axis=0)
        toateEtichetele = np.concatenate((np.ones(self.imaginiPozitive.shape[0]), np.zeros(self.imaginiNegative.shape[0])))
        self.modelInvatare.fit(toateImaginile, toateEtichetele)

        print('Acuratete Model: ', self.modelInvatare.evaluate(toateImaginile, toateEtichetele)[1]) # 0 = loss, 1 = accuracy



    def testeaza(self, adresaTestare: str, adresaPredictiiRezultate: str):

        os.makedirs(adresaPredictiiRezultate, exist_ok=True)

        for fisierImagine in os.listdir(adresaTestare):
            print('Testare: ', adresaTestare + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaTestare + '/' + fisierImagine)
            imagineRezultat = imagineOriginala.copy()

            zoneDeInteres = []
            imaginiDeInteres = []

            for inaltimeFereastra in self.inaltimiFereastraUtilizabile:
                for aspectRatio in self.aspectRatiosUtilizabili:
                    if int(aspectRatio * inaltimeFereastra) > imagineOriginala.shape[1]:
                        continue

                    print('Inaltime Fereastra: ', inaltimeFereastra, ' Aspect Ratio: ', aspectRatio)

                    latimeFereastra = int(aspectRatio * inaltimeFereastra)

                    saltXFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * latimeFereastra)
                    saltYFereastra = int(self.PROCENT_SALT_FEREASTRA_GLISANTA * inaltimeFereastra)

                    for yMin in range(0, imagineOriginala.shape[0] - int(inaltimeFereastra) + 1, saltYFereastra):
                        for xMin in range(0, imagineOriginala.shape[1] - latimeFereastra + 1, saltXFereastra):
                            xMax = xMin + latimeFereastra - 1
                            yMax = yMin + int(inaltimeFereastra) - 1

                            imagineDeInteres = imagineOriginala[yMin:yMax + 1, xMin:xMax + 1].copy()
                            imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                            imagineDeInteres = imagineDeInteres.astype(np.float32)
                            imagineDeInteres /= self.SCALAR_NORMALIZARE

                            zoneDeInteres.append((xMin, yMin, xMax, yMax))
                            imaginiDeInteres.append(imagineDeInteres)


            scoruriImaginiDeInteres = self.modelInvatare.predict(np.array(imaginiDeInteres))
            zoneDeInteres = [(zoneDeInteres[i][0], zoneDeInteres[i][1], zoneDeInteres[i][2], zoneDeInteres[i][3], scoruriImaginiDeInteres[i][0]) for i in range(len(zoneDeInteres))]
            zoneDeInteres = [zonaDeInteres for zonaDeInteres in zoneDeInteres if zonaDeInteres[4] > self.PRAG_PREDICTIE_POZITIVA_CNN]

            zoneDeInteres = Utilitar.suprimareNonMaxime(zoneDeInteres)

            print('Scoruri Predictii: ')
            for zonaDeInteres in zoneDeInteres:
                print(zonaDeInteres[4])

            # Salvare Imagine cu Predictiile Evidentiate
            for zonaDeInteres in zoneDeInteres:
                cv.rectangle(imagineRezultat, (zonaDeInteres[0], zonaDeInteres[1]), (zonaDeInteres[2], zonaDeInteres[3]), (0, 0, 255), 2) # BGR

            cv.imwrite(adresaPredictiiRezultate + '/' + fisierImagine, imagineRezultat)




