import os
import numpy as np
import cv2 as cv

import torch



import Utilitar


class YOLOModel:

    def __init__(self, numePersonaj: str):  # numePersonaj trebuie sa fie 'unknown' in cazul task-ului 1
        self.numePersonaj = numePersonaj

        self.modelInvatare = None
        self.imaginiPozitive = []
        self.imaginiNegative = []

        self.PRAG_PREDICTIE_POZITIVA_YOLO = 0.0



    def antreneaza(self, adresaAntrenareExemplePozitive: str, adresaAntrenareExempleNegative: str):
        numePersonaje = ['dad', 'deedee', 'dexter', 'mom']  # 'unknown' nu trebuie inclus aici

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
                imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2RGB)

                if self.numePersonaj == numePersonaj or self.numePersonaj == 'unknown':  # self.numePersonaj si numePersonaj nu sunt aceleasi mereu
                    print('Antrenare Exemple Pozitive: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:
                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        self.imaginiPozitive.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = np.fliplr(imagineDeInteres)
                        self.imaginiPozitive.append(imagineDeInteres)
                else:
                    print('Antrenare Exemple Negative: ', adresaAntrenareExemplePozitive + '/' + numePersonaj + '/' + fisierImagine)

                    for zonaDeInteres in zoneDeInteres[fisierImagine]:
                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = np.fliplr(imagineDeInteres)
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = np.flipud(imagineDeInteres)
                        self.imaginiNegative.append(imagineDeInteres)

                        imagineDeInteres = imagineOriginala[zonaDeInteres[1]:zonaDeInteres[3] + 1, zonaDeInteres[0]:zonaDeInteres[2] + 1].copy()
                        imagineDeInteres = np.flipud(np.fliplr(imagineDeInteres))
                        self.imaginiNegative.append(imagineDeInteres)

        # exemple negative
        for fisierImagine in os.listdir(adresaAntrenareExempleNegative):
            print('Antrenare Exemple Negative: ', adresaAntrenareExempleNegative + '/' + fisierImagine)

            imagineOriginala = cv.imread(adresaAntrenareExempleNegative + '/' + fisierImagine)
            imagineOriginala = cv.cvtColor(imagineOriginala, cv.COLOR_BGR2RGB)

            self.imaginiNegative.append(imagineOriginala.copy())

            imagineInversataOrizontal = np.fliplr(imagineOriginala)
            self.imaginiNegative.append(imagineInversataOrizontal)

            imagineInversataVertical = np.flipud(imagineOriginala)
            self.imaginiNegative.append(imagineInversataVertical)

            imagineInversataVerticalOrizontal = np.flipud(np.fliplr(imagineOriginala))
            self.imaginiNegative.append(imagineInversataVerticalOrizontal)

        self.imaginiPozitive = np.array(self.imaginiPozitive)
        self.imaginiNegative = np.array(self.imaginiNegative)


        # Construire Model
        self.modelInvatare = torch.hub.load('ultralytics/yolov5:v6.2', 'yolov5s', pretrained=False)

        # Antrenare Model

        toateImaginile = np.concatenate((self.imaginiPozitive, self.imaginiNegative), axis=0)
        toateEtichetele = np.concatenate((np.ones(self.imaginiPozitive.shape[0]), np.zeros(self.imaginiNegative.shape[0])))

        # TODO: train model + modificari pentru metoda de test de mai jos


    def testeaza(self, adresaTestare: str, adresaPredictiiRezultate: str):

        # TODO: aici de vazut tot codul + refactoring

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
            zoneDeInteres = [(zoneDeInteres[i][0], zoneDeInteres[i][1], zoneDeInteres[i][2], zoneDeInteres[i][3],
                              scoruriImaginiDeInteres[i][0]) for i in range(len(zoneDeInteres))]
            zoneDeInteres = [zonaDeInteres for zonaDeInteres in zoneDeInteres if
                             zonaDeInteres[4] > self.PRAG_PREDICTIE_POZITIVA_CNN]

            zoneDeInteres = Utilitar.suprimareNonMaxime(zoneDeInteres)

            print('Scoruri Predictii: ')
            for zonaDeInteres in zoneDeInteres:
                print(zonaDeInteres[4])

            # Salvare Imagine cu Predictiile Evidentiate
            for zonaDeInteres in zoneDeInteres:
                cv.rectangle(imagineRezultat, (zonaDeInteres[0], zonaDeInteres[1]),
                             (zonaDeInteres[2], zonaDeInteres[3]), (0, 0, 255), 2)  # BGR

            cv.imwrite(adresaPredictiiRezultate + '/' + fisierImagine, imagineRezultat)




