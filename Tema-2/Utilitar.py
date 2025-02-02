import shutil
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

                aspectRatios[cuvinte[5]].add((xMax - xMin + 1.0) / (yMax - yMin + 1.0))
                inaltimiFereastra[cuvinte[5]].add(yMax - yMin + 1)

                if cuvinte[5] != 'unknown':
                    aspectRatios['unknown'].add((xMax - xMin + 1.0) / (yMax - yMin + 1.0))
                    inaltimiFereastra['unknown'].add(yMax - yMin + 1)

            fisierAdnotari.close()


    os.makedirs(adresaHiperparametrii, exist_ok=True)


    NUM_CLUSTER_ASPECT_RATIO = 4
    NUM_CLUSTER_ASPECT_RATIO_UNKNOWN = 1 * NUM_CLUSTER_ASPECT_RATIO
    for numePersonaj in aspectRatios:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatios.txt', 'w')
        for aspectRatio in aspectRatios[numePersonaj]:
            fisier.write(str(aspectRatio) + '\n')
        fisier.close()

        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatiosClustered.txt', 'w')
        numClusterAspectRatio = NUM_CLUSTER_ASPECT_RATIO
        if numePersonaj == 'unknown':
            numClusterAspectRatio = NUM_CLUSTER_ASPECT_RATIO_UNKNOWN
        aspectRatiosClustered = cluster.KMeans(n_clusters=numClusterAspectRatio, random_state=7)
        aspectRatiosClustered.fit(np.array(list(aspectRatios[numePersonaj])).reshape(-1, 1))
        for clusterCenter in aspectRatiosClustered.cluster_centers_.flatten():
            fisier.write(str(clusterCenter) + '\n')
        fisier.close()


    NUM_CLUSTER_INALTIME_FEREASTRA = 6
    NUM_CLUSTER_INALTIME_FEREASTRA_UNKNOWN = 1 * NUM_CLUSTER_INALTIME_FEREASTRA
    for numePersonaj in inaltimiFereastra:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastra.txt', 'w')
        for inaltimeFereastra in inaltimiFereastra[numePersonaj]:
            fisier.write(str(inaltimeFereastra) + '\n')
        fisier.close()

        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastraClustered.txt', 'w')
        numClusterInaltimeFereastra = NUM_CLUSTER_INALTIME_FEREASTRA
        if numePersonaj == 'unknown':
            numClusterInaltimeFereastra = NUM_CLUSTER_INALTIME_FEREASTRA_UNKNOWN
        inaltimiFereastraClustered = cluster.KMeans(n_clusters=numClusterInaltimeFereastra, random_state=7)
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



def punctInDreptunghi(xPunct, yPunct, xMin, yMin, xMax, yMax):
    return xMin < xPunct and xPunct < xMax and yMin < yPunct and yPunct < yMax



def segmentInSegment(st1, dr1, st2, dr2):
    return st2 <= st1 and dr1 <= dr2



def dreptunghiInDreptunghi(xMin1, yMin1, xMax1, yMax1, xMin2, yMin2, xMax2, yMax2):
    return segmentInSegment(xMin1, xMax1, xMin2, xMax2) and segmentInSegment(yMin1, yMax1, yMin2, yMax2)



