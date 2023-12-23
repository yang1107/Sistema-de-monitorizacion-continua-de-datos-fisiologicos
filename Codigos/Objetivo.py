import requests


class Objetivo:
    def __init__(self, nombre_u):
        self.nombre_usuario = nombre_u
        self.paso = 0
        self.suenio = 0
        self.peso = 0

    def reset_datos(self, nombre_u):
        self.nombre_usuario = nombre_u
        self.paso = 0
        self.suenio = 0
        self.peso = 0

    def get_objetivo(self, cur, url, headers, payload, nombre_u):
        response_goals = requests.request("POST", url, headers=headers, data=payload)

        goals_data = response_goals.json()
        goals_info = goals_data['body']['goals']

        # print (goals_info)

        if not goals_info:
            print("no se ha obtenido datos sobre objetivos del usuario.")
        else:
            count = 0
            for series in goals_info:
                self.reset_datos(self.nombre_usuario) #resetear datos
                if series == 'steps':
                    self.paso = goals_info['steps']
                if series == 'sleep':
                    self.suenio = goals_info['sleep']
                if series == 'weight':
                    self.peso = goals_info['weight']['value'] / 1000

                count += 1
                # print (count)
                if count % 3 == 0 or count == len(goals_info):
                    # print('steps = ', self.paso)
                    # print('sleep = ', self.suenio)
                    # print('weigt = ', self.paso)

                    sql = "SELECT * FROM objetivo where nombre_usuario = '{0}'".format(nombre_u)
                    cur.execute(sql)
                    result = cur.fetchall()
                    if not result:
                        # guardamos los datos obtenidos en la base de datos
                        # almacenar datos en la base de dato
                        sql = "INSERT INTO objetivo(paso, suenio, peso, nombre_usuario) VALUES ( %s, %s, %s, %s)"
                        val = (self.paso, self.suenio, self.peso, self.nombre_usuario)
                        cur.execute(sql, val)
                        # print("datos de objetivo almacenados")
                        cur.execute("SELECT * FROM objetivo")
                        for id_o, pasos, suenio, peso, nombre_usu in cur.fetchall():
                            print(id_o, pasos, suenio, peso, nombre_usu)
                    else:
                        # actualizamos
                        if self.paso != 0:
                            sql = "Update objetivo set paso = %s where nombre_usuario = %s"
                            val = (self.paso, nombre_u)
                            cur.execute(sql, val)
                        if self.suenio != 0:
                            sql = "Update objetivo set suenio = %s where nombre_usuario = %s"
                            val = (self.suenio, nombre_u)
                            cur.execute(sql, val)
                        if self.peso != 0:
                            sql = "Update objetivo set peso = %s where nombre_usuario = %s"
                            val = (self.peso, nombre_u)
                            cur.execute(sql, val)
