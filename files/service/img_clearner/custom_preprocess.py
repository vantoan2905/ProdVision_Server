import cv2
import numpy as np
from typing import Dict

from defect_detection import DefectDetectionService
from image_process import ImageProcessService


class ImgCleanerService(DefectDetectionService, ImageProcessService):
    def __init__(self):
        DefectDetectionService.__init__(self)
        ImageProcessService.__init__(self)


    def check_image(self, image: np.ndarray) -> Dict:
        return self.check_defects(image)


    def enhance_image(self, image: np.ndarray) -> np.ndarray:

        report = self.check_defects(image)
        fixed = image.copy()

        if "flip" in report["fixable_defects"]:
            fixed = self.flip_image(fixed, mode="vertical")

        if "skew" in report["fixable_defects"]:
            angle = report["skew"]["skew_angle"]
            fixed = self.skew_correction(fixed, angle)

        if "sat_noise" in report["fixable_defects"]:
            fixed = self.reduce_noise(fixed)

        if "blur" in report["fixable_defects"]:
            fixed = self.blur_enhancement(fixed, strength=1.0)

        if report["lighting"]["is_bad_dark"]:
            fixed = self.adjust_brightness_contrast(fixed, brightness=25)

        if report["lighting"]["is_bad_light"]:
            fixed = self.adjust_brightness_contrast(fixed, brightness=-15)

        return fixed
