import requests
import datetime
from funciones import *


class Ecg:
    def __init__(self):
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'
        self.nombre_dispositivo = 'None'
        self.id_senial = 0
        self.senial = 0
        self.qrs = 0
        self.qt = 0
        self.pr = 0
        self.qtc = 0
        self.heart_rate = 0

    def reset_datos(self):
        self.id_modelo = 'None'
        self.id_dispositivo = 'None'
        self.nombre_usuario = 'None'
        self.nombre_dispositivo = 'None'
        self.id_senial = 0
        self.senial = 0
        self.qrs = 0
        self.qt = 0
        self.pr = 0
        self.qtc = 0
        self.heart_rate = 0

    def get_datos(self, cur, url, url2, headers, payload):
        print()
        print("------------------------peticion de ECG------------------------------------")
        print()
        response_ecg = requests.request("POST", url, headers=headers, data=payload)
        ecg_data = response_ecg.json()
        ecg_info = ecg_data['body']['series']

        if not ecg_info:
            print("no se ha obtenido datos sobre ecg del usuario.")
        else:
            for series in ecg_info:
                self.reset_datos() #resetear datos
                if 'timestamp' in series:
                    t1 = series['timestamp']
                    time_ecg = datetime.datetime.fromtimestamp(t1)
                if 'model' in series:
                    self.id_modelo = series['model']
                if 'deviceid' in series:
                    self.id_dispositivo = series['deviceid']
                if 'ecg' in series:
                    self.id_senial = series['ecg']['signalid']
                if 'heart_rate' in series:
                    self.heart_rate = series['heart_rate']


                # solicitamos datos de los qrs, qt, pr, qtc con getmeas
                time_start = t1
                time_end = time_start + 14400
                payload_ini = 'action=getmeas&meastype=135%2C136%2C137%2C138&category=1&startdate=0&enddate=0'
                payload_ecg2 = changepayload_time(payload_ini, time_start, time_end)
                response_ecg2 = requests.request("POST", url2, headers=headers, data=payload_ecg2)

                ecg2_data = response_ecg2.json()
                ecg2_info = ecg2_data['body']['measuregrps']

                if not ecg2_info:
                    print("no se ha obtenido datos del usuario.")
                else:
                    for serie in ecg2_info:
                        for series_data in serie['measures']:
                            if series_data['type'] == 135:
                                self.qrs = series_data['value']
                            elif series_data['type'] == 136:
                                self.pr = series_data['value']
                            elif series_data['type'] == 137:
                                self.qt = series_data['value']
                            elif series_data['type'] == 138:
                                self.qtc = series_data['value']

                        # almacenamos datos en BD
                        # comprobamos si ya tenemos datos con la misma senial en la base de datos
                        sql = "SELECT * FROM ecg WHERE signal_id = '{0}'".format(self.id_senial)
                        cur.execute(sql)
                        result = cur.fetchall()
                        if not result:  # si no tenemos, guardamos directamente en la BD
                            # almacenar datos en la base de dato
                            # print("no tenemos dados en la BD, insertamos los datos")
                            pass

                            # 1
                            # .averiguamos el nombre del usuario mediante modelid obtenido del json
                            sql = "SELECT * FROM dispositivo WHERE id_modelo = '{0}'".format(self.id_modelo)
                            cur.execute(sql)
                            result = cur.fetchall()
                            if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del dispositivo es None
                                print('no se ha encontrado dispositivo')
                            else:
                                for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                                    self.nombre_usuario = nombre_usu

                            # 2. guardamos datos de ecg en la tabla
                            sql = "INSERT INTO ecg(time_ecg, model_id, signal_id, qrs, qt, pr, qtc, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (time_ecg, self.id_modelo, self.id_senial, self.qrs, self.qt, self.pr, self.qtc, self.nombre_usuario)
                            cur.execute(sql, val)

                            # guardamos datos de senial ecg
                            payload_signal_ini = 'action=get&signalid=0'

                            # modificamos el id_signal del payload
                            prop_signal = {}
                            new_payload_signal = payload_signal_ini.split('&')

                            for item in new_payload_signal:
                                key, value = item.split('=')
                                if key == 'signalid':
                                    value = self.id_senial
                                prop_signal[key] = value

                            payload_signal = '&'.join([key + '=' + str(value) for key, value in prop_signal.items()])
                            response_signal = requests.request("POST", url, headers=headers, data=payload_signal)

                            signal_data = response_signal.json()
                            signal_info = signal_data['body']


                            if not signal_info:
                                print("no se ha obtenido datos sobre senial ecg del usuario.")
                            else:
                                seniales = signal_info['signal']
                                time1 = t1
                                time_signal = datetime.datetime.fromtimestamp(time1)
                                time_increment = 1 / 300
                                for signal_data in seniales:
                                    # guardamos datos en la bd
                                    sql = "INSERT INTO senial_ecg(time_senial, signal_id, valor_senial) VALUES ( %s, %s, %s)"
                                    val = (time_signal, self.id_senial, signal_data)
                                    cur.execute(sql, val)
                                    time1 = time1 + time_increment
                                    time_signal = datetime.datetime.fromtimestamp(time1)
                                print()
                                print("          Datos de senial ecg almacenados          ")
                                print()
                        else:  # si ya tenemos datos con mismo id, no hacemos nada
                            # print('ya tenemos datos con este id, no hacemos nada')
                            pass

                        # guardamos datos de heart_rate obtenido
                        if self.heart_rate != 0:
                            # comprobamos si ya hay datos de heart rate con el mismo timestamp
                            sql = "SELECT * FROM heart_rate WHERE timestamp_heart_rate = '{0}'".format(t1)
                            # print("timestamp a comprobar es ", t1)
                            cur.execute(sql)
                            result = cur.fetchall()
                            # print('el resultado de la busquedad es ', result)
                            if not result:  # si no tenemos, guardamos directamente en la BD
                                # print("no tenemos dados en la BD, insertamos los datos hr")
                                # averiguamos el nombre del dispositivo mediante deviceid obtenido del json
                                sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                                cur.execute(sql)
                                result = cur.fetchall()
                                if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del dispositivo es None
                                    print('no se ha encontrado dispositivo')
                                else:
                                    for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                                        # print (id, nombre_disp, tipo, id_modelo, device_id, nombre_usu)
                                        self.nombre_dispositivo = nombre_disp

                                sql = "INSERT INTO heart_rate(time_heart_rate, timestamp_heart_rate, nombre_dispositivo, model_id, device_id, heart_rate, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                                val = (time_ecg, t1, self.nombre_dispositivo, self.id_modelo, self.id_dispositivo, self.heart_rate, self.nombre_usuario)
                                cur.execute(sql, val)
                            else:  # si ya tenemos datos con mismo id, no hacemos nada
                                # print('ya tenemos datos de heart_rate con este timestamp, no hacemos nada')
                                pass
                        else:
                            # print('no hay datos de hr vinculada con este signal id')
                            pass
