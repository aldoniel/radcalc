# radcalc

## Intro

Permet de calculer
* DFG
* Poumon
    * modèle de Brock
    * modèle de Herder
    * temps de doublement
    * arbres décisionnels
        * BTS 2015
        * Fleischner 2017
* Onco
    * RECIST
    * lugano lymphomes
* Endoc
    * calcul wash-out surrénales
    * volume testicule ; volume surface ovaire
    * mémo tirads
* Vasculaire
    * % sténose
    * score d'accident coronarien MESA à 10 ans
* Divers
    * Volume ellipsoïde
    * IMC ; surface corporelle

## Versions utilisables (Release)
* Sur l'android store, voir [RadCalc par Aldoniel](https://play.google.com/store/apps/details?id=io.aldoniel.radcalc)
* Sur tous navigateurs (PC, téléphones) [version en ligne](https://aldoniel.github.io/radcalc/)

Pour iOS(c), il faut ouvrir la version navigateur dans Safari, puis dans le menu du bas, toucher "partager" (l'icône boîte avec une flèche haute), puis glisser vers le haut ("swipe" haut), puis défiler dans la liste jusqu'à "Ajouter à l'écran d'accueil".

Sur Chrome, le menu ajouter à l'écran d'accueil est présent dans les options générales de la page web en haut à droite.

Il faut ensuite ouvrir l'application une fois depuis son icône sur l'écran d'accueil du téléphone et elle devrait ensuite fonctionner en mode hors ligne.

## Licence
* Ce code est placé sous droit français et licence CeCILL 2.1 (voir cecill21fr.html).

## Todo
1. [ ] se motiver pour étudier un auto adaptateur d'injection d'iode même si la SFR est pas intéressée...
1. [x] ajout nouveau calcul adénomes
1. [x] ajouter inverser à lugano
1. [x] essayer de publier une web app ios
1. [x] ajouter inverser avant et après dans le recist
1. [x] ajouter un mémo de tirads
1. [x] remettre dans les notes le seuil de significative du volume (nodule)
1. [x] ajouter dans l'app tuto install / ios + QR code lien et un contact
1. [x] désactiver la licence en ligne
​1. [x] ajouter tableau ecst nascet
1. [ ] arranger le modal : il faut prblm faire une version android et une windows pour faire simple. Echec. J'ai mis un vieux hack avec une taille fixe pour PC dans le css max-height: 800px; qui passe sur un écran "normal" et c'est pas lié au css, j'ai idem en png quoique je fasse (en pire car le hack déforme.). On peut tenter de faire une version à la carte par image en récupérant plus d'attributs (fait sur les QR avec récup de height width)
1. [x] ajouter le support de la touche retour au modal
1. [x] ajouter surface ovaire
1. [x] ajouter un convertisseur de volume élipsoïde en lambert
1. [x] ajouter des boutons effacer les champs partout, 
1. [ ] arranger le padding du menu top qui est n'importe quoi
1. [x] corriger le bug recist
1. [x] menu recist incohérent
1. [x] faire vascu
1. [x] ajouter les avertissements légaux
1. [x] arranger le sélecteur de date d'android qui est vraiment nul : abandon on fera avec
1. [x] publier sur android
1. [x] et sur internet
1. [x] ajouter une option de volume ellipsoïde
1. [x] et un convertisseur d'elipsoïde en lambert
1. [x] comprendre pourquoi sur android l'onglet est mal retenu (voir la gestion onkill de cordova)
1. [x] faire un 1er démarrage plus convivial avec une aide pour cliquer les icônes et plier-déplier les licences
1. [x] la coloration verte des icônes marche plus pour dropdown !
1. [x] essayer de comprendre pk sur android le dropdow menu se replie pas au toucher
