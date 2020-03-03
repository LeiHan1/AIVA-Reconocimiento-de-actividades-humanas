import unittest


class Test_aiva(unittest.TestCase):

    def test_import(self):
        import cv2
        import numpy
        import pandas
        import sklearn


    def test_read_video(self):
        import cv2
        cap = cv2.VideoCapture("/home/pixelabs/Vídeos/ShopAssistant2front.mpg")

        self.assertTrue(cap.isOpened())

        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                self.assertTrue(frame is not None)
            else:
                self.assertTrue("Finished correctly")
                break

        # When everything done, release the video capture object
        cap.release()

if __name__ == '__main__':
    unittest.main()