from Medidas import *


class Suenio(Medidas):
    def __init__(self):
        super().__init__()
        self.id_suenio = 0
        self.id_modelo = 'None'
        self.startdate = '01-01-1990'
        self.enddate = '01-01-1990'
        self.wakeup_duration = 0
        self.wakeup_count = 0
        self.duration_to_wakeup = 0
        self.total_sleep_time = 0
        self.sleep_efficiency = 0
        self.sleep_latency = 0
        self.waso = 0
        self.light_sleep_duration = 0
        self.deep_sleep_duration = 0
        self.rem_sleep_duration = 0
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr = 0
        self.sleep_score = 0

    def reset_datos(self):
        super().reset_datos()
        self.id_suenio = 0
        self.id_modelo = 'None'
        self.startdate = '01-01-1990'
        self.enddate = '01-01-1990'
        self.wakeup_duration = 0
        self.wakeup_count = 0
        self.duration_to_wakeup = 0
        self.total_sleep_time = 0
        self.sleep_efficiency = 0
        self.sleep_latency = 0
        self.waso = 0
        self.light_sleep_duration = 0
        self.deep_sleep_duration = 0
        self.rem_sleep_duration = 0
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr = 0
        self.sleep_score = 0

    def get_datos_suenio(self, cur, url, headers, payload1, payload2):
        print()
        print("------------------------peticion de Suenio resumen------------------------------------")
        print()
        response_sleep_sum = requests.request("POST", url, headers=headers, data=payload1)

        sleep_sum_data = response_sleep_sum.json()
        sleep_sum_info = sleep_sum_data['body']['series']


        if not sleep_sum_info:
            print("no se ha obtenido datos sobre el suenio del usuario.")
        else:
            for series in sleep_sum_info:
                self.reset_datos() #resetear datos
                if 'id' in series:
                    self.id_suenio = series['id']
                if 'date' in series:
                    self.fecha = series['date']
                if 'model_id' in series:
                    self.id_modelo = series['model_id']
                if 'hash_deviceid' in series:
                    self.id_dispositivo = series['hash_deviceid']
                if 'startdate' in series:
                    t1 = series['startdate']
                    self.startdate = datetime.datetime.fromtimestamp(t1)
                if 'enddate' in series:
                    t2 = series['enddate']
                    self.enddate = datetime.datetime.fromtimestamp(t2)
                if 'created' in series:
                    t3 = series['created']
                    datas_time = datetime.datetime.fromtimestamp(t3)
                if 'data' in series:
                    datas = series['data']

                    if 'wakeupduration' in datas:
                        self.wakeup_duration = datas['wakeupduration']
                    if 'wakeupcount' in datas:
                        self.wakeup_count = datas['wakeupcount']
                    if 'durationtowakeup' in datas:
                        self.duration_to_wakeup = datas['durationtowakeup']
                    if 'total_sleep_time' in datas:
                        self.total_sleep_time = datas['total_sleep_time']
                    if 'sleep_efficiency' in datas:
                        self.sleep_efficiency = datas['sleep_efficiency']
                    if 'sleep_latency' in datas:
                        self.sleep_latency = datas['sleep_latency']
                    if 'waso' in datas:
                        self.waso = datas['waso']
                    if 'lightsleepduration' in datas:
                        self.light_sleep_duration = datas['lightsleepduration']
                    if 'deepsleepduration' in datas:
                        self.deep_sleep_duration = datas['deepsleepduration']
                    if 'remsleepduration' in datas:
                        self.rem_sleep_duration = datas['remsleepduration']
                    if 'hr_average' in datas:
                        self.hr_average = datas['hr_average']
                    if 'hr_min' in datas:
                        self.hr_min = datas['hr_min']
                    if 'hr_max' in datas:
                        self.hr_max = datas['hr_max']
                    if 'sleep_score' in datas:
                        self.sleep_score = datas['sleep_score']


                # almacenamiento de datos en BD
                # comprobamos si ya tenemos datos del mismo id en la base de datos
                sql = "SELECT * FROM suenio WHERE id_suenio = '{0}'".format(self.id_suenio)
                cur.execute(sql)
                result = cur.fetchall()
                # print('el resultado de la busquedad es ', result)
                if not result:  # si no tenemos, guardamos directamente en la BD
                    # almacenar datos en la base de dato
                    # print("no tenemos datos en la BD, insertamos los datos")

                    # 1.averiguamos el nombre del usuario mediante el id modelo obtenido del json
                    sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del usuario es None
                        print('no se ha encontrado dispositivo')
                    else:
                        for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                            self.nombre_usuario = nombre_usu

                    # 2.guardamos datos general
                    sql = "INSERT INTO suenio(id_suenio, date_suenio, model_id, device_id, startdate, enddate, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.id_suenio, self.fecha, self.id_modelo, self.id_dispositivo, self.startdate, self.enddate, self.nombre_usuario)
                    cur.execute(sql, val)

                    # 3.insertamos datos resumen del suenio
                    sql = "INSERT INTO datos_suenio(wakeup_duration, wakeup_count, duration_to_wakeup, total_sleep_time, sleep_efficiency, sleep_latency, waso, light_sleep_duration, deep_sleep_duration, rem_sleep_duration, hr_average, hr_min, hr_max, sleep_score, id_suenio) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.wakeup_duration, self.wakeup_count, self.duration_to_wakeup, self.total_sleep_time,
                           self.sleep_efficiency, self.sleep_latency, self.waso, self.light_sleep_duration,
                           self.deep_sleep_duration, self.rem_sleep_duration, self.hr_average, self.hr_min, self.hr_max,
                           self.sleep_score, self.id_suenio)
                    cur.execute(sql, val)

                    print('--------------------------------------------------------------')
                    print('Datos SUENIO almacenados')
                else:  # si ya tenemos datos con mismo id, no hacemos nada
                    # print('ya tenemos datos con este id, no hacemos nada')
                    pass

            print()
            print("          Datos de resumen suenio almacenados")
            print()
        # -----------------------------obtencion de datos de alta frecuencia ---------------------------------------
        print()
        print("------------------------peticion de Hr suenio------------------------------------")
        print()
        response_sleep = requests.request("POST", url, headers=headers, data=payload2)

        sleep_data = response_sleep.json()
        sleep_info = sleep_data['body']['series']

        if not sleep_info:
            print("no se ha obtenido datos sobre el suenio del usuario.")
        else:
            for series in sleep_info:
                if 'hr' in series:
                    self.id_modelo = series['model_id']
                    self.id_dispositivo = series['hash_deviceid']
                    hr_datas = series['hr']

                    # averiguamos el nombre del usuario mediante el id modelo obtenido del json
                    sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del usuario es None
                        print('no se ha encontrado dispositivo')
                    else:
                        for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                            self.nombre_usuario = nombre_usu
                    # obtenemos los valores de los hr de cada timestamp
                    for index, time in enumerate(hr_datas):
                        timestamp_hr = time
                        tiempo = datetime.datetime.fromtimestamp(float(timestamp_hr))
                        self.hr = hr_datas[time]

                        # guardamos los datos en la BD
                        sql = "INSERT INTO hr_suenio(time_hr, timestamp_hr, hr_suenio, id_suenio) VALUES ( %s, %s, %s, %s)"
                        val = (tiempo, timestamp_hr, self.hr, self.id_suenio)
                        cur.execute(sql, val)

            print()
            print("          Datos de Hr suenio almacenados          ")
            print()
