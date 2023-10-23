from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from rembg import remove
import cv2
from typing import Tuple

    
def scale_brightness(image: np.ndarray, factor: float) -> np.ndarray:
    image = Image.fromarray(image)
    image = ImageEnhance.Brightness(image).enhance(factor)
    image = np.array(image)
    return image


def scale_contrast(image: np.ndarray, factor: float) -> np.ndarray:
    image = Image.fromarray(image)
    image = ImageEnhance.Contrast(image).enhance(factor)
    image = np.array(image)
    return image


def scale_blurness(image: np.ndarray, factor: float) -> np.ndarray:
    radius = factor * 10
    image = Image.fromarray(image)
    image = image.filter(ImageFilter.GaussianBlur(radius))
    image = np.array(image)
    return image


def scale_sharpness(image: np.ndarray, factor: float) -> np.ndarray:
    percent = factor * 100
    image = Image.fromarray(image)
    image = image.filter(ImageFilter.UnsharpMask(percent))
    image = np.array(image)
    return image


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    image = Image.fromarray(image)
    image = image.convert("L")
    image = image.convert("RGB")
    image = np.array(image)
    return image


def convert_to_negative(image: np.ndarray) -> np.ndarray:
    image = 255 - image
    return image


def erase(image: np.ndarray) -> np.ndarray:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image[:, :, 3] = 0
    return image


def horizontal_flip(image: np.ndarray) -> np.ndarray:
    return cv2.flip(image, 1)


def vertical_flip(image: np.ndarray) -> np.ndarray:
    return cv2.flip(image, 0)


def rotate_clockwise(image: np.ndarray, angle: float) -> np.ndarray:
    return rotate_counter_clockwise(image, -angle)


def rotate_counter_clockwise(image: np.ndarray, angle: float) -> np.ndarray:
    image = Image.fromarray(image)
    image = image.rotate(angle=angle, expand=True)
    image = np.array(image)
    return image


def zoom(image: np.ndarray, factor: float, pivot) -> np.ndarray:
    """
    Zoom the input image around a pivot point by a given factor.

    :param image: Input image (NumPy ndarray).
    :param pivot: Pivot point as a tuple (x, y).
    :param factor: Zoom factor (e.g., 1.5 for 1.5x zoom).
    :return: Zoomed image (NumPy ndarray).
    """
    
    height, width = image.shape[0], image.shape[1]

    # Calculate the pivot point in the image coordinates.
    pivot_x, pivot_y = pivot

    # Create an affine transformation matrix for the zoom.
    matrix = np.array([[factor, 0, (1 - factor) * pivot_x],
                       [0, factor, (1 - factor) * pivot_y]])

    # Apply the transformation using cv2.warpAffine.
    zoomed_image = cv2.warpAffine(image, matrix, (width, height))

    return zoomed_image


def forebackground_segment(image: np.ndarray) -> np.ndarray:
    fg_mask = remove(image, alpha_matting=True, only_mask=True, post_process_mask=True)
    bg_mask = 255 - fg_mask
    return {
        "foreground": fg_mask, 
        "background": bg_mask
    }

