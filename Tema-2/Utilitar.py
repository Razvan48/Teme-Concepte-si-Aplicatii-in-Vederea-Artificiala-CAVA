import os


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

    for numePersonaj in aspectRatios:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_aspectRatios.txt', 'w')
        for aspectRatio in aspectRatios[numePersonaj]:
            fisier.write(str(aspectRatio) + '\n')
        fisier.close()

    for numePersonaj in inaltimiFereastra:
        fisier = open(adresaHiperparametrii + '/' + numePersonaj + '_inaltimiFereastra.txt', 'w')
        for inaltimeFereastra in inaltimiFereastra[numePersonaj]:
            fisier.write(str(inaltimeFereastra) + '\n')
        fisier.close()
