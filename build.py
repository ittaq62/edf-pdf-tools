import subprocess
import sys


def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "EDF_PDF_Tools",
        "--icon", "Logo-EDF.png",
        "--add-data", "Logo-EDF.png;.",
        "main.py",
    ]

    print("Construction de l'exécutable...")
    print(f"Commande : {' '.join(cmd)}\n")

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\nBuild terminé avec succès !")
        print("L'exécutable se trouve dans le dossier dist/")
    else:
        print("\nErreur lors du build.")
        sys.exit(1)


if __name__ == "__main__":
    build()
