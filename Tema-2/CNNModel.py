import os
import datetime

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

        self.PROCENT_SALT_FEREASTRA_GLISANTA = 0.2
        self.PRAG_PREDICTIE_POZITIVA_CNN = 0.9

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

                if self.numePersonaj == numePersonaj or self.numePersonaj == 'unknown':  # self.numePersonaj si numePersonaj nu sunt aceleasi mereu
                    print('Antrenare Exemple Pozitive: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

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
                else:
                    print('Antrenare Exemple Negative: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(imagineDeInteres, self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.fliplr(imagineDeInteres), self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.flipud(imagineDeInteres), self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = cv.resize(np.flipud(np.fliplr(imagineDeInteres)), self.dimensiuneImagine)
                        imagineDeInteres = imagineDeInteres.astype(np.float32)
                        imagineDeInteres /= self.SCALAR_NORMALIZARE
                        self.imaginiNegative.append(imagineDeInteres)



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


        self.imaginiPozitive = np.array(self.imaginiPozitive)
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

            zoneDeInteres = []
            imaginiDeInteres = []

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
                            imagineDeInteres = imagineDeInteres.astype(np.float32)
                            imagineDeInteres /= self.SCALAR_NORMALIZARE

                            zoneDeInteres.append((xMin, yMin, xMax, yMax))
                            imaginiDeInteres.append(imagineDeInteres)


            scoruriImaginiDeInteres = self.modelInvatare.predict(np.array(imaginiDeInteres))
            zoneDeInteres = [(zoneDeInteres[i][0], zoneDeInteres[i][1], zoneDeInteres[i][2], zoneDeInteres[i][3], scoruriImaginiDeInteres[i][0]) for i in range(len(zoneDeInteres))]
            zoneDeInteres = [zonaDeInteres for zonaDeInteres in zoneDeInteres if zonaDeInteres[4] > self.PRAG_PREDICTIE_POZITIVA_CNN]

            zoneDeInteres = Utilitar.suprimareNonMaxime(zoneDeInteres)

            for zonaDeInteres in zoneDeInteres:
                detectii.append([zonaDeInteres[0], zonaDeInteres[1], zonaDeInteres[2], zonaDeInteres[3]])
                numeFisiere.append(fisierImagine)
                scoruri.append(zonaDeInteres[4])

            # print('Scoruri Predictii: ')
            # for zonaDeInteres in zoneDeInteres:
            #     print(zonaDeInteres[4])

            # Salvare Imagine cu Predictiile Evidentiate
            os.makedirs(adresaPredictiiRezultate + '/352_Capatina_Razvan/imagini_' + self.numePersonaj, exist_ok=True)
            for zonaDeInteres in zoneDeInteres:
                cv.rectangle(imagineRezultat, (zonaDeInteres[0], zonaDeInteres[1]), (zonaDeInteres[2], zonaDeInteres[3]), (0, 0, 255), 2) # BGR

            cv.imwrite(adresaPredictiiRezultate + '/352_Capatina_Razvan/imagini_' + self.numePersonaj + '/' + fisierImagine, imagineRezultat)


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
        self.modelInvatare.save(adresaSalvareModel + '/' + self.numePersonaj + '_CNNModel_' + str(data.year) + '_' + str(data.month) + '_' + str(data.day) + '_' + str(data.hour) + '_' + str(data.minute) + '_' + str(data.second) + '.h5')


    def incarcaModel(self, adresaIncarcareModel: str):
        self.modelInvatare = tf.keras.models.load_model(adresaIncarcareModel)
        #self.dimensiuneImagine = (self.modelInvatare.input_shape[1], self.modelInvatare.input_shape[2])





