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

from PIL import Image as ImagePIL


class ReadQRCodeScreen(Screen):

    def on_enter(self):

        #self.ids['lblQrCode'].text = "teste"
        print(self.ids)
        for item in self.ids:
            print(item)


        self.lblQRCode = self.ids['lblQrCode']
        self.imgCamera = self.ids['imgCamera']
        #self.imgCamera = Image(source='chopp.jpeg')
     
        #self.layout = BoxLayout(orientation='vertical')
        
        #self.add_widget(self.lblQRCode)
        #self.add_widget(self.imgCamera)

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

        teste = self.readQRCode(frame)

        
    
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
            print(decoded.data)
            #Clock.unschedule(self.updateImage)
            return decoded.data