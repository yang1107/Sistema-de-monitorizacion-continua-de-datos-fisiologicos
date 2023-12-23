from Medidas import *


class Entrenamiento(Medidas):
    def __init__(self):
        super().__init__()
        self.id_entrenamiento = 0
        self.startdate = '01-01-1900'
        self.enddate = '01-01-1900'
        self.id_modelo = 'None'
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr_zone_0 = 0
        self.hr_zone_1 = 0
        self.hr_zone_2 = 0
        self.hr_zone_3 = 0
        self.elevacion = 0
        self.paso = 0
        self.spo2_average = 0
        self.distancia = 0
        self.calorias = 0

    def reset_datos(self):
        super().reset_datos()
        self.id_entrenamiento = 0
        self.startdate = '01-01-1900'
        self.enddate = '01-01-1900'
        self.id_modelo = 'None'
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr_zone_0 = 0
        self.hr_zone_1 = 0
        self.hr_zone_2 = 0
        self.hr_zone_3 = 0
        self.elevacion = 0
        self.paso = 0
        self.spo2_average = 0
        self.distancia = 0
        self.calorias = 0

    def get_datos(self, cur, url, headers, payload):
        print()
        print("------------------------peticion de Entrenamiento------------------------------------")
        print()
        response_workouts = requests.request("POST", url, headers=headers, data=payload)

        workouts_data = response_workouts.json()
        workouts_info = workouts_data['body']['series']

        if not workouts_info:
            print("no se ha obtenido datos sobre actividad del usuario.")
        else:
            for series in workouts_info:
                self.reset_datos() #resetear datos
                if 'id' in series:
                    self.id_entrenamiento = series['id']
                if 'date' in series:
                    self.fecha = series['date']
                if 'startdate' in series:
                    t1 = series['startdate']
                    self.startdate = datetime.datetime.fromtimestamp(t1)
                if 'enddate' in series:
                    t2 = series['enddate']
                    self.enddate = datetime.datetime.fromtimestamp(t2)
                if 'deviceid' in series:
                    self.id_dispositivo = series['deviceid']
                if 'modified' in series:
                    t3 = series['modified']
                    datas_time = datetime.datetime.fromtimestamp(t3)
                if 'model' in series:
                    self.id_modelo = series['model']
                if 'data' in series:
                    datas = series['data']

                if 'elevation' in datas:
                    self.elevacion = datas['elevation']
                if 'calories' in datas:
                    self.calorias = datas['calories']
                if 'hr_average' in datas:
                    self.hr_average = datas['hr_average']
                if 'hr_min' in datas:
                    self.hr_min = datas['hr_min']
                if 'hr_max' in datas:
                    self.hr_max = datas['hr_max']
                if 'hr_zone_0' in datas:
                    self.hr_zone_0 = datas['hr_zone_0']
                if 'hr_zone_1' in datas:
                    self.hr_zone_1 = datas['hr_zone_1']
                if 'hr_zone_2' in datas:
                    self.hr_zone_2 = datas['hr_zone_2']
                if 'hr_zone_3' in datas:
                    self.hr_zone_3 = datas['hr_zone_3']
                if 'spo2_average' in datas:
                    self.spo2_average = datas['spo2_average']
                if 'steps' in datas:
                    self.paso = datas['steps']
                if 'distance' in datas:
                    self.distancia = datas['distance']

                # almacenamiento de datos en BD
                # comprobamos si ya tenemos datos del mismo id en la base de datos
                sql = "SELECT * FROM entrenamiento WHERE id_entrenamiento = '{0}'".format(self.id_entrenamiento)
                cur.execute(sql)
                result = cur.fetchall()
                if not result:  # si no tenemos, guardamos directamente en la BD
                    # almacenar datos en la base de dato
                    # print("no tenemos dados en la BD, insertamos los datos")

                    # 1.averiguamos el nombre del usuario mediante el id modelo obtenido del json
                    sql = "SELECT * FROM dispositivo WHERE id_modelo = '{0}'".format(self.id_modelo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del usuario es None
                        print('no se ha encontrado dispositivo')
                    else:
                        for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                            self.nombre_usuario = nombre_usu

                    # 2.guardamos datos general
                    sql = "INSERT INTO entrenamiento(id_entrenamiento, date_entrenamiento, startdate, enddate, device_id, modelo_disp, nombre_usuario) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.id_entrenamiento, self.fecha, self.startdate, self.enddate, self.id_dispositivo, self.id_modelo, self.nombre_usuario)
                    cur.execute(sql, val)

                    # 3.insertamos datos de calorias
                    sql = "INSERT INTO calorias_entrenamiento(time_calorias, calorias, id_entrenamiento) VALUES ( %s, %s, %s)"
                    val = (datas_time, self.calorias, self.id_entrenamiento)
                    cur.execute(sql, val)


                    # 4.insertamos datos de distancias
                    sql = "INSERT INTO distancia_entrenamiento(time_distancia, distancia, id_entrenamiento) VALUES ( %s, %s, %s)"
                    val = (datas_time, self.distancia, self.id_entrenamiento)
                    cur.execute(sql, val)


                    # 5.insertamos datos de elevacion
                    sql = "INSERT INTO elevacion_entrenamiento(time_elevacion, elevacion, id_entrenamiento) VALUES ( %s, %s, %s)"
                    val = (datas_time, self.elevacion, self.id_entrenamiento)
                    cur.execute(sql, val)


                    # 6.insertamos datos de hr
                    sql = "INSERT INTO hr_entrenamiento(time_hr, hr_average, hr_min, hr_max, hr_zone_0, hr_zone_1, hr_zone_2, hr_zone_3, id_entrenamiento) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (datas_time, self.hr_average, self.hr_min, self.hr_max, self.hr_zone_0, self.hr_zone_1,
                           self.hr_zone_2, self.hr_zone_3, self.id_entrenamiento)
                    cur.execute(sql, val)

                    # 7.insertamos datos de pasos
                    sql = "INSERT INTO pasos_entrenamiento(time_pasos, pasos, id_entrenamiento) VALUES ( %s, %s, %s)"
                    val = (datas_time, self.paso, self.id_entrenamiento)
                    cur.execute(sql, val)


                    # 8.insertamos datos de spo2
                    sql = "INSERT INTO spo2_average_entrenamiento(time_spo2, spo2_average, id_entrenamiento) VALUES ( %s, %s, %s)"
                    val = (datas_time, self.spo2_average, self.id_entrenamiento)
                    cur.execute(sql, val)

                else:  # si ya tenemos datos con mismo id, no hacemos nada
                    print('ya tenemos datos con este id, no hacemos nada')





            print()
            print('          datos de Entrenamiento almacenados          ')
            print()
