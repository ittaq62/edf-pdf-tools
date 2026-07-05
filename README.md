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
