import os
import sklearn.cluster as cluster
import numpy as np
import cv2 as cv



def genereazaHiperparametriFereastraGlisanta(adresaDirector: str, adresaHiperparametrii: str):

    aspectRatios = dict()
    aspectRatios['dad'] = set()
    aspectRatios['deedee'] = set()
    aspectRatios['dexter'] = set()
    aspectRatios['mom'] = set()
    aspectRatios['unknown'] = set()

    inaltimiFereastra = dict()
    inaltimiFereastra['dad'] = set()
    inaltimiFereastra['deedee'] = set()
    inaltimiFereastra['dexter'] = set()
    inaltimiFereastra['mom'] = set()
    inaltimiFereastra['unknown'] = set()

    for fisier in os.listdir(adresaDirector):
        if fisier.endswith('.txt'):
            fisierAdnotari = open(adresaDirector + '/' + fisier, 'r')
            for linie in fisierAdnotari:
                cuvinte = linie.split(' ')

                #elimina \n
                if cuvinte[-1][-1] == '\n':
                    cuvinte[-1] = cuvinte[-1][:-1]

                xMin = int(cuvinte[1])
                yMin = int(cuvinte[2])
                xMax = int(cuvinte[3])
                yMax = int(cuvinte[4])

                aspectRatios[cuvinte[5]].add((xMax - xMin) / (yMax - yMin))
                inaltimiFereastra[cuvinte[5]].add(yMax - yMin)

                if cuvinte[5] != 'unknown':
                    aspectRatios['unknown'].add((xMax - xMin) / (yMax - yMin))
                    inaltimiFereastra['unknown'].add(yMax - yMin)

            fisierAdnotari.close()


    os.makedirs(adresaHiperparametrii, exist_ok=True)


    NUM_CLUSTER_ASPECT_RATIO = 7
    for numePersonaj in aspectRatios:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatios.txt', 'w')
        for aspectRatio in aspectRatios[numePersonaj]:
            fisier.write(str(aspectRatio) + '\n')
        fisier.close()

        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatiosClustered.txt', 'w')
        aspectRatiosClustered = cluster.KMeans(n_clusters=NUM_CLUSTER_ASPECT_RATIO, random_state=7)
        aspectRatiosClustered.fit(np.array(list(aspectRatios[numePersonaj])).reshape(-1, 1))
        for clusterCenter in aspectRatiosClustered.cluster_centers_.flatten():
            fisier.write(str(clusterCenter) + '\n')
        fisier.close()


    NUM_CLUSTER_INALTIME_FEREASTRA = 7
    for numePersonaj in inaltimiFereastra:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastra.txt', 'w')
        for inaltimeFereastra in inaltimiFereastra[numePersonaj]:
            fisier.write(str(inaltimeFereastra) + '\n')
        fisier.close()

        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastraClustered.txt', 'w')
        inaltimiFereastraClustered = cluster.KMeans(n_clusters=NUM_CLUSTER_INALTIME_FEREASTRA, random_state=7)
        inaltimiFereastraClustered.fit(np.array(list(inaltimiFereastra[numePersonaj])).reshape(-1, 1))
        for clusterCenter in inaltimiFereastraClustered.cluster_centers_.flatten():
            fisier.write(str(clusterCenter) + '\n')
        fisier.close()



def genereazaExempleNegative(adresaDirector: str, adresaHiperparametrii: str, adresaExempleNegative: str, numarExemple: int):
    numePersonaje = ['dad', 'deedee', 'dexter', 'mom']

    NUMAR_EXEMPLE_ANTRENARE_PER_PERSONAJ = 1000
    for _ in range(numarExemple):
        numePersonaj = np.random.choice(numePersonaje)
        indexImagine = np.random.randint(1, NUMAR_EXEMPLE_ANTRENARE_PER_PERSONAJ + 1)

        print(indexImagine)


    # TODO: de creat orice fel de fisier daca nu exista, folosind os.makedirs(adresaExempleNegative, exist_ok=True) si altele
    # TODO: de implementat intersection over union si de ales exemple negative folosind asta
