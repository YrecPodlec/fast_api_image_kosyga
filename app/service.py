import cv2
import numpy as np
from io import BytesIO
from fastapi import UploadFile


def hex_to_bgr(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)


async def process_image(
    file: UploadFile,
    threshold1: int,
    threshold2: int,
    blur: int,
    thickness: int,
    min_area: int,
    color: str,
    mode: str,
):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Не удалось прочитать изображение")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if blur % 2 == 0:
        blur += 1
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)

    if mode == "grayscale":
        result = gray

    elif mode == "binary":
        _, result = cv2.threshold(
            blurred, threshold1, 255, cv2.THRESH_BINARY
        )

    elif mode == "edges":
        edges = cv2.Canny(blurred, threshold1, threshold2)
        kernel = np.ones((3, 3), np.uint8)
        result = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

    elif mode == "contours":
        edges = cv2.Canny(blurred, threshold1, threshold2)

        kernel = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv2.findContours(
            closed,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        filtered = [c for c in contours if cv2.contourArea(c) > min_area]

        color_bgr = hex_to_bgr(color)
        result = image.copy()
        cv2.drawContours(result, filtered, -1, color_bgr, thickness)

    else:
        result = image

    if len(result.shape) == 2:
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    success, buffer = cv2.imencode(".png", result)
    if not success:
        raise ValueError("Ошибка кодирования изображения")

    return BytesIO(buffer.tobytes())