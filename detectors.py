import cv2

# !/usr/bin/python
# Filename: face.py

class FaceDetector(object):
    def __init__(self, xml_path):
        # Create classifier object
        self.classifier = cv2.CascadeClassifier(xml_path)

    def detect(self, image, biggest_only=True):
        is_color = len(image) == 3
        if is_color:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image

        # Change to True if we want to detect only one face
        flags = cv2.CASCADE_FIND_BIGGEST_OBJECT | \
            cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else \
            cv2.CASCADE_SCALE_IMAGE

        face_coord = self.classifier.detectMultiScale(
            image_gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30,30),
            flags=flags
        )

        return face_coord




