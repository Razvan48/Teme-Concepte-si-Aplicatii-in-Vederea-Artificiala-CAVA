Adnotari schimbate:

In dad_annotations: 0455.jpg 250 57 425 311 dad  (era mom inainte)
In deedee_annotations: 0347.jpg 288 39 413 133 deedee (era dexter inainte)
In deedee_annotations: 0471.jpg 326 6 414 65 deedee (era dexter inainte)
In deedee_annotations: 0656.jpg 152 146 343 264 deedee (era unknown inainte)
In dexter_annotations: 0921.jpg 109 111 267 278 dexter (era deedee inainte)


Versiune Python: 3.9.13


Module folosite:

shutil
os
scikit-learn==1.5.0
numpy==1.26.4
opencv-python==4.10.0 (4.10.0.84)

copy
datetime
scikit-image==0.24.0
pickle==4.0

tensorflow==2.17.0
keras==3.5.0


Mod de Utilizare:

Fisierele main.py, Utilitar.py, SVMHogModel.py, CNNModel.py trebuie sa ramana intr-un director comun.

Fisierul SVMHogModel.py nu va fi folosit, l-am inclus deoarece contine implementarea mai putin performanta
ce foloseste descriptorii HoG si pe care am mentionat-o in documentatia pdf.
Implementarea finala foloseste CNNModel.py.

Toate filepath-urile folosite in implementare sunt relative la acest director comun.

Proiectul se va rula pornind din main.py.

Mai intai trebuie declarata o instanta a clasei CNNModel.

Constructorul clasei are urmatorii parametrii in aceasta ordine:

numePersonaj (string) = numele personajului (pentru Task-ul 1 se foloseste "unknown", iar pentru Task-ul 2 orice
din multimea {"dad", "deedee", "dexter", "mom"}).

adresaHiperparametrii (string) = adresa unde se afla fisierele .txt de aspectRatio-uri clusterizate si inaltimi clusterizate necesare ferestrei glisante.

Dupa ce obiectul de tip CNNModel a fost instantiat se va apela metoda .incarcaModel() care primeste adresa unde se afla fisierul de format .h5 ce reprezinta modelul.

Se poate apela apoi metoda .testeaza(), care primeste adresa fisierului unde se afla imaginile de test si adresa unde sa creeze un fisier cu numele 352_Capatina_Razvan in care se vor genera 2 alte fisiere (task1 si task2)
ce vor contine predictiile in format .npy.

Instantele clasei CNNModel sunt de unica folosinta, trebuie realizata o noua instanta pentru fiecare task in parte (Task1, Task2-Dad, Task2-DeeDee, Task2-Dexter, Task2-Mom).

Clasa CNNModel mai contine 2 metode:
.salveazaModel(), care primeste o adresa unde sa salveze sub format .h5 modelul curent.
.antreneaza(), care primeste adresa unde se afla fisierul de antrenare primit initial (si cu aceeasi ierarhie de fisiere, dad/deedee/dexter/mom, dad_annotations.txt, deedee_annotations.txt, etc.) si adresa
unde se afla fisierul cu exemple negative ("iesire/exempleNegativeOriginal", cu 20.000 exemple si "iesire/exempleNegativeExtinse", cu 30.000 exemple).





Exemplu de cod:




# CNN Model

cnnModelUnknown = CNNModel.CNNModel('unknown', 'fisiere/iesire/hiperparametrii')

cnnModelUnknown.incarcaModel('fisiere/iesire/modele/CNNModel/unknown_CNNModel_2025_1_20_0_4_49.h5')

cnnModelUnknown.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar Dad

cnnModelDad = CNNModel.CNNModel('dad', 'fisiere/iesire/hiperparametrii')

cnnModelDad.incarcaModel('fisiere/iesire/modele/CNNModel/dad_CNNModel_2025_1_18_0_20_2.h5')

cnnModelDad.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar DeeDee

cnnModelDeeDee = CNNModel.CNNModel('deedee', 'fisiere/iesire/hiperparametrii')

cnnModelDeeDee.incarcaModel('fisiere/iesire/modele/CNNModel/deedee_CNNModel_2025_1_18_18_56_49.h5')

cnnModelDeeDee.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar Dexter

cnnModelDexter = CNNModel.CNNModel('dexter', 'fisiere/iesire/hiperparametrii')

cnnModelDexter.incarcaModel('fisiere/iesire/modele/CNNModel/dexter_CNNModel_2025_1_18_19_20_29.h5')

cnnModelDexter.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')

# CNN doar Mom

cnnModelMom = CNNModel.CNNModel('mom', 'fisiere/iesire/hiperparametrii')

cnnModelMom.incarcaModel('fisiere/iesire/modele/CNNModel/mom_CNNModel_2025_1_20_22_15_39.h5')

cnnModelMom.testeaza('fisiere/evaluare/fake_test', 'fisiere/iesire')



















