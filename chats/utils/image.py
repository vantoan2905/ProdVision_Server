import base64
import io
import numpy as np
from PIL import Image


def tensor_to_base64(tensor: np.ndarray) -> str:
    """
    Convert image tensor (H, W, C) to base64 PNG string.
    """
    if tensor.dtype != np.uint8:
        tensor = tensor.astype("uint8")

    image = Image.fromarray(tensor)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")
