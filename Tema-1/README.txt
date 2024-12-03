Versiune Python: 3.9.13


Module Folosite:

numpy==2.0.2
opencv_python==4.10.0 (4.10.0.84)
os
shutil


Mod de Utilizare:

Fisierele EvaluatorSabloane.py, main.py, Tema_1.py si Utilitar.py trebuie sa ramana intr-un director comun.
Toate filepath-urile folosite in implementare sunt relative la acest director comun.

Pentru a rula proiectul trebuie ca in main.py sa se instantieze un obiect de tipul Tema_1 si apoi acestei instante sa i se apeleze metoda .ruleaza().
Instantele de tipul Tema_1 au o unica folosinta, odata rulate nu mai pot fi refolosite, trebuie reinstantiate.

Constructorul clasei Tema_1 are urmatorii parametri (in aceasta ordine):

adresaDirectorImagini : string, reprezinta filepath-ul catre directorul unde se afla fisierele de test .jpg si cele .txt.

adresaImagineStart : string, reprezinta filepath-ul catre imaginea de baza a tablei (echivalentul la 01.jpg din imagini_auxiliare)

nrJoc : int, reprezinta indexul jocului ce va fi rulat (programul va incarca doar fisierele de forma nrJoc_x.txt si nrJoc_x.jpg din adresaDirectorImagini)

nrImaginiPerJoc : int, primele cate imagini din jocul respectiv vor fi incarcate (50)

adresaDirectorIesire : string, fisierul unde se va genera tot output-ul aplicatiei.

adresaDirectorSabloane : string, fisierul unde se afla toate seturile de date pentru template matching pe care aplicatia le va incarca si utiliza la task-ul 2. Daca urmatorul parametru (sabloaneDejaGenerate : bool este setat pe True, atunci aplicatia doar va incarca toate sabloanele gasite la aceasta adresa, altfel va genera seturile de date aici).

sabloaneDejaGenerate : bool, ramane pe True, am adaugat in arhiva toate seturile de date, nu mai este necesara regenerarea lor.


Fragment de cod pentru rulat in main.py:

tema_1 = Tema_1.Tema_1('fisiere/testare', 'fisiere/imagini_auxiliare/01.jpg', 1, 50, 'fisiere/iesire/352_Capatina_Razvan', 'fisiere/sabloane', True)
tema_1.ruleaza()

tema_1 = Tema_1.Tema_1('fisiere/testare', 'fisiere/imagini_auxiliare/01.jpg', 2, 50, 'fisiere/iesire/352_Capatina_Razvan', 'fisiere/sabloane', True)
tema_1.ruleaza()

tema_1 = Tema_1.Tema_1('fisiere/testare', 'fisiere/imagini_auxiliare/01.jpg', 3, 50, 'fisiere/iesire/352_Capatina_Razvan', 'fisiere/sabloane', True)
tema_1.ruleaza()

tema_1 = Tema_1.Tema_1('fisiere/testare', 'fisiere/imagini_auxiliare/01.jpg', 4, 50, 'fisiere/iesire/352_Capatina_Razvan', 'fisiere/sabloane', True)
tema_1.ruleaza()



Pentru un Intel Core i7, 2.80GHz si 16GB RAM:

Incarcarea sabloanelor (fara generare) dureaza aproximativ 10-15 secunde.
Generarea raspunsurilor pentru un singur test (50 de imagini) dureaza in jur de 30 de secunde.




























