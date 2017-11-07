#!/usr/local/bin/python
# coding: latin-1

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from kivy.graphics.texture import Texture

import cv2
import zbar
import requests
import socket

from PIL import Image as ImagePIL


class ReadQRCodeScreen(Screen):

    def on_enter(self):
        #"capturando" o widget de IMAGE para atualizar a imagem da camera
        self.imgCamera = self.ids['imgCamera']

        #criando um objeto de capture de video. Associamos a primeira camera
        self.capture = cv2.VideoCapture(0)
        #criando um frame com esta imagem
        ret, frame = self.capture.read()
        #criando um clock para atualizar a imagem a cada 1/320 de segundo
        Clock.schedule_interval(self.updateImage, 1.0/30.0)
 
    def updateImage(self, dt):
        
        #captura uma imagem da camera
        ret, frame = self.capture.read()
        #inverte a imagem
        buf1 = cv2.flip(frame, 0)
        #converte em textura
        buf = buf1.tostring() 
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        #apresenta a imagem
        self.imgCamera.texture = texture1

        #fazendo a leitura do QRCode
        qrCode = self.readQRCode(frame)

        #testa  se foi obtido algum valor do QRCode.
        #caso TRUE, faz a requisição e encerra a camera e os frames guardados.
        if not qrCode is None:
            self.requisition_code(qrCode)
            del(self.capture)
            cv2.destroyAllWindows()
        #    print "Teste 'is not None' " + qrCode
        #else:
        #    print "Teste 'is None'"
        
    def readQRCode(self, frame):
        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = ImagePIL.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # Prints data from image.
        for decoded in zbar_image:
            print("QRCode foi lido! => " + decoded.data)
            Clock.unschedule(self.updateImage)
            return decoded.data

    def requisition_code(self, qrCode):
        #readed_qrcode = self.readcode()
        readed_qrcode = qrCode
        print("QRCode passado para requisição = "+qrCode)

        #try:
        r = requests.post("http://fast-retreat-18030.herokuapp.com/validate_qrcode", data={'qrcode': readed_qrcode})
        result = r.json()

        if 'errors' in result:
            print("deu erro")
            print result['errors']
            self.manager.current = 'invalidQRCodeScreen'
        elif 'code' in result:
            print("deu certo")
            print result['code']
            self.open_socket(str(result['code']))
        #except:
         #   print("Não foi possível conectar ao servidor")

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
    
#    def __init__(self, *args):
#        self.requisition_code()

        # Teste para sair do while quando um qrcode for lido
        #if decoded.data is not None:
        #    break