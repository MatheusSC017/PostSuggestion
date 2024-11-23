import io

from PIL import Image


def genenerate_image_bytes():
    image = Image.new("RGB", (1024, 1024), color="white")

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    image_byte_data = image_bytes.getvalue()
    return image_byte_data
