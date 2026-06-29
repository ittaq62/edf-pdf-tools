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
