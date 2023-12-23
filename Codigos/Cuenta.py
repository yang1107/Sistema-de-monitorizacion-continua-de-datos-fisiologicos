class Cuenta:
    def __init__(self, nombre):
        self.nombre_cuenta = nombre

    def reset_datos(self):
        self.nombre_cuenta = 'None'

    def almacenar_datos(self, cur):
        # comprobamos si tenemos ya el usuario en la base de datos
        sql = "SELECT * FROM cuenta where nombre_cuenta = '{0}'".format(self.nombre_cuenta)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            sql = "INSERT INTO cuenta(nombre_cuenta) VALUES ('{0}')".format(self.nombre_cuenta)
            cur.execute(sql)
