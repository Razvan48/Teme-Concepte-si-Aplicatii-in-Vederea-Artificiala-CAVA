import numpy as np
import cv2 as cv
import os

import EvaluatorSabloane
import Utilitar


class Tema_1:


    def __init__(self, adresaDirectorImagini: str, adresaImagineStart: str, nrJoc: int, nrImaginiPerJoc: int, adresaDirectorIesire: str, adresaDirectorSabloane: str, sabloaneDejaGenerate: bool):
        self.adresaDirectorImagini = adresaDirectorImagini
        self.adresaImagineStart = adresaImagineStart
        self.nrJoc = nrJoc
        self.nrImaginiPerJoc = nrImaginiPerJoc
        self.adresaDirectorIesire = adresaDirectorIesire

        self.evaluatorSabloane = EvaluatorSabloane.EvaluatorSabloane()

        if sabloaneDejaGenerate:
            self.evaluatorSabloane.incarcaSabloane(adresaDirectorSabloane)
        else:
            self.evaluatorSabloane.genereazaSiIncarcaSabloane(adresaDirectorImagini, '.jpg', adresaDirectorSabloane)

        self.dimImgAfisare = (512, 512)
        self.imaginiCareu = []

        self.numarDePeCelula = [[(-1) for j in range(14)] for i in range(14)]
        self.numarDePeCelula[6][6] = 1
        self.numarDePeCelula[6][7] = 2
        self.numarDePeCelula[7][6] = 3
        self.numarDePeCelula[7][7] = 4

        self.PONDERI_SCOR_CELULA = [
            [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
            [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
            [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3]
        ]

        self.CONSTRANGERI_CELULE = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', '-', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', '+', '*', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '/', ' ', ' ', ' ', ' ', '*', '+', ' ', ' ', ' ', ' ', '/', ' '],
            [' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],
            [' ', ' ', ' ', '*', '+', ' ', ' ', ' ', ' ', '*', '+', ' ', ' ', ' '],
            [' ', ' ', ' ', '+', '*', ' ', ' ', ' ', ' ', '+', '*', ' ', ' ', ' '],
            [' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],
            [' ', '/', ' ', ' ', ' ', ' ', '+', '*', ' ', ' ', ' ', ' ', '/', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', '*', '+', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', '-', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        self.indexCurentInListaRunde = -1
        self.listaRunde = self.__incarcaRundeDinFisier()


    def __reseteaza(self):
        self.numarDePeCelula = [[(-1) for j in range(14)] for i in range(14)]
        self.numarDePeCelula[6][6] = 1
        self.numarDePeCelula[6][7] = 2
        self.numarDePeCelula[7][6] = 3
        self.numarDePeCelula[7][7] = 4

        self.evaluatorSabloane.reseteazaPieseIncaFolosibile()

        self.indexCurentInListaRunde = -1
        self.listaRunde = self.__incarcaRundeDinFisier()


    def __incarcaRundeDinFisier(self):
        fisierRunde = open(f'{self.adresaDirectorImagini}/{self.nrJoc}_turns.txt', 'r')
        listaRunde = []

        for linie in fisierRunde:
            elementeLinie = linie.split(' ')
            listaRunde.append([elementeLinie[0], int(elementeLinie[1]), 0])

        fisierRunde.close()
        return listaRunde


    def __salveazaScoruriRundeInFisier(self):
        fisierScoruri = open(f'{self.adresaDirectorIesire}/{self.nrJoc}_scores.txt', 'w')

        rundaCurenta = 0
        for runda in self.listaRunde:
            fisierScoruri.write(f'{runda[0]} {runda[1]} {runda[2]}')
            if rundaCurenta + 1 < len(self.listaRunde):
                fisierScoruri.write('\n')
            rundaCurenta += 1


    def __salveazaRundeInFisier(self):
        fisierRunde = open(f'{self.adresaDirectorIesire}/{self.nrJoc}_turns.txt', 'w')

        rundaCurenta = 0
        for runda in self.listaRunde:
            fisierRunde.write(f'{runda[0]} {runda[1]}')
            if rundaCurenta + 1 < len(self.listaRunde):
                fisierRunde.write('\n')
            rundaCurenta += 1


    def __calculeazaScorPiesaNoua(self, iPiesa: int, jPiesa: int):
        valoarePiesa = self.PONDERI_SCOR_CELULA[iPiesa][jPiesa] * self.numarDePeCelula[iPiesa][jPiesa]
        scorTotalPiesa = 0

        #print('Pondere Piesa:', valoarePiesa)

        # Linie Stanga
        if jPiesa > 1 and self.numarDePeCelula[iPiesa][jPiesa - 1] != -1 and self.numarDePeCelula[iPiesa][jPiesa - 2] != -1:
            if (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '+') and self.numarDePeCelula[iPiesa][jPiesa - 1] + self.numarDePeCelula[iPiesa][jPiesa - 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '*') and self.numarDePeCelula[iPiesa][jPiesa - 1] * self.numarDePeCelula[iPiesa][jPiesa - 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa][jPiesa - 1] - self.numarDePeCelula[iPiesa][jPiesa - 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa][jPiesa - 2] - self.numarDePeCelula[iPiesa][jPiesa - 1] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa

            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa][jPiesa - 1] != 0 and self.numarDePeCelula[iPiesa][jPiesa - 2] % self.numarDePeCelula[iPiesa][jPiesa - 1] == 0 and self.numarDePeCelula[iPiesa][jPiesa - 2] // self.numarDePeCelula[iPiesa][jPiesa - 1] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa][jPiesa - 2] != 0 and self.numarDePeCelula[iPiesa][jPiesa - 1] % self.numarDePeCelula[iPiesa][jPiesa - 2] == 0 and self.numarDePeCelula[iPiesa][jPiesa - 1] // self.numarDePeCelula[iPiesa][jPiesa - 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
        #print('Scor Piesa:', scorTotalPiesa)

        # Linie Dreapta
        if jPiesa + 2 < 14 and self.numarDePeCelula[iPiesa][jPiesa + 1] != -1 and self.numarDePeCelula[iPiesa][jPiesa + 2] != -1:
            if (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '+') and self.numarDePeCelula[iPiesa][jPiesa + 1] + self.numarDePeCelula[iPiesa][jPiesa + 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '*') and self.numarDePeCelula[iPiesa][jPiesa + 1] * self.numarDePeCelula[iPiesa][jPiesa + 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa][jPiesa + 1] - self.numarDePeCelula[iPiesa][jPiesa + 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa][jPiesa + 2] - self.numarDePeCelula[iPiesa][jPiesa + 1] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa

            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa][jPiesa + 1] != 0 and self.numarDePeCelula[iPiesa][jPiesa + 2] % self.numarDePeCelula[iPiesa][jPiesa + 1] == 0 and self.numarDePeCelula[iPiesa][jPiesa + 2] // self.numarDePeCelula[iPiesa][jPiesa + 1] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa][jPiesa + 2] != 0 and self.numarDePeCelula[iPiesa][jPiesa + 1] % self.numarDePeCelula[iPiesa][jPiesa + 2] == 0 and self.numarDePeCelula[iPiesa][jPiesa + 1] // self.numarDePeCelula[iPiesa][jPiesa + 2] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
        #print('Scor Piesa:', scorTotalPiesa)

        # Coloana Sus
        if iPiesa > 1 and self.numarDePeCelula[iPiesa - 1][jPiesa] != -1 and self.numarDePeCelula[iPiesa - 2][jPiesa] != -1:
            if (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '+') and self.numarDePeCelula[iPiesa - 1][jPiesa] + self.numarDePeCelula[iPiesa - 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '*') and self.numarDePeCelula[iPiesa - 1][jPiesa] * self.numarDePeCelula[iPiesa - 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa - 1][jPiesa] - self.numarDePeCelula[iPiesa - 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa - 2][jPiesa] - self.numarDePeCelula[iPiesa - 1][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa

            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa - 1][jPiesa] != 0 and self.numarDePeCelula[iPiesa - 2][jPiesa] % self.numarDePeCelula[iPiesa - 1][jPiesa] == 0 and self.numarDePeCelula[iPiesa - 2][jPiesa] // self.numarDePeCelula[iPiesa - 1][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa - 2][jPiesa] != 0 and self.numarDePeCelula[iPiesa - 1][jPiesa] % self.numarDePeCelula[iPiesa - 2][jPiesa] == 0 and self.numarDePeCelula[iPiesa - 1][jPiesa] // self.numarDePeCelula[iPiesa - 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
        #print('Scor Piesa:', scorTotalPiesa)

        # Coloana Jos
        if iPiesa + 2 < 14 and self.numarDePeCelula[iPiesa + 1][jPiesa] != -1 and self.numarDePeCelula[iPiesa + 2][jPiesa] != -1:
            if (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '+') and self.numarDePeCelula[iPiesa + 1][jPiesa] + self.numarDePeCelula[iPiesa + 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '*') and self.numarDePeCelula[iPiesa + 1][jPiesa] * self.numarDePeCelula[iPiesa + 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa + 1][jPiesa] - self.numarDePeCelula[iPiesa + 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '-') and self.numarDePeCelula[iPiesa + 2][jPiesa] - self.numarDePeCelula[iPiesa + 1][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa

            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa + 1][jPiesa] != 0 and self.numarDePeCelula[iPiesa + 2][jPiesa] % self.numarDePeCelula[iPiesa + 1][jPiesa] == 0 and self.numarDePeCelula[iPiesa + 2][jPiesa] // self.numarDePeCelula[iPiesa + 1][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
            elif (self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == ' ' or self.CONSTRANGERI_CELULE[iPiesa][jPiesa] == '/') and self.numarDePeCelula[iPiesa + 2][jPiesa] != 0 and self.numarDePeCelula[iPiesa + 1][jPiesa] % self.numarDePeCelula[iPiesa + 2][jPiesa] == 0 and self.numarDePeCelula[iPiesa + 1][jPiesa] // self.numarDePeCelula[iPiesa + 2][jPiesa] == self.numarDePeCelula[iPiesa][jPiesa]:
                scorTotalPiesa += valoarePiesa
        #print('Scor Piesa:', scorTotalPiesa)

        return scorTotalPiesa


    def incarcaCareuImagine(self, nrImagine: int):
        if nrImagine == 0:
            imgInit = cv.imread(self.adresaImagineStart)
        elif nrImagine < 10:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_0{nrImagine}.jpg')
        else:
            imgInit = cv.imread(f'{self.adresaDirectorImagini}/{self.nrJoc}_{nrImagine}.jpg')

        imgCareu = Utilitar.extrageCareuImagine(imgInit)

        # self.afiseazaImagine(imgCareu)

        self.imaginiCareu.append(imgCareu)


    def __numarPixeliNegri(self, img):
        img = cv.resize(img, (16, 16))
        numPixeli = 0
        threshold = 89
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j, 0] < threshold and img[i, j, 1] < threshold and img[i, j, 2] < threshold:
                    numPixeli += 1
        return numPixeli


    def __candidatCorectCelulaLibera(self, i: int, j: int):
        if self.numarDePeCelula[i][j] != -1:
            return False

        if i > 1 and self.numarDePeCelula[i - 1][j] != -1 and self.numarDePeCelula[i - 2][j] != -1:
            return True
        if i + 2 < 14 and self.numarDePeCelula[i + 1][j] != -1 and self.numarDePeCelula[i + 2][j] != -1:
            return True
        if j > 1 and self.numarDePeCelula[i][j - 1] != -1 and self.numarDePeCelula[i][j - 2] != -1:
            return True
        if j + 2 < 14 and self.numarDePeCelula[i][j + 1] != -1 and self.numarDePeCelula[i][j + 2] != -1:
            return True

        return False


    def __identificareSingureleSabloaneAcceptabile(self, i : int, j : int):
        sabloaneAcceptabile = set()

        if i > 1 and self.numarDePeCelula[i - 1][j] != -1 and self.numarDePeCelula[i - 2][j] != -1:
            sabloaneAcceptabile.add(self.numarDePeCelula[i - 1][j] + self.numarDePeCelula[i - 2][j])
            sabloaneAcceptabile.add(self.numarDePeCelula[i - 1][j] * self.numarDePeCelula[i - 2][j])
            sabloaneAcceptabile.add(abs(self.numarDePeCelula[i - 1][j] - self.numarDePeCelula[i - 2][j]))
            if self.numarDePeCelula[i - 1][j] != 0 and self.numarDePeCelula[i - 2][j] % self.numarDePeCelula[i - 1][j] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i - 2][j] // self.numarDePeCelula[i - 1][j])
            if self.numarDePeCelula[i - 2][j] != 0 and self.numarDePeCelula[i - 1][j] % self.numarDePeCelula[i - 2][j] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i - 1][j] // self.numarDePeCelula[i - 2][j])
        if i + 2 < 14 and self.numarDePeCelula[i + 1][j] != -1 and self.numarDePeCelula[i + 2][j] != -1:
            sabloaneAcceptabile.add(self.numarDePeCelula[i + 1][j] + self.numarDePeCelula[i + 2][j])
            sabloaneAcceptabile.add(self.numarDePeCelula[i + 1][j] * self.numarDePeCelula[i + 2][j])
            sabloaneAcceptabile.add(abs(self.numarDePeCelula[i + 1][j] - self.numarDePeCelula[i + 2][j]))
            if self.numarDePeCelula[i + 1][j] != 0 and self.numarDePeCelula[i + 2][j] % self.numarDePeCelula[i + 1][j] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i + 2][j] // self.numarDePeCelula[i + 1][j])
            if self.numarDePeCelula[i + 2][j] != 0 and self.numarDePeCelula[i + 1][j] % self.numarDePeCelula[i + 2][j] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i + 1][j] // self.numarDePeCelula[i + 2][j])
        if j > 1 and self.numarDePeCelula[i][j - 1] != -1 and self.numarDePeCelula[i][j - 2] != -1:
            sabloaneAcceptabile.add(self.numarDePeCelula[i][j - 1] + self.numarDePeCelula[i][j - 2])
            sabloaneAcceptabile.add(self.numarDePeCelula[i][j - 1] * self.numarDePeCelula[i][j - 2])
            sabloaneAcceptabile.add(abs(self.numarDePeCelula[i][j - 1] - self.numarDePeCelula[i][j - 2]))
            if self.numarDePeCelula[i][j - 1] != 0 and self.numarDePeCelula[i][j - 2] % self.numarDePeCelula[i][j - 1] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i][j - 2] // self.numarDePeCelula[i][j - 1])
            if self.numarDePeCelula[i][j - 2] != 0 and self.numarDePeCelula[i][j - 1] % self.numarDePeCelula[i][j - 2] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i][j - 1] // self.numarDePeCelula[i][j - 2])
        if j + 2 < 14 and self.numarDePeCelula[i][j + 1] != -1 and self.numarDePeCelula[i][j + 2] != -1:
            sabloaneAcceptabile.add(self.numarDePeCelula[i][j + 1] + self.numarDePeCelula[i][j + 2])
            sabloaneAcceptabile.add(self.numarDePeCelula[i][j + 1] * self.numarDePeCelula[i][j + 2])
            sabloaneAcceptabile.add(abs(self.numarDePeCelula[i][j + 1] - self.numarDePeCelula[i][j + 2]))
            if self.numarDePeCelula[i][j + 1] != 0 and self.numarDePeCelula[i][j + 2] % self.numarDePeCelula[i][j + 1] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i][j + 2] // self.numarDePeCelula[i][j + 1])
            if self.numarDePeCelula[i][j + 2] != 0 and self.numarDePeCelula[i][j + 1] % self.numarDePeCelula[i][j + 2] == 0:
                sabloaneAcceptabile.add(self.numarDePeCelula[i][j + 1] // self.numarDePeCelula[i][j + 2])

        return sabloaneAcceptabile


    def compara2Imagini(self, indexAnt: int, indexCrt: int, filtrareStrictaCelule: bool):
        if indexAnt >= len(self.imaginiCareu) or indexCrt >= len(self.imaginiCareu):
            print('Nu sunt suficiente imagini')
            return

        # Copie ca sa putem modifica fara sa afectam imaginile originale
        imgAnt = self.imaginiCareu[indexAnt].copy()
        imgCrt = self.imaginiCareu[indexCrt].copy()

        latimeCelulaImgAnt = imgAnt.shape[1] / 14
        inaltimeCelulaImgAnt = imgAnt.shape[0] / 14
        latimeCelulaImgCrt = imgCrt.shape[1] / 14
        inaltimeCelulaImgCrt = imgCrt.shape[0] / 14

        # Debug
        xStangaSusSol = -1.0
        yStangaSusSol = -1.0
        latimeSol = -1.0
        inaltimeSol = -1.0

        xPragProcent = 0.082
        yPragProcent = 0.082

        difMaxima = -1.0
        iMaxim = -1
        jMaxim = -1
        imgCelulaMaximaFaraContur = None

        yImgAnt = 0.0
        yImgCrt = 0.0
        for i in range(14):
            xImgAnt = 0.0
            xImgCrt = 0.0

            for j in range(14):
                celulaImgAnt = imgAnt[int(yImgAnt):int(yImgAnt + inaltimeCelulaImgAnt), int(xImgAnt):int(xImgAnt + latimeCelulaImgAnt)].copy()
                celulaImgCrt = imgCrt[int(yImgCrt):int(yImgCrt + inaltimeCelulaImgCrt), int(xImgCrt):int(xImgCrt + latimeCelulaImgCrt)].copy()

                celulaImgAnt = cv.resize(celulaImgAnt, (int(latimeCelulaImgCrt), int(inaltimeCelulaImgCrt)))
                celulaImgAntFaraContur = celulaImgAnt[int(yPragProcent * inaltimeCelulaImgCrt):int((1.0 - yPragProcent) * inaltimeCelulaImgCrt), int(xPragProcent * latimeCelulaImgCrt):int((1.0 - xPragProcent) * latimeCelulaImgCrt)].copy()
                celulaImgCrtFaraContur = celulaImgCrt[int(yPragProcent * inaltimeCelulaImgCrt):int((1.0 - yPragProcent) * inaltimeCelulaImgCrt), int(xPragProcent * latimeCelulaImgCrt):int((1.0 - xPragProcent) * latimeCelulaImgCrt)].copy()

                if (self.__candidatCorectCelulaLibera(i, j) == False) or (filtrareStrictaCelule and (self.__numarPixeliNegri(celulaImgAntFaraContur) > 12 or self.__numarPixeliNegri(celulaImgCrtFaraContur) < 4)):
                    xImgAnt += latimeCelulaImgAnt
                    xImgCrt += latimeCelulaImgCrt
                    continue

                # difCurenta = np.mean((celulaImgCrtFaraContur - celulaImgAntFaraContur) ** 2)
                # difCurenta = np.mean(np.abs(celulaImgCrtFaraContur - celulaImgAntFaraContur))
                difCurenta = cv.norm(celulaImgAntFaraContur, celulaImgCrtFaraContur, cv.NORM_L2)

                if difCurenta > difMaxima:
                    difMaxima = difCurenta
                    iMaxim = i
                    jMaxim = j
                    imgCelulaMaximaFaraContur = celulaImgCrtFaraContur.copy()

                    # Debug
                    xStangaSusSol = xImgCrt
                    yStangaSusSol = yImgCrt
                    latimeSol = latimeCelulaImgCrt
                    inaltimeSol = inaltimeCelulaImgCrt

                xImgAnt += latimeCelulaImgAnt
                xImgCrt += latimeCelulaImgCrt

            yImgAnt += inaltimeCelulaImgAnt
            yImgCrt += inaltimeCelulaImgCrt


        # Debug pentru a vedea care este celula care a dat cea mai mare diferenta (incluzand si procentul de micsorare)
        #cv.rectangle(imgAnt, (int(xStangaSusSol + xPragProcent * latimeSol), int(yStangaSusSol + yPragProcent * inaltimeSol)), (int(xStangaSusSol + (1.0 - xPragProcent) * latimeSol), int(yStangaSusSol + (1.0 - yPragProcent) * inaltimeSol)), (0, 0, 255), -1)
        #cv.rectangle(imgCrt, (int(xStangaSusSol + xPragProcent * latimeSol), int(yStangaSusSol + yPragProcent * inaltimeSol)), (int(xStangaSusSol + (1.0 - xPragProcent) * latimeSol), int(yStangaSusSol + (1.0 - yPragProcent) * inaltimeSol)), (0, 0, 255), -1)
        #self.afiseazaImagini([imgAnt, imgCrt])


        if imgCelulaMaximaFaraContur is None:
            return self.compara2Imagini(indexAnt, indexCrt, False)

        etichetaSolutie = self.evaluatorSabloane.evalueazaImagine(imgCelulaMaximaFaraContur, self.__identificareSingureleSabloaneAcceptabile(iMaxim, jMaxim))

        self.numarDePeCelula[iMaxim][jMaxim] = etichetaSolutie

        self.listaRunde[self.indexCurentInListaRunde][2] += self.__calculeazaScorPiesaNoua(iMaxim, jMaxim)

        # iMaxim = rand, jMaxim = coloana
        return str(1 + iMaxim) + str(chr(jMaxim + ord('A'))) + ' ' + str(etichetaSolutie)


    def afiseazaImagine(self, img):
        cv.imshow('Imagine', cv.resize(img, self.dimImgAfisare))
        cv.moveWindow("Imagine", 200, 200)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def afiseazaImagini(self, imagini: list):
        imaginiRedim = [cv.resize(img, self.dimImgAfisare) for img in imagini]
        cv.imshow('Imagine', np.hstack(imaginiRedim))
        cv.moveWindow("Imagine", 200, 200)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def ruleaza(self):
        self.__reseteaza()

        self.incarcaCareuImagine(0)

        for i in range(1, self.nrImaginiPerJoc + 1):
            self.incarcaCareuImagine(i)

        os.makedirs(self.adresaDirectorIesire, exist_ok=True)

        for i in range(1, len(self.imaginiCareu)):

            if self.indexCurentInListaRunde + 1 < len(self.listaRunde) and i == self.listaRunde[self.indexCurentInListaRunde + 1][1]:
                self.indexCurentInListaRunde += 1

            raspuns = self.compara2Imagini(i - 1, i, True)
            print(f'Imaginea {i} - {raspuns}')
            #self.afiseazaImagini(self.imaginiCareu[i - 1:i + 1])

            adresaFisierIesire = self.adresaDirectorIesire
            if i > 9:
                adresaFisierIesire += '/' + f'{self.nrJoc}_{i}.txt'
            else:
                adresaFisierIesire += '/' + f'{self.nrJoc}_0{i}.txt'

            fisierIesire = open(adresaFisierIesire, 'w')
            fisierIesire.write(raspuns)
            fisierIesire.close()

            #print('Configuratie Tabla:')
            #for i in range(14):
            #    for j in range(14):
            #        print(self.numarDePeCelula[i][j], end=' ')
            #    print()


        self.__salveazaScoruriRundeInFisier()
        self.__salveazaRundeInFisier()



