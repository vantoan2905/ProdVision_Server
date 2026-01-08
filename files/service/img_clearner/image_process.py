import cv2
import numpy as np


class ImageProcessService:
    def __init__(self):
        pass


    # =========================
    # NOISE REDUCTION
    # =========================
    def reduce_noise(self, image, strength=10):
        """
        Fix salt & pepper / mild noise
        """
        strength = max(3, min(strength, 15))
        return cv2.fastNlMeansDenoisingColored(
            image, None, strength, strength, 7, 21
        )


    # =========================
    # BRIGHTNESS / CONTRAST
    # =========================
    def adjust_brightness_contrast(self, image, brightness=0, contrast=0):
        """
        brightness: [-100, 100]
        contrast:   [-100, 100]
        """
        brightness = int(np.clip(brightness, -100, 100))
        contrast = int(np.clip(contrast, -100, 100))

        buf = image.copy()

        if brightness != 0:
            alpha = 1.0
            gamma = brightness
            buf = cv2.addWeighted(buf, alpha, buf, 0, gamma)

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            buf = cv2.addWeighted(buf, f, buf, 0, 127 * (1 - f))

        return buf


    # =========================
    # BLUR RECOVERY (SHARPEN)
    # =========================
    def blur_enhancement(self, image, strength=1.0):
        """
        Recover blur by unsharp masking
        """
        strength = max(0.3, min(strength, 2.0))

        blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=1.2)
        sharpened = cv2.addWeighted(
            image, 1 + strength, blurred, -strength, 0
        )
        return sharpened


    # =========================
    # FLIP
    # =========================
    def flip_image(self, image, mode="vertical"):
        """
        vertical = upside down
        horizontal = mirror
        """
        if mode == "horizontal":
            return cv2.flip(image, 1)
        elif mode == "vertical":
            return cv2.flip(image, 0)
        return image.copy()


    # =========================
    # SKEW CORRECTION
    # =========================
    def skew_correction(self, image, angle=None):
        """
        Deskew using minAreaRect
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        coords = np.column_stack(np.where(bw > 0))
        if len(coords) < 100:
            return image  

        if angle is None:
            angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        if abs(angle) < 0.5:
            return image  

        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        return cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
