from Medidas import *


class Salud(Medidas):
    def __init__(self):
        super().__init__()
        self.vo2max = 0
        self.fat_mass = 0
        self.fat_free_mass = 0
        self.fat_ratio = 0
        self.bone_mass = 0
        self.muscle_mass = 0
        self.pulse_wave_velocity = 0
        self.weight = 0
        self.hydration = 0
        self.heart_pulse = 0

    def reset_datos(self):
        super().reset_datos()
        self.vo2max = 0
        self.fat_mass = 0
        self.fat_free_mass = 0
        self.fat_ratio = 0
        self.bone_mass = 0
        self.muscle_mass = 0
        self.pulse_wave_velocity = 0
        self.weight = 0
        self.hydration = 0
        self.heart_pulse = 0

    #  IMC = peso (kg)/ [estatura (m)]2
    def calcularIMC(self, peso, estatura):
        altura = float(estatura) / 100.0
        imc = float(peso) / altura**2

        return imc


    def obtenerIMC(self, cur, peso, nombre_u):
        imc = 0
        altura = 0

        sql = "SELECT * FROM usuario where nombre = '{0}'".format(nombre_u)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            print('no existe el usuario', nombre_u)
        else:
            for id_u, ape, nomb, email, edad, alt, sexo, nombre_c in result:
                # print (id_u, ape, nomb, email, edad, alt, sexo, nombre_c)
                altura = alt

        if altura != 0 and peso != 0:
            imc = self.calcularIMC(peso, altura)

        return imc

    def calcularTMB(self, weight, height, sex, age):
        tmb_general = (10 * float(weight)) + (6.25 * float(height)) - (5 * float(age))

        if sex == 'H':
            tmb = tmb_general + 5
        else:
            tmb = tmb_general - 161

        return tmb

    def obtenerTMB(self, cur, peso, nombre_u):
        tmb = 0

        sql = "SELECT * FROM usuario where nombre = '{0}'".format(nombre_u)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            print('no existe el usuario', nombre_u)
        else:
            for id_u, ape, nomb, email, edad, alt, sexo, nombre_c in result:
                # print (id_u, ape, nomb, email, edad, alt, sexo, nombre_c)
                altura = alt
                sex = sexo
                age = edad

        if altura != 0 and peso != 0 and age != 0 and sex != 'None':
            tmb = self.calcularTMB(peso, altura, sex, age)

        return tmb



    def obtenerProteina(self, cur, muscle_mass, nombre_u):
        pproteina = 0
        # obtener el id del ultimo registro de la salud que pertenece al usuario
        sql = "SELECT * FROM salud where nombre_usuario = '{0}' ORDER BY id_salud DESC LIMIT 1".format(nombre_u)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            print('no hay datos de este usuario')
        else:
            for id_s, fecha, id_d, nombre_u, creacion in result:
                #print (id_s, fecha, id_d, nombre_u, creacion)
                id_salud = id_s

            sql = "SELECT * FROM weight where id_salud = '{0}'".format(id_salud)
            cur.execute(sql)
            result = cur.fetchall()
            if not result:
                print('no hay datos de peso')
            else:
                for id_w, p, tiempo in result:
                    peso = p

            porcentaje_muscular = muscle_mass / peso * 100
            pproteina = porcentaje_muscular * 0.27

        return pproteina


    def obtenerAgua(self, cur, muscle_mass, nombre_u):
        pagua = 0
        # obtener el id del ultimo registro de la salud que pertenece al usuario
        sql = "SELECT * FROM salud where nombre_usuario = '{0}' ORDER BY id_salud DESC LIMIT 1".format(nombre_u)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            print('no hay datos de este usuario')
        else:
            for id_s, fecha, id_d, nombre_u, creacion in result:
                #print (id_s, fecha, id_d, nombre_u, creacion)
                id_salud = id_s

            sql = "SELECT * FROM weight where id_salud = '{0}'".format(id_salud)
            cur.execute(sql)
            result = cur.fetchall()
            if not result:
                print('no hay datos de peso')
            else:
                for id_w, p, tiempo in result:
                    peso = p

            porcentaje_muscular = muscle_mass / peso * 100
            pagua = porcentaje_muscular * 0.73

        return pagua


    def get_datos(self, cur, url, headers, payload):
        print()
        print("------------------------peticion de datos de salud general------------------------------------")
        print()
        response_health = requests.request("POST", url, headers=headers, data=payload)

        health_data = response_health.json()
        health_info = health_data['body']['measuregrps']

        if not health_info:
            print("no se ha obtenido datos sobre la salud del usuario.")
        else:
            for series in health_info:
                self.reset_datos() #resetear datos
                id_sa = 0
                imc = 0
                tmb = 0
                proteina = 0
                agua = 0
                if 'date' in series:
                    epoch_time = series['date']
                    self.fecha = datetime.datetime.fromtimestamp(epoch_time).date()
                if 'created' in series:
                    tiempo_creacion = series['created']
                if 'deviceid' in series:
                    self.id_dispositivo = series['deviceid']

                for series_data in series['measures']:
                    if series_data['type'] == 54:
                        spo2 = series_data['value']
                    elif series_data['type'] == 123:
                        self.vo2max = series_data['value']
                    elif series_data['type'] == 1:
                        self.weight = series_data['value'] / 1000
                    elif series_data['type'] == 76:
                        self.muscle_mass = series_data['value'] / 100
                    elif series_data['type'] == 88:
                        self.bone_mass = series_data['value'] / 100
                    elif series_data['type'] == 8:
                        self.fat_mass = series_data['value'] / 100
                    elif series_data['type'] == 5:
                        self.fat_free_mass = series_data['value'] / 1000
                    elif series_data['type'] == 6:
                        self.fat_ratio = series_data['value'] / 1000
                    elif series_data['type'] == 91:
                        self.pulse_wave_velocity = series_data['value'] / 1000
                    elif series_data['type'] == 77:
                        self.hydration = series_data['value'] / 1000
                    elif series_data['type'] == 11:
                        self.heart_pulse = series_data['value']


                # almacenamiento de datos en la BD

                # comprobamos si ya tenemos datos de la misma fecha en la base de datos
                sql = "SELECT * FROM salud WHERE date_salud = '{0}'".format(self.fecha)
                cur.execute(sql)
                result = cur.fetchall()
                if not result:  # si no tenemos, guardamos directamente en la BD
                    # almacenar datos en la base de dato
                    # print("no tenemos dados en la BD, insertamos los datos")

                    # 1.averiguamos el nombre del usuario mediante deviceid obtenido del json
                    sql = "SELECT * FROM dispositivo WHERE device_id = '{0}'".format(self.id_dispositivo)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result is None:  # si no se ha encontrado el id del dispositivo en la base de datos, el nombre del dispositivo es None
                        print('no se ha encontrado dispositivo')
                    else:
                        for id_d, nombre_disp, tipo, id_modelo, device_id, nombre_u in result:
                            self.nombre_usuario = nombre_u

                    # 2.guardamos datos de la salud
                    sql = "INSERT INTO salud(date_salud, device_id, nombre_usuario, time_created) VALUES ( %s, %s, %s, %s)"
                    val = (self.fecha, self.id_dispositivo, self.nombre_usuario, tiempo_creacion)
                    cur.execute(sql, val)

                    # obtenemos el id del ultimo insertado
                    sql = "SELECT * FROM salud ORDER BY id_salud DESC LIMIT 1"
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:
                        print('error en la obtencion del id_salud')
                    else:
                        for id_s, dia, id_d, nombre_u, creacion in result:
                            #print (id_s, dia, id_d, nombre_u, creacion)
                            id_sa = id_s

                    # 3.guardamos datos de vo2max
                    if self.vo2max != 0:
                        sql = "INSERT INTO vo2max(vo2max, id_salud) VALUES ( %s, %s)"
                        val = (self.vo2max, id_sa)
                        cur.execute(sql, val)

                    # 4.guardamos datos de weight
                    if self.weight != 0:
                        sql = "INSERT INTO weight(weight, id_salud) VALUES ( %s, %s)"
                        val = (self.weight, id_sa)
                        cur.execute(sql, val)

                        #tenemos datos de peso, calculamos IMC y TMB
                        imc = self.obtenerIMC(cur, self.weight, self.nombre_usuario)
                        tmb = self.obtenerTMB(cur, self.weight, self.nombre_usuario)

                        # guardamos datos en la BD
                        if imc != 0:
                            sql = "INSERT INTO imc(imc, id_salud) VALUES ( %s, %s)"
                            val = (imc, id_sa)
                            cur.execute(sql, val)

                        if tmb != 0:
                            sql = "INSERT INTO tmb(tmb, id_salud) VALUES ( %s, %s)"
                            val = (tmb, id_sa)
                            cur.execute(sql, val)

                    # 5.guardamos datos de muscle_mass
                    if self.muscle_mass != 0:
                        sql = "INSERT INTO muscle_mass(muscle_mass, id_salud) VALUES ( %s, %s)"
                        val = (self.muscle_mass, id_sa)
                        cur.execute(sql, val)

                        # tenemos datos de muscle_mass, calculamos porcentaje de agua y proteinas
                        agua = self.obtenerAgua(cur, self.muscle_mass, self.nombre_usuario)
                        proteina = self.obtenerProteina(cur, self.muscle_mass, self.nombre_usuario)

                        if agua != 0:
                            sql = "INSERT INTO agua(agua, id_salud) VALUES ( %s, %s)"
                            val = (agua, id_sa)
                            cur.execute(sql, val)

                        if proteina != 0:
                            sql = "INSERT INTO proteina(proteina, id_salud) VALUES ( %s, %s)"
                            val = (proteina, id_sa)
                            cur.execute(sql, val)

                    # 6.guardamos datos de bone_mass
                    if self.bone_mass != 0:
                        sql = "INSERT INTO bone_mass(bone_mass, id_salud) VALUES ( %s, %s)"
                        val = (self.bone_mass, id_sa)
                        cur.execute(sql, val)


                    # 7.guardamos datos de fat_mass
                    if self.fat_mass != 0:
                        sql = "INSERT INTO fat_mass(fat_mass, id_salud) VALUES ( %s, %s)"
                        val = (self.fat_mass, id_sa)
                        cur.execute(sql, val)

                    # 8.guardamos datos de fat_free_mass
                    if self.fat_free_mass != 0:
                        sql = "INSERT INTO fat_free_mass(fat_free_mass, id_salud) VALUES ( %s, %s)"
                        val = (self.fat_free_mass, id_sa)
                        cur.execute(sql, val)

                    # 9.guardamos datos de fat_ratio
                    if self.fat_ratio != 0:
                        sql = "INSERT INTO fat_ratio(fat_ratio, id_salud) VALUES ( %s, %s)"
                        val = (self.fat_ratio, id_sa)
                        cur.execute(sql, val)

                    # 10.guardamos datos de pulse_wave_velocity
                    if self.pulse_wave_velocity != 0:
                        sql = "INSERT INTO pulse_wave_velocity(pulse_wave_velocity, id_salud) VALUES ( %s, %s)"
                        val = (self.pulse_wave_velocity, id_sa)
                        cur.execute(sql, val)

                    # 11.guardamos datos de hydration
                    if self.hydration != 0:
                        sql = "INSERT INTO hydration(hydration, id_salud) VALUES ( %s, %s)"
                        val = (self.hydration, id_sa)
                        cur.execute(sql, val)

                    # 12.guardamos datos de heart_pulse
                    if self.heart_pulse != 0:
                        sql = "INSERT INTO heart_pulse(heart_pulse, id_salud) VALUES ( %s,%s)"
                        val = (self.heart_pulse, id_sa)
                        cur.execute(sql, val)

                    print('--------------------------------------------------------------')
                    print('datos SALUD almacenados')
                else:  # tenemos datos del mismo dia, ahora comprobamos si tienen el mismo tiempo de creacion
                    # print('ya tenemos datos de este dia registrados, no hacemos nada')
                    # print('...........')
                    pass

            print()
            print("          Datos de salud general almacenados          ")
            print()
