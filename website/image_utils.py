from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def optimize_uploaded_image(instance, field_name, max_size=(1600, 1200), quality=82):
    """Convert a newly uploaded image to a reasonably sized WebP file."""
    image_field = getattr(instance, field_name, None)
    if not image_field or getattr(image_field, "_committed", True):
        return

    image_field.file.seek(0)
    with Image.open(image_field.file) as source:
        image = ImageOps.exif_transpose(source)
        has_alpha = image.mode in {"RGBA", "LA"} or "transparency" in image.info
        image = image.convert("RGBA" if has_alpha else "RGB")
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        output = BytesIO()
        image.save(output, format="WEBP", quality=quality, method=6)

    filename = f"{Path(image_field.name).stem}.webp"
    image_field.save(filename, ContentFile(output.getvalue()), save=False)
