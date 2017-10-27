#coding: utf-8

from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
import zbar

from PIL import Image
import cv2
import requests
import socket

class Connected(Screen):
    def readcode(self):
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
    
    def requisition_code(self):
        readed_qrcode = self.readcode()
        try:
            r = requests.post("http://fast-retreat-18030.herokuapp.com/validate_qrcode", data={'qrcode': readed_qrcode})
            result = r.json()
            if result['status'] == 'bad_request':
                print result['errors']
            elif result['status'] == 'ok':
                print result['code']
                self.open_socket(str(result['code']))
        except:
            print("Não foi possível conectar ao servidor")

    def open_socket(self, message):
        IP = "127.0.0.1"
        PORT = 9600
    	TCP_IP = IP
        TCP_PORT = PORT
        BUFFER_SIZE = len(message)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        sock.send(message)
        data = sock.recv(100)
        sock.close()

    def __init__(self, **kwargs):
        self.requisition_code()


