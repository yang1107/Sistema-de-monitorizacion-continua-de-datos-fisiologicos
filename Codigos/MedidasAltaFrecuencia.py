import requests
import datetime


class MedidasAltaFrecuencia:
    def __init__(self):
        self.nombre_dispositivo = 'None'
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'
        self.heart_rate = 0
        self.calorias = 0
        self.spo2 = 0
        self.paso = 0
        self.elevacion = 0
        self.distancia = 0

    def reset_datos(self):
        self.nombre_dispositivo = 'None'
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'
        self.heart_rate = 0
        self.calorias = 0
        self.spo2 = 0
        self.paso = 0
        self.elevacion = 0
        self.distancia = 0

    def get_datos(self, cur, url, headers, payload):
        print()
        print("------------------------peticion de Medidas de alta frecuencia------------------------------------")
        print()
        response_high = requests.request("POST", url, headers=headers, data=payload)

        high_data = response_high.json()
        high_info = high_data['body']['series']

        if not high_info:
            print("no se ha obtenido datos de alta frecuencia del usuario.")
        else:
            for timestamps in high_info:
                self.reset_datos() #resetear datos
                tiempo = timestamps
                time_data = datetime.datetime.fromtimestamp(int(tiempo))
                datas = high_info[timestamps]

                if 'model' in datas:
                    self.nombre_dispositivo = datas['model']
                if 'model_id' in datas:
                    self.id_modelo = datas['model_id']
                if 'deviceid' in datas:
                    self.id_dispositivo = datas['deviceid']
                if 'distance' in datas:
                    self.distancia = datas['distance']
                if 'spo2_auto' in datas:
                    self.spo2 = datas['spo2_auto']
                if 'heart_rate' in datas:
                    self.heart_rate = datas['heart_rate']
                if 'elevation' in datas:
                    self.elevacion = datas['elevation']
                if 'steps' in datas:
                    self.paso = datas['steps']
                if 'calories' in datas:
                    self.calorias = datas['calories']

                # almacenamiento de datos

                # averiguamos el nombre del usuario mediante deviceid obtenido del json
                sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                cur.execute(sql)
                result = cur.fetchall()
                if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del dispositivo es None
                    print('no se ha encontrado dispositivo')
                else:
                    for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                        self.nombre_usuario = nombre_usu

                # distancia
                # comprobamos si tenemos datos
                if self.distancia != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM distancia WHERE timestamp_distancia = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO distancia(time_distancia, timestamp_distancia, nombre_dispositivo, model_id, device_id, distancia, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.distancia, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos distancia')

                # heart_rate
                # comprobamos si tenemos datos
                if self.heart_rate != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM heart_rate WHERE timestamp_heart_rate = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO heart_rate(time_heart_rate, timestamp_heart_rate, nombre_dispositivo, model_id, device_id, heart_rate, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo,
                               self.heart_rate, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos hr')

                # spo2
                # comprobamos si tenemos datos
                if self.spo2 != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM spo2 WHERE timestamp_spo2 = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO spo2(time_spo2, timestamp_spo2, nombre_dispositivo, model_id, device_id, spo2, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.spo2, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos spo2')

                # elevacion
                # comprobamos si tenemos datos
                if self.elevacion != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM elevacion WHERE timestamp_elevacion = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO elevacion(time_elevacion, timestamp_elevacion, nombre_dispositivo, model_id, device_id, elevacion, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.elevacion, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos elevacion')

                # pasos
                # comprobamos si tenemos datos
                if self.paso != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM pasos WHERE timestamp_pasos = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO pasos(time_pasos, timestamp_pasos, nombre_dispositivo, model_id, device_id, pasos, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.paso, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos pasos')

                # calorias
                # comprobamos si tenemos datos
                if self.calorias != 0:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM calorias WHERE timestamp_calorias = '{0}'".format(tiempo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato
                        # print("no tenemos dados en la BD, insertamos los datos")
                        # guardamos datos en la tabla
                        sql = "INSERT INTO calorias(time_calorias, timestamp_calorias, nombre_dispositivo, model_id, device_id, calorias, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                        val = (time_data, tiempo, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.calorias, self.nombre_usuario)
                        cur.execute(sql, val)
                    else:  # si ya tenemos datos con mismo id, no hacemos nada
                        # print('ya tenemos datos con este tiempo, no hacemos nada')
                        pass
                else:
                    print('no hay datos calorias')

            print()
            print("          Datos de Alta frecuencia almacenados          ")
            print()
