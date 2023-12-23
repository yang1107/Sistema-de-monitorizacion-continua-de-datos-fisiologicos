import requests
import datetime


class Medidas:
    def __init__(self):
        self.fecha = '01-01-1900'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'

    def get_datos(self, cur, url, headers, payload):
        pass

    def reset_datos(self):
        self.fecha = '01-01-1900'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'
