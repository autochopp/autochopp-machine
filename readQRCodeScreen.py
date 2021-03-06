#!/usr/local/bin/python
# coding: latin-1

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from embedded_electronics import MachineController

import cv2
import zbar
import requests
import socket
import time

from PIL import Image as ImagePIL


class ReadQRCodeScreen(Screen):

    machine = MachineController()

    def on_enter(self):
        #"capturando" o widget de IMAGE para atualizar a imagem da camera
        self.img_camera = self.ids['img_camera']

        # criando um objeto de capture de video. Associamos a primeira camera
        self.capture = cv2.VideoCapture(0)
        # criando um frame com esta imagem
        ret, frame = self.capture.read()
        #criando um clock para atualizar a imagem a cada 1/320 de segundo
        Clock.schedule_interval(self.update_image, 1.0/30.0)

    def update_image(self, dt):
        #captura uma imagem da camera
        ret, frame = self.capture.read()
        # inverte a imagem
        buf1 = cv2.flip(frame, 0)
        #converte em textura
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        #apresenta a imagem
        self.img_camera.texture = texture1

        #fazendo a leitura do QRCode
        qrCode = self.read_qr_code(frame)

        # testa  se foi obtido algum valor do QRCode.
        # caso TRUE, faz a requisição e encerra a camera e os frames guardados.
        if not qrCode is None:
            del(self.capture)
            cv2.destroyAllWindows()
            self.requisition_code(qrCode)

    def read_qr_code(self, frame):
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
            Clock.unschedule(self.update_image)
            return decoded.data

    def requisition_code(self, qrCode):
        #readed_qrcode = self.readcode()
        readed_qrcode = qrCode
        print("QRCode passado para requisição = "+qrCode)

        try: 
            r = requests.post("http://fast-retreat-18030.herokuapp.com/validate_qrcode", data={'qrcode': readed_qrcode})
            result = r.json()

            if 'errors' in result:
                print("Error: ")
                print result['errors']
                self.manager.current = 'invalidQRCodeScreen'
                    
            elif 'code' in result:
                print("Success: ")
                print result['code']
                self.manager.current = 'validQRCodeScreen'
                self.machine.set_chopp(result['code'])
                Clock.schedule_once(self.wait_cup, 1)
        except:
            self.manager.current = 'exceptionScreen'
 
    def wait_cup(self, dt):
        if self.machine.is_drawer_open() == True:
            self.manager.current = 'waitCup'
            print "WaitCup"
            Clock.schedule_once(self.wait_chopp)

    def wait_chopp(self, dt):
        if self.machine.cup_activate() == True:
            print "WaitChopp"
            self.manager.current = 'waitChopp'
            Clock.schedule_once(self.success_chopp)
        elif self.machine.cup_activate() == False:
            self.manager.current = 'main' 

    def success_chopp(self, dt):
        if self.machine.already_got_beer() == True:
            print "sucess Chopp"
            self.manager.current = 'successChopp'
