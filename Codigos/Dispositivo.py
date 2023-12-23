import requests


class Dispositivo:
    def __init__(self, nombre_u):
        self.nombre_dispositivo = 'None'
        self.tipo = 'None'
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = nombre_u

    def reset_datos(self, nombre_u):
        self.nombre_dispositivo = 'None'
        self.tipo = 'None'
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = nombre_u

    def get_dispositivos(self, cur, url, headers, payload):
        response_device = requests.request("POST", url, headers=headers, data=payload)

        device_data = response_device.json()
        device_info = device_data['body']['devices']

        # nombre, tipo, ide_modelo,device_id,nombre_usuario
        if not device_info:
            print("no se ha obtenido datos sobre dispositivos del usuario.")
        else:
            for series in device_info:
                self.reset_datos(self.nombre_usuario) #resetear datos
                if 'model' in series:
                    self.nombre_dispositivo = series['model']
                if 'type' in series:
                    self.tipo = series['type']
                if 'model_id' in series:
                    self.id_modelo = series['model_id']
                if 'deviceid' in series:
                    self.id_dispositivo = series['deviceid']

                # guardamos los datos obtenidos en la base de datos
                # comprobamos si tenemos ya el dispositivo en la base de datos
                sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                cur.execute(sql)
                result = cur.fetchall()

                if not result:  # si no tenemos, guardamos directamente en la BD
                    # almacenar datos en la base de dato
                    # print("no tenemos datos en la BD, insertamos los datos")
                    # almacenar datos en la base de dato
                    sql = "INSERT INTO dispositivo(nombre_dispositivo,tipo, id_modelo, device_id, nombre_usuario) " \
                          "VALUES ( %s, %s, %s, %s, %s) "
                    val = (self.nombre_dispositivo, self.tipo, self.id_modelo, self.id_dispositivo, self.nombre_usuario)
                    cur.execute(sql, val)
                    print()
                    print("------------------------Datos de dispositivo almacenado------------------------------------")
                    print()