def genereazaExempleNegative(adresaAntrenare: str, adresaHiperparametrii: str, adresaExempleNegative: str, numarExemple: int):
    numePersonaje = ['dad', 'deedee', 'dexter', 'mom'] # 'unknown' nu trebuie inclus aici

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

    # pentru unknown
    fisierAspectRatios = open(adresaHiperparametrii + '/unknown_aspectRatiosClustered.txt', 'r')
    for linie in fisierAspectRatios:
        aspectRatiosUtilizabile.add(float(linie))
    fisierAspectRatios.close()

    fisierInaltimiFereastra = open(adresaHiperparametrii + '/unknown_inaltimiFereastraClustered.txt', 'r')
    for linie in fisierInaltimiFereastra:
        inaltimiFereastraUtilizabile.add(float(linie))
    fisierInaltimiFereastra.close()



    if os.path.exists(adresaExempleNegative):
        shutil.rmtree(adresaExempleNegative)
    os.makedirs(adresaExempleNegative, exist_ok=True)



    NUMAR_EXEMPLE_ANTRENARE_PER_PERSONAJ = 1000
    indexExempluNegativ = 0
    while indexExempluNegativ < numarExemple:
        print('Se construieste exemplul negativ ' + str(indexExempluNegativ) + '...')

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
            inaltimeFereastraAleasa = np.random.choice(list(inaltimiFereastraUtilizabile))

            if int(aspectRatioAles * inaltimeFereastraAleasa) > imagine.shape[1]: # nu trebuie verificata si inaltimea fata de imagine.shape[0]
                continue

            xMin = np.random.randint(0, imagine.shape[1] - int(aspectRatioAles * inaltimeFereastraAleasa) + 1)
            yMin = np.random.randint(0, imagine.shape[0] - int(inaltimeFereastraAleasa) + 1)
            xMax = xMin + int(aspectRatioAles * inaltimeFereastraAleasa) - 1
            yMax = yMin + int(inaltimeFereastraAleasa) - 1


            PRAG_INTERSECTION_OVER_UNION = 0.3
            exempluNegativGasit = True
            for zonaDeInteres in zoneDeInteres:
                if intersectionOverUnion(xMin, yMin, xMax, yMax, zonaDeInteres[0], zonaDeInteres[1], zonaDeInteres[2], zonaDeInteres[3]) > PRAG_INTERSECTION_OVER_UNION or dreptunghiInDreptunghi(zonaDeInteres[0], zonaDeInteres[1], zonaDeInteres[2], zonaDeInteres[3], xMin, yMin, xMax, yMax):
                    exempluNegativGasit = False
                    break

            if exempluNegativGasit:
                cv.imwrite(adresaExempleNegative + '/' + str(indexExempluNegativ) + '.jpg', imagine[yMin:yMax + 1, xMin:xMax + 1])

            indexIncercare += 1

        if exempluNegativGasit:
            indexExempluNegativ += 1



def suprimareNonMaxime(zoneDeInteres: list):
    if len(zoneDeInteres) < 2:
        return zoneDeInteres

    PRAG_INTERSECTION_OVER_UNION = 0.3

    zoneDeInteres.sort(key=(lambda x: x[4]), reverse=True)

    zoneCeRaman = [True for _ in range(len(zoneDeInteres))]

    for i in range(len(zoneDeInteres) - 1):
        if not zoneCeRaman[i]:
            continue

        for j in range(i + 1, len(zoneDeInteres)):
            if not zoneCeRaman[j]:
                continue

            xMin1 = zoneDeInteres[i][0]
            yMin1 = zoneDeInteres[i][1]
            xMax1 = zoneDeInteres[i][2]
            yMax1 = zoneDeInteres[i][3]

            xMin2 = zoneDeInteres[j][0]
            yMin2 = zoneDeInteres[j][1]
            xMax2 = zoneDeInteres[j][2]
            yMax2 = zoneDeInteres[j][3]

            xCentru2 = (xMin2 + xMax2) / 2
            yCentru2 = (yMin2 + yMax2) / 2

            if intersectionOverUnion(xMin1, yMin1, xMax1, yMax1, xMin2, yMin2, xMax2, yMax2) > PRAG_INTERSECTION_OVER_UNION:
                zoneCeRaman[j] = False
            elif punctInDreptunghi(xCentru2, yCentru2, xMin1, yMin1, xMax1, yMax1):
                zoneCeRaman[j] = False

    return [zoneDeInteres[i] for i in range(len(zoneDeInteres)) if zoneCeRaman[i]]






