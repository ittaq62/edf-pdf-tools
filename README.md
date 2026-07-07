# EDF PDF Tools

Outil interne de compression et de fusion de fichiers PDF.

## Fonctionnalités

- **Compression PDF** : Réduire la taille des fichiers PDF en ajustant la qualité des images
- **Fusion PDF** : Combiner plusieurs fichiers PDF en un seul document avec réorganisation

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Build (.exe)

```bash
python build.py
```

Le fichier exécutable sera généré dans le dossier `dist/`.

## Technologies

- Python 3.12
- PyQt6
- pypdf
- Pillow

## Historique des versions

### 1.4.0

- Nouveau niveau « Extrême » : les pages sont converties en images,
  pour un gain maximal sur les documents dont le poids vient des
  polices (exports Word, CV...). Le texte n'est alors plus
  sélectionnable, comme sur les compresseurs en ligne
- La structure des PDF est réécrite en flux d'objets compressés :
  les documents Office ne regonflent plus à la compression
- Description du niveau sélectionné affichée dans l'interface

### 1.3.1

- Les images PNG à canal de transparence opaque (standard des CV et
  exports bureautiques) sont désormais compressées : gains alignés
  sur les outils en ligne
- Une image qui ne gagne rien est conservée telle quelle, sans
  annuler les gains des autres images du fichier

### 1.3.0

- Correction : le nom des fichiers et l'estimation du gain
  n'apparaissaient pas dans la liste de compression
- Zone de dépôt mise en surbrillance pendant un glisser-déposer,
  avec fondu à l'apparition

### 1.2.0

- Gain de compression estimé et affiché en direct pour chaque fichier
  ajouté (pourcentage et octets économisés), recalculé selon le niveau
- Prise en charge des PDF protégés en modification, très courants en
  entreprise (l'origine des erreurs de compression en 1.1)
- Message clair pour les PDF exigeant un mot de passe, signalés avant
  même de lancer la compression
- Une page au contenu inhabituel n'interrompt plus le traitement du fichier
- Niveaux de compression plus contrastés

### 1.1.3

- Barre de titre sombre restaurée sur la fenêtre principale

### 1.1.2

- Menu déroulant affiché en liste simple, sans les marges du menu
  système

### 1.1.1

- Correction de l'affichage des listes déroulantes lorsque Windows
  est en thème sombre

### 1.1.0

- Écran de démarrage affiché dès le lancement, avec suivi du chargement
- Compression des images entièrement revue : recompression JPEG et
  redimensionnement selon le niveau choisi, gains nettement supérieurs
- Niveaux de compression réellement différenciés (légère / moyenne / forte)
- Un fichier compressé ne peut plus être plus volumineux que l'original
- Exécutable allégé et ouverture plus rapide

### 1.0.0

- Compression et fusion de fichiers PDF
- Interface aux couleurs EDF avec glisser-déposer
