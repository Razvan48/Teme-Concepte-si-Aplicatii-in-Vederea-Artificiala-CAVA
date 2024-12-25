import os
import sklearn.cluster as cluster
import numpy as np
import cv2 as cv



def genereazaHiperparametriFereastraGlisanta(adresaAntrenare: str, adresaHiperparametrii: str):

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

    for fisier in os.listdir(adresaAntrenare):
        if fisier.endswith('.txt'):
            fisierAdnotari = open(adresaAntrenare + '/' + fisier, 'r')
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



def intersectionOverUnion(xMin1, yMin1, xMax1, yMax1, xMin2, yMin2, xMax2, yMax2):
    suprapunereX = min(xMax1, xMax2) - max(xMin1, xMin2) + 1
    suprapunereY = min(yMax1, yMax2) - max(yMin1, yMin2) + 1

    if suprapunereX < 0:
        suprapunereX = 0
    if suprapunereY < 0:
        suprapunereY = 0

    arieSuprapunere = suprapunereX * suprapunereY
    arie1 = (xMax1 - xMin1 + 1) * (yMax1 - yMin1 + 1)
    arie2 = (xMax2 - xMin2 + 1) * (yMax2 - yMin2 + 1)

    if arie1 == 0 or arie2 == 0:
        raise ValueError('intersectionOverUnion: arie1 sau arie2 este 0')

    return arieSuprapunere / (arie1 + arie2 - arieSuprapunere)



def ferestreleSeSuprapun(xMin1, yMin1, xMax1, yMax1, xMin2, yMin2, xMax2, yMax2):
    suprapunereX = min(xMax1, xMax2) - max(xMin1, xMin2) + 1
    suprapunereY = min(yMax1, yMax2) - max(yMin1, yMin2) + 1

    return suprapunereX > 0 and suprapunereY > 0


def genereazaExempleNegative(adresaAntrenare: str, adresaHiperparametrii: str, adresaExempleNegative: str, numarExemple: int):
    numePersonaje = ['dad', 'deedee', 'dexter', 'mom']

    aspectRatiosUtilizabile = set()
    inaltimiFereastraUtilizabile = set()

    for numePersonaj in numePersonaje:
        fisierAspectRatios = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatiosClustered.txt', 'r')
        for linie in fisierAspectRatios:
            aspectRatiosUtilizabile.add(float(linie))
        fisierAspectRatios.close()

        fisierInaltimiFereastra = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastraClustered.txt', 'r')
        for linie in fisierInaltimiFereastra:
            inaltimiFereastraUtilizabile.add(float(linie))
        fisierInaltimiFereastra.close()



    os.makedirs(adresaExempleNegative, exist_ok=True)

    NUMAR_EXEMPLE_ANTRENARE_PER_PERSONAJ = 1000
    indexExempluNegativ = 0
    while indexExempluNegativ < numarExemple:
        numePersonaj = np.random.choice(numePersonaje)
        indexImagine = np.random.randint(1, NUMAR_EXEMPLE_ANTRENARE_PER_PERSONAJ + 1)

        strIndexImagine = str(indexImagine)
        if indexImagine < 10:
            strIndexImagine = '000' + strIndexImagine
        elif indexImagine < 100:
            strIndexImagine = '00' + strIndexImagine
        elif indexImagine < 1000:
            strIndexImagine = '0' + strIndexImagine

        fisierAdnotari = open(adresaAntrenare + '/' + numePersonaj + '_annotations.txt', 'r')
        zoneDeInteres = []

        for linie in fisierAdnotari:
            cuvinte = linie.split(' ')

            # elimina \n
            if cuvinte[-1][-1] == '\n':
                cuvinte[-1] = cuvinte[-1][:-1]

            numeFisierImagine = cuvinte[0]
            xMin = int(cuvinte[1])
            yMin = int(cuvinte[2])
            xMax = int(cuvinte[3])
            yMax = int(cuvinte[4])

            if numeFisierImagine == strIndexImagine + '.jpg':
                zoneDeInteres.append((xMin, yMin, xMax, yMax))

        fisierAdnotari.close()

        imagine = cv.imread(adresaAntrenare + '/' + numePersonaj + '/' + strIndexImagine + '.jpg')

        NUMAR_INCERCARI_EXEMPLU_NEGATIV = 5
        exempluNegativGasit = False
        indexIncercare = 0
        while (not exempluNegativGasit) and indexIncercare < NUMAR_INCERCARI_EXEMPLU_NEGATIV:
            aspectRatioAles = np.random.choice(list(aspectRatiosUtilizabile))
            inaltimeFereastraAleasa = int(np.random.choice(list(inaltimiFereastraUtilizabile)))

            if aspectRatioAles * inaltimeFereastraAleasa > imagine.shape[1]: # nu trebuie verificata si inaltimea fata de imagine.shape[0]
                continue

            xMin = np.random.randint(0, imagine.shape[1] - int(aspectRatioAles * inaltimeFereastraAleasa) + 1)
            yMin = np.random.randint(0, imagine.shape[0] - inaltimeFereastraAleasa + 1)
            xMax = xMin + int(aspectRatioAles * inaltimeFereastraAleasa) - 1
            yMax = yMin + inaltimeFereastraAleasa - 1


            exempluNegativGasit = True
            for zonaDeInteres in zoneDeInteres:
                if ferestreleSeSuprapun(xMin, yMin, xMax, yMax, zonaDeInteres[0], zonaDeInteres[1], zonaDeInteres[2], zonaDeInteres[3]):
                    exempluNegativGasit = False
                    break

            if exempluNegativGasit:
                cv.imwrite(adresaExempleNegative + '/' + str(indexExempluNegativ) + '.jpg', imagine[yMin:yMax + 1, xMin:xMax + 1])

            indexIncercare += 1

        if exempluNegativGasit:
            indexExempluNegativ += 1







