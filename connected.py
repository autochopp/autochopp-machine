from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
import zbar

from PIL import Image
import cv2

class Connected(Screen):
    def readcode(self):
        print ('dsadadasdasdasdsad')
        # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
        # to be your webcam.
        capture = cv2.VideoCapture(0)

        while True:
            # To quit this program press q.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Breaks down the video into frames
            ret, frame = capture.read()

            # Displays the current frame
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.imshow('image', frame)
            cv2.resizeWindow('image', 400,400)
            # cv2.destroyAllWindows()

            # Converts image to grayscale.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
            image = Image.fromarray(gray)
            width, height = image.size
            zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

            # Scans the zbar image.
            scanner = zbar.ImageScanner()
            scanner.scan(zbar_image)

            # Prints data from image.
            for decoded in zbar_image:
                print(decoded.data)
                return decoded.data
        
        # def requisitonApi(self):
            

    def __init__(self, **kwargs):
        # super(Screen,self).__init__(**kwargs)
        self.readcode()


