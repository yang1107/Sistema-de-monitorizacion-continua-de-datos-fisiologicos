class Usuario:
    def __init__(self, apellido_u, nombre_u, correos, edad, altura, sexo, nombre_c):
        self.apellido = apellido_u
        self.nombre = nombre_u
        self.email = correos
        self.edad = edad
        self.altura = altura
        self.sexo = sexo
        self.nombre_cuenta = nombre_c


    def almacenar_datos(self, cur):
        # comprobamos si tenemos ya el usuario en la base de datos
        sql = "SELECT * FROM usuario where nombre = '{0}'".format(self.nombre)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            sql = "INSERT INTO usuario(apellido,nombre, email, edad, altura, sexo, nombre_cuenta) " \
                  "VALUES ( %s, %s, %s, %s, %s, %s, %s) "
            val = (self.apellido, self.nombre, self.email, self.edad, self.altura, self.sexo, self.nombre_cuenta)
            cur.execute(sql, val)
