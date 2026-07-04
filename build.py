import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

from version import APP_VERSION

SPLASH_SIZE = (420, 260)


def make_splash():
    """Genere l'image de l'ecran de demarrage a partir du logo."""
    logo = Image.open("Logo-EDF.png").convert("RGBA")
    logo.thumbnail((280, 130), Image.Resampling.LANCZOS)

    splash = Image.new("RGB", SPLASH_SIZE, "white")
    splash.paste(logo, ((SPLASH_SIZE[0] - logo.width) // 2, 45), logo)

    draw = ImageDraw.Draw(splash)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        font = ImageFont.load_default()
        small_font = font

    title = "PDF Tools"
    title_width = draw.textlength(title, font=font)
    draw.text(((SPLASH_SIZE[0] - title_width) / 2, 188), title, fill="#003DA5", font=font)

    version = f"v{APP_VERSION}"
    version_width = draw.textlength(version, font=small_font)
    draw.text((SPLASH_SIZE[0] - version_width - 12, 10), version, fill="#AAAAAA", font=small_font)

    draw.line([(20, 228), (SPLASH_SIZE[0] - 20, 228)], fill="#DDDDDD", width=1)
    draw.rectangle([0, 0, SPLASH_SIZE[0] - 1, SPLASH_SIZE[1] - 1], outline="#CCCCCC")

    splash.save("splash.png")
    print("splash.png genere")


def build():
    make_splash()

    cmd = [sys.executable, "-m", "PyInstaller", "EDF_PDF_Tools.spec", "--noconfirm"]
    print("Construction de l'executable...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\nBuild termine ! Executable disponible dans dist/")
    else:
        print("\nErreur lors du build.")
        sys.exit(1)


if __name__ == "__main__":
    build()
