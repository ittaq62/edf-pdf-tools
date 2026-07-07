import io
import shutil
from pathlib import Path


QUALITY_PRESETS = {
    "Légère": {"quality": 80, "max_dimension": 2600},
    "Moyenne": {"quality": 55, "max_dimension": 1600},
    "Forte": {"quality": 30, "max_dimension": 1000},
}

# En dessous de cette surface, une image ne pèse presque rien :
# la retraiter n'apporte aucun gain visible
MIN_IMAGE_PIXELS = 10_000


class PdfProtegeError(Exception):
    """PDF exigeant un mot de passe pour être ouvert."""


def compress_pdf(input_path, output_path, quality_name="Moyenne", progress_callback=None):
    buffer, original_size = _compress_to_buffer(input_path, quality_name, progress_callback)
    compressed_size = buffer.getbuffer().nbytes

    # Un PDF déjà optimisé ressortirait plus lourd : on garde alors l'original
    if compressed_size >= original_size:
        shutil.copyfile(input_path, output_path)
        compressed_size = original_size
    else:
        with open(output_path, "wb") as f:
            f.write(buffer.getbuffer())

    if progress_callback:
        progress_callback(100)

    return original_size, compressed_size


def estimate_compression(input_path, quality_name="Moyenne"):
    """Taille attendue après compression, sans rien écrire sur le disque."""
    buffer, original_size = _compress_to_buffer(input_path, quality_name, None)
    estimated_size = min(buffer.getbuffer().nbytes, original_size)
    return original_size, estimated_size


def _compress_to_buffer(input_path, quality_name, progress_callback):
    from pypdf import PdfReader, PdfWriter

    preset = QUALITY_PRESETS[quality_name]

    reader = PdfReader(input_path)
    _dechiffrer_si_necessaire(reader)

    writer = PdfWriter(clone_from=reader)
    if progress_callback:
        progress_callback(5)

    _recompress_images(writer, preset, progress_callback)

    for page in writer.pages:
        try:
            page.compress_content_streams(level=9)
        except Exception:
            # Un flux de contenu inhabituel ne doit pas faire échouer le fichier
            pass

    try:
        writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    except Exception:
        pass

    if progress_callback:
        progress_callback(92)

    buffer = io.BytesIO()
    writer.write(buffer)

    original_size = Path(input_path).stat().st_size
    return buffer, original_size


def _dechiffrer_si_necessaire(reader):
    """Les PDF « protégés en modification » (mot de passe utilisateur vide,
    très courants en entreprise) s'ouvrent de façon transparente. Seuls les
    PDF exigeant un vrai mot de passe sont refusés, avec un message clair."""
    if not reader.is_encrypted:
        return
    try:
        result = reader.decrypt("")
    except Exception as exc:
        raise PdfProtegeError(
            "ce PDF utilise un chiffrement non pris en charge"
        ) from exc
    if int(result) == 0:
        raise PdfProtegeError(
            "ce PDF est protégé par un mot de passe, il ne peut pas être traité"
        )


def _recompress_images(writer, preset, progress_callback):
    page_image_lists = []
    total = 0
    for page in writer.pages:
        try:
            images = page.images
            count = len(images)
        except Exception:
            continue
        page_image_lists.append((images, count))
        total += count

    if total == 0:
        return

    done = 0
    for images, count in page_image_lists:
        for index in range(count):
            done += 1
            try:
                _recompress_single(images[index], preset)
            except Exception:
                # Une image illisible ne doit pas faire échouer tout le fichier
                pass
            if progress_callback:
                progress_callback(5 + int(done / total * 82))


def _recompress_single(image_file, preset):
    from PIL import Image

    pil_image = image_file.image
    if pil_image is None:
        return

    width, height = pil_image.size
    if width * height < MIN_IMAGE_PIXELS:
        return

    # Les images à palette, avec transparence ou en noir et blanc 1 bit
    # se dégradent ou grossissent en JPEG : on ne touche pas
    if pil_image.mode in ("RGB", "L"):
        processed = pil_image
    elif pil_image.mode == "CMYK":
        processed = pil_image.convert("RGB")
    else:
        return

    max_dim = preset["max_dimension"]
    ratio = min(1.0, max_dim / max(width, height))
    if ratio < 1.0:
        new_size = (max(1, round(width * ratio)), max(1, round(height * ratio)))
        processed = processed.resize(new_size, Image.Resampling.LANCZOS)

    image_file.replace(processed, quality=preset["quality"], optimize=True)


def merge_pdfs(input_paths, output_path, progress_callback=None):
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    total = len(input_paths)

    for i, path in enumerate(input_paths):
        reader = PdfReader(path)
        _dechiffrer_si_necessaire(reader)
        for page in reader.pages:
            writer.add_page(page)

        if progress_callback:
            progress_callback(int((i + 1) / total * 90))

    with open(output_path, "wb") as f:
        writer.write(f)

    if progress_callback:
        progress_callback(100)

    return Path(output_path).stat().st_size
