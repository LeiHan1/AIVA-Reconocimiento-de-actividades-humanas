import unittest


class TestMockup(unittest.TestCase):
    def test_imports(self):
        import cv2
        import numpy
        import pandas
        import sklearn

    def test_read_video(self):
        import cv2
        cap = cv2.VideoCapture("/home/pixelabs/Vídeos/ShopAssistant2front.mpg")

        self.assertTrue(cap.isOpened())

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                self.assertTrue(frame is not None)
            else:
                self.assertTrue("Finished correctly")
                break

        cap.release()

    def test_preprocessing_images(self, frame):
        self.assertTrue(len(frame.shape) == 3)

    def test_get_contours(self, img):
        self.assertTrue(len(img.shape) == 2)

    def test_load_pedestrian_detector(self, path):
        import os
        self.assertTrue(os.path.exists(path))

    def test_classify_contours(self):
        self.fail()

    def test_save_results(self, results):
        self.assertTrue(results is not None)

if __name__ == '__main__':
    unittest.main()