from Medidas import *


class Actividad(Medidas):
    def __init__(self):
        super().__init__()
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr_zone_0 = 0
        self.hr_zone_1 = 0
        self.hr_zone_2 = 0
        self.hr_zone_3 = 0
        self.calorias = 0
        self.total_calorias = 0
        self.suave = 0
        self.moderada = 0
        self.intensa = 0
        self.activa = 0
        self.elevacion = 0
        self.paso = 0
        self.distancia = 0

    def reset_datos(self):
        super().reset_datos()
        self.hr_average = 0
        self.hr_min = 0
        self.hr_max = 0
        self.hr_zone_0 = 0
        self.hr_zone_1 = 0
        self.hr_zone_2 = 0
        self.hr_zone_3 = 0
        self.calorias = 0
        self.total_calorias = 0
        self.suave = 0
        self.moderada = 0
        self.intensa = 0
        self.activa = 0
        self.elevacion = 0
        self.paso = 0
        self.distancia = 0

    def get_datos(self, cur, url, headers, payload):
        print()
        print("------------------------peticion de actividad------------------------------------")
        print()
        response_activity = requests.request("POST", url, headers=headers, data=payload)

        activity_data = response_activity.json()
        activity_info = activity_data['body']['activities']
        # print (activity_info)

        if not activity_info:
            print("no se ha obtenido datos sobre actividad del usuario.")
        else:
            for series in activity_info:
                self.reset_datos() #resetear datos
                id_act = 0
                if 'elevation' in series:
                    self.elevacion = series['elevation']
                if 'soft' in series:
                    self.suave = series['soft']
                if 'moderate' in series:
                    self.moderada = series['moderate']
                if 'intense' in series:
                    self.intensa = series['intense']
                if 'active' in series:
                    self.activa = series['active']
                if 'calories' in series:
                    self.calorias = series['calories']
                if 'steps' in series:
                    self.paso = series['steps']
                if 'distance' in series:
                    self.distancia = series['distance']
                if 'totalcalories' in series:
                    self.total_calorias = series['totalcalories']
                if 'hr_average' in series:
                    self.hr_average = series['hr_average']
                if 'hr_min' in series:
                    self.hr_min = series['hr_min']
                if 'hr_max' in series:
                    self.hr_max = series['hr_max']
                if 'hr_zone_0' in series:
                    self.hr_zone_0 = series['hr_zone_0']
                if 'hr_zone_1' in series:
                    self.hr_zone_1 = series['hr_zone_1']
                if 'hr_zone_2' in series:
                    self.hr_zone_2 = series['hr_zone_2']
                if 'hr_zone_3' in series:
                    self.hr_zone_3 = series['hr_zone_3']
                if 'date' in series:
                    self.fecha = series['date']
                if 'deviceid' in series:
                    self.id_dispositivo = series['deviceid']
                if 'modified' in series:
                    modified = series['modified']
                else:
                    modified = 0

                # comprobamos si tenemos datos para almacenar
                if self.elevacion == 0 and self.suave == 0 and self.moderada == 0 and self.intensa == 0 and self.activa == 0 and self.calorias == 0 and self.paso == 0 and self.distancia == 0 and self.total_calorias == 0 and self.hr_average == 0 and self.hr_min == 0 and self.hr_max == 0 and self.hr_zone_0 == 0 and self.hr_zone_1 == 0 and self.hr_zone_2 == 0 and self.hr_zone_3 == 0:
                    print('no tenemos datos de actividad para almacenar')
                else:
                    # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                    sql = "SELECT * FROM actividad WHERE date_actividad = '{0}'".format(self.fecha)
                    cur.execute(sql)
                    result = cur.fetchall()

                    if not result:  # si no tenemos, guardamos directamente en la BD
                        # almacenar datos en la base de dato

                        # 1.averiguamos el nombre del usuario mediante deviceid obtenido del json
                        sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                        cur.execute(sql)
                        result = cur.fetchall()
                        if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del usuario es None
                            print('no se ha encontrado dispositivo')
                        else:
                            for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_usu in result:
                                self.nombre_usuario = nombre_usu

                        # 2.guardamos datos general
                        sql = "INSERT INTO actividad(date_actividad, device_id, nombre_usuario, modified) VALUES ( %s, %s, %s, %s)"
                        val = (self.fecha, self.id_dispositivo, self.nombre_usuario, modified)
                        cur.execute(sql, val)

                        # obtenemos el id del ultimo insertado
                        sql = "SELECT * FROM actividad ORDER BY id_actividad DESC LIMIT 1"
                        cur.execute(sql)
                        result = cur.fetchall()
                        if not result:
                            print('error en la obtencion del id_actividad')
                        else:
                            for id_a, dia, id_d, nombre_u, modificacion in result:
                                #print (id_a, dia, id_d, nombre_u, modificacion)
                                id_act = id_a

                        # 3.insertamos datos de elevacion
                        if self.elevacion != 0:
                            sql = "INSERT INTO elevacion_actividad(id_actividad, elevacion) VALUES ( %s, %s)"
                            val = (id_act, self.elevacion)
                            cur.execute(sql, val)

                        # 4.insertamos datos de distancia
                        if self.distancia != 0:
                            sql = "INSERT INTO distancia_actividad(id_actividad, distancia) VALUES ( %s, %s)"
                            val = (id_act, self.distancia)
                            cur.execute(sql, val)

                        # 5.insertamos datos de pasos
                        if self.paso != 0:
                            sql = "INSERT INTO paso_actividad(id_actividad, pasos) VALUES ( %s, %s)"
                            val = (id_act, self.paso)
                            cur.execute(sql, val)

                        # 6.insertamos datos de calorias
                        if self.calorias != 0 or self.total_calorias != 0:
                            sql = "INSERT INTO calorias_actividad(id_actividad, calorias, total_calorias) VALUES ( %s, %s, %s)"
                            val = (id_act, self.calorias, self.total_calorias)
                            cur.execute(sql, val)

                        # 7.insertamos datos de intensidad
                        if self.suave != 0 or self.moderada != 0 or self.intensa != 0 or self.activa != 0:
                            sql = "INSERT INTO intensidad_actividad(id_actividad, suave, moderada, intensa, activa) VALUES ( %s, %s, %s, %s, %s)"
                            val = (id_act, self.suave, self.moderada, self.intensa, self.activa)
                            cur.execute(sql, val)


                        # 8.insertamos datos de hr
                        if self.hr_average != 0 or self.hr_min != 0 or self.hr_max != 0 or self.hr_zone_0 != 0 or self.hr_zone_1 != 0 or self.hr_zone_2 != 0 or self.hr_zone_3 != 0:
                            sql = "INSERT INTO hr_actividad(id_actividad, hr_average, hr_min, hr_max, hr_zone_0, hr_zone_1, hr_zone_2, hr_zone_3) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (id_act, self.hr_average, self.hr_min, self.hr_max, self.hr_zone_0, self.hr_zone_1, self.hr_zone_2, self.hr_zone_3)
                            cur.execute(sql, val)

                    else:  # si ya tenemos, comprobamos la fecha de ultima actualizacion,
                        for id_a, fecha, id_disp, nombre_usu, tiempo_act in result:
                            tiempo_actualizacion = tiempo_act
                            id_act = id_a
                            if tiempo_actualizacion == modified:  # si es lo mismo que tenemos en la BD, no hacemos nada
                                # print('son los mismos datos, no vamos a hacer nada')
                                pass
                            else:  # si son diferente, actualizamos por los nuevos datos
                                #print('ya tenemos datos registrados, actualizamos los datos')
                                #print('...........')
                                # actualizamos datos de la actividad
                                sql = "Update actividad set device_id = %s, modified = %s where date_actividad = %s"
                                val = (self.id_dispositivo, modified, self.fecha)
                                cur.execute(sql, val)
                                # actualizamos datos de elevacion
                                if self.elevacion != 0:
                                    sql = "Update elevacion_actividad set elevacion = %s where id_actividad = %s"
                                    val = (self.elevacion, id_act)
                                    cur.execute(sql, val)
                                # actualizamos datos de distancia
                                if self.distancia != 0:
                                    sql = "Update distancia_actividad set distancia = %s where id_actividad = %s"
                                    val = (self.distancia, id_act)
                                    cur.execute(sql, val)
                                # actualizamos datos de pasos
                                if self.paso != 0:
                                    sql = "Update paso_actividad set pasos = %s where id_actividad = %s"
                                    val = (self.paso, id_act)
                                    cur.execute(sql, val)
                                # actualizamos datos de calorias
                                if self.calorias != 0 or self.total_calorias != 0:
                                    sql = "Update calorias_actividad set calorias = %s, total_calorias = %s where id_actividad = %s"
                                    val = (self.calorias, self.total_calorias, id_act)
                                    cur.execute(sql, val)
                                # actualizamos datos de intensidad
                                if self.suave != 0 or self.moderada != 0 or self.intensa != 0 or self.activa != 0:
                                    sql = "Update intensidad set suave = %s, moderada = %s, intensa = %s, activa = %s where id_actividad = %s"
                                    val = (self.suave, self.moderada, self.intensa, self.activa, id_act)
                                    cur.execute(sql, val)
                                # actualizamos datos de hr
                                if self.hr_average != 0 or self.hr_min != 0 or self.hr_max != 0 or self.hr_zone_0 != 0 or self.hr_zone_1 != 0 or self.hr_zone_2 != 0 or self.hr_zone_3 != 0:
                                    sql = "Update hr_actividad set hr_average = %s, hr_min = %s, hr_max = %s, hr_zone_0 = %s, hr_zone_1 = %s, hr_zone_2 = %s, hr_zone_3 = %s where id_actividad = %s"
                                    val = (self.hr_average, self.hr_min, self.hr_max, self.hr_zone_0, self.hr_zone_1,
                                           self.hr_zone_2, self.hr_zone_3, id_act)
                                    cur.execute(sql, val)





            print()
            print("          Datos de actividad almacenados          ")
            print()
