import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from PIL import Image


QUALITY_PRESETS = {
    "Légère": {"image_quality": 80, "scale": 1.0},
    "Moyenne": {"image_quality": 50, "scale": 0.85},
    "Forte": {"image_quality": 25, "scale": 0.7},
}


def compress_pdf(input_path, output_path, quality_name="Moyenne", progress_callback=None):
    preset = QUALITY_PRESETS[quality_name]
    reader = PdfReader(input_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for i, page in enumerate(reader.pages):
        writer.add_page(page)

        if progress_callback:
            progress_callback(int((i + 1) / total_pages * 50))

    _compress_images(writer, preset, progress_callback, total_pages)

    for page in writer.pages:
        page.compress_content_streams()

    writer.remove_links()

    with open(output_path, "wb") as f:
        writer.write(f)

    if progress_callback:
        progress_callback(100)

    original_size = Path(input_path).stat().st_size
    compressed_size = Path(output_path).stat().st_size
    return original_size, compressed_size


def _compress_images(writer, preset, progress_callback, total_pages):
    image_count = 0
    images_processed = 0

    for page in writer.pages:
        if "/Resources" in page and "/XObject" in page["/Resources"]:
            xobjects = page["/Resources"]["/XObject"]
            for obj_name in xobjects:
                obj = xobjects[obj_name].get_object()
                if obj.get("/Subtype") == "/Image":
                    image_count += 1

    if image_count == 0:
        if progress_callback:
            progress_callback(90)
        return

    for page in writer.pages:
        if "/Resources" not in page or "/XObject" not in page["/Resources"]:
            continue

        xobjects = page["/Resources"]["/XObject"]
        for obj_name in xobjects:
            obj = xobjects[obj_name].get_object()
            if obj.get("/Subtype") != "/Image":
                continue

            try:
                width = int(obj["/Width"])
                height = int(obj["/Height"])

                new_w = max(1, int(width * preset["scale"]))
                new_h = max(1, int(height * preset["scale"]))

                data = obj.get_data()
                color_space = obj.get("/ColorSpace", "/DeviceRGB")

                if isinstance(color_space, list):
                    color_space = str(color_space[0])
                else:
                    color_space = str(color_space)

                if "/DeviceCMYK" in color_space:
                    mode = "CMYK"
                elif "/DeviceGray" in color_space:
                    mode = "L"
                else:
                    mode = "RGB"

                bits = int(obj.get("/BitsPerComponent", 8))
                if bits != 8:
                    images_processed += 1
                    continue

                expected_size = width * height * (len(mode))
                if len(data) < expected_size:
                    images_processed += 1
                    continue

                img = Image.frombytes(mode, (width, height), data[:expected_size])
                if img.mode == "CMYK":
                    img = img.convert("RGB")

                if preset["scale"] < 1.0:
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=preset["image_quality"], optimize=True)
                compressed_data = buffer.getvalue()

                obj._data = compressed_data
                obj["/Filter"] = "/DCTDecode"
                obj["/Width"] = new_w
                obj["/Height"] = new_h
                obj["/ColorSpace"] = "/DeviceRGB"
                obj["/BitsPerComponent"] = 8
                obj["/Length"] = len(compressed_data)
            except Exception:
                pass

            images_processed += 1
            if progress_callback and image_count > 0:
                progress = 50 + int(images_processed / image_count * 40)
                progress_callback(min(progress, 90))


def merge_pdfs(input_paths, output_path, progress_callback=None):
    writer = PdfWriter()
    total = len(input_paths)

    for i, path in enumerate(input_paths):
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

        if progress_callback:
            progress_callback(int((i + 1) / total * 90))

    with open(output_path, "wb") as f:
        writer.write(f)

    if progress_callback:
        progress_callback(100)

    return Path(output_path).stat().st_size
