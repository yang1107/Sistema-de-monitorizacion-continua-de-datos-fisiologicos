# -*- coding: utf-8 -*-

# realiza la tarea de obtener datos de los parametros de salud registrados por el dispositivo withings a traves de la API Withings
# y lo almacena en la tabla correspondiente de la base de datos.

import requests  # para realizar peticiones POST
import json  # para gestionar archivos json
import calendar
import time
import psycopg2
import datetime
from funciones import *
import sys
from Actividad import *
from Cuenta import *
from Dispositivo import *
from Ecg import *
from Entrenamiento import *
from MedidasAltaFrecuencia import *
from Objetivo import *
from Salud import *
from Suenio import *
from Usuario import *

# Comprobacion, ejecutar solo si se reciben 2 argumentos
if len(sys.argv) == 4:
    access_token = sys.argv[1]
    refresh_token = sys.argv[2]
    userid = sys.argv[3]
    print()
    print('access_token ', access_token)
    print('refresh_token ', refresh_token)
    print()

    if userid == '12035246':
        usuario = Usuario('aholgado', 'juan', 'jaholgado@ugr.es', 38, 175, 'H', 'altius')
    if userid == '12060035':
        usuario = Usuario('cris', 'patricia', 'patricia@correo.com', 25, 178, 'M', 'altius')
    if userid == '12157510':
        usuario = Usuario('Alex', 'Basso', 'Alex@correo.com', 25, 178, 'H', 'altius')

    actividad = Actividad()
    cuenta = Cuenta('altius')
    dispositivo = Dispositivo(usuario.nombre)
    ecg = Ecg()
    entrenamiento = Entrenamiento()
    medidasAlta = MedidasAltaFrecuencia()
    salud = Salud()
    suenio = Suenio()
    objetivo = Objetivo(usuario.nombre)

    access_token_time = time.time()  # almacenamos el tiempo en el que onbtenemos el access_token actual
    EXIPRE_TIME = 9000  # pasado este tiempo se expira el access_token actual
    need_refresh_token = False
    almacenar_usu = False

    current_time = time.time()
    enddate = int(current_time)
    startdate = enddate - 14400
    startdateymd = time.strftime('%Y-%m-%d', time.localtime(float(startdate)))
    enddateymd = time.strftime('%Y-%m-%d', time.localtime(float(startdate)))

    # ---------------------headers para todas las peticiones-------------------
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + access_token
    }

    # -------------------los urls y payloads ------------------------
    url_token = "https://wbsapi.withings.net/v2/oauth2"
    payload_token = 'action=requesttoken&client_id=97e338c19161c11184c57302dbdd3557f63cea80f37c6fd743c060159c3cfc21&client_secret=6df7fe92bfd8cdc4c240bb278494a02af1e1586bcff558167163457535af2bfc&grant_type=refresh_token&refresh_token=0'
    headers_token = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    url_goals = "https://wbsapi.withings.net/v2/user"
    payload_goals = 'action=getgoals'

    url_device = "https://wbsapi.withings.net/v2/user"
    payload_device = 'action=getdevice'

    url_activity = "https://wbsapi.withings.net/v2/measure"
    payload_activity_ini = 'action=getactivity&data_fields=elevation%2Chr_average%2Chr_min%2Chr_max%2Chr_zone_0%2Csoft%2Cmoderate%2Cintense%2Cactive%2Ctotalcalories%2Ccalories%2Chr_zone_1%2Chr_zone_2%2Chr_zone_3%2Csteps%2Cdistance&startdateymd=0&enddateymd=0'
    payload_activity = changepayload_date(payload_activity_ini, startdateymd, enddateymd)

    url_health = "https://wbsapi.withings.net/measure"
    payload_health_ini = 'action=getmeas&meastype=54%2C123%2C1%2C76%2C88%2C8%2C5%2C6%2C91%2C11&category=1&startdate=0&enddate=0'
    payload_health = changepayload_time(payload_health_ini, startdate, enddate)

    url_workouts = "https://wbsapi.withings.net/v2/measure"
    payload_workouts_ini = 'action=getworkouts&data_fields=calories%2Cintensity%2Chr_average%2Chr_min%2Chr_max%2C%20hr_zone_0%2C%20hr_zone_1%2C%20hr_zone_2%2C%20hr_zone_3%2C%20pause_duration%2C%20spo2_average%2C%20steps%2C%20distance%2C%20elevation&startdateymd=0&enddateymd=0'
    payload_workouts = changepayload_date(payload_workouts_ini, startdateymd, enddateymd)

    url_sleep = "https://wbsapi.withings.net/v2/sleep"
    payload_sleep_sum_ini = 'action=getsummary&startdateymd=2021-11-24&enddateymd=2021-11-25&data_fields=nb_rem_episodes%2Csleep_efficiency%2Csleep_latency%2Ctotal_sleep_time%2C%20total_timeinbed%2C%20wakeup_latency%2Cwaso%2Capnea_hypopnea_index%2C%20breathing_disturbances_intensity%2Casleepduration%2C%20deepsleepduration%2C%20durationtosleep%2Cdurationtowakeup%2Chr_average%2Chr_max%2Chr_min%2Clightsleepduration%2Cnight_events%2Cout_of_bed_count%2Cremsleepduration%2Crr_average%2Crr_max%2Crr_min%2Csleep_score%2Csnoring%2Csnoringepisodecount%2Cwakeupcount%2Cwakeupduration'
    payload_sleep_ini = 'action=get&startdate=1637712004&enddate=1637798404&data_fields=hr%2Crr%2Csnoring%2Csdnn_1%2Crmssd'
    payload_sleep_sum = changepayload_date(payload_sleep_sum_ini, startdateymd, enddateymd)
    payload_sleep = changepayload_time(payload_sleep_ini, startdate, enddate)

    url_ecg = "https://wbsapi.withings.net/v2/heart"
    payload_ecg_ini = 'action=list&startdate=0&enddate=0'
    payload_ecg = changepayload_time(payload_ecg_ini, startdate, enddate)

    url_high = "https://wbsapi.withings.net/v2/measure"
    payload_high_ini = 'action=getintradayactivity&startdate=0&enddate=0&data_fields=steps%2Celevation%2Ccalories%2Cdistance%2Cheart_rate%2Cspo2_auto'
    payload_high = changepayload_time(payload_high_ini, startdate, enddate)


    # -----------------------recopilacion de datos de forma continua --------------------
    while True:
        #conexion a BD
        conexion = psycopg2.connect(
            database="withingsdatas",
            user="withinguser",
            host="localhost",
            password="cB1M4gB",
            port="5432"
        )

        # creamos el cursor con el objeto conexion
        cur = conexion.cursor()

        #------------------------almacenar datos de la cuenta y de usuario en la BD al iniciar el programa -----------------------
        if almacenar_usu:
            cuenta.almacenar_datos(cur)
            usuario.almacenar_datos(cur)
            # -------------------obtencion de objetivos ------------------
            objetivo.get_objetivo(cur, url_goals, headers, payload_goals, objetivo.nombre_usuario)
            almacenar_usu = False

        # ---------------------------------------comprobar si ha expirado el token---------------------------------
        tiempoa = time.time() - access_token_time
        print()
        print("Ha pasado ", tiempoa, "segundos desde que obtenemos el token de acceso" )
        print("Cuando llega a ", EXIPRE_TIME, "segundos, tenemos que renovarlo")
        print()
        if (time.time() - access_token_time) >= EXIPRE_TIME:
            need_refresh_token = True

        # --------------------------------------------------------si hay que actualizar el token -------------------
        if need_refresh_token:
            print("Ha caducado el access token, vamos a renovarlo")

            print()
            print("------------------------Actualizacion del token------------------------------------")
            print()

            # actualizamos refresh token del payload
            aux = {}
            payload_aux = payload_token.split('&')

            for item in payload_aux:
                key, value = item.split('=')
                if key == 'refresh_token':
                    value = refresh_token
                aux[key] = value

            payload_token = '&'.join([key + '=' + value for key, value in aux.items()])

            # print(payload_token)

            response_token = requests.request("POST", url_token, headers=headers_token, data=payload_token)

            datos_token = response_token.json()
            access_token = datos_token['body']['access_token']
            refresh_token = datos_token['body']['refresh_token']

            print()
            print("          Tokens actualizados          ")
            print()
            print("El nuevo token de acceso es ", access_token)
            print("El nuevo refresh token es ", refresh_token)

            access_token_time = time.time()
            need_refresh_token = False

            # Actualizar el token de acceso que enviamos en el headers
            new_token = 'Bearer ' + access_token
            headers['Authorization'] = new_token
        else:
            print("Todavia es valido el token, no hay que renovarlo")

        print()
        print("Empezamos la nuevaq peticion de datos")

        # -----------------obtencion de dispositivos --------------------
        dispositivo.get_dispositivos(cur, url_device, headers, payload_device)

        # -----------obtencion de datos de actividad --------------------
        actividad.get_datos(cur, url_activity, headers, payload_activity)

        # -----------ontencion de datos de salud ---------------------------
        salud.get_datos(cur, url_health, headers, payload_health)

        # -----------ontencion de datos de entrenamiento ---------------------------
        entrenamiento.get_datos(cur, url_workouts, headers, payload_workouts)

        # -----------ontencion de datos de suenio ---------------------------
        suenio.get_datos_suenio(cur, url_sleep, headers, payload_sleep_sum, payload_sleep)

        # -----------ontencion de datos de ecg ---------------------------
        ecg.get_datos(cur, url_ecg, url_health, headers, payload_ecg)

        # -----------ontencion de datos de slta frecuencia ---------------------------
        medidasAlta.get_datos(cur, url_high, headers, payload_high)

        # cerramos la conexion a la base de datos
        conexion.commit()
        # print("cambios de datos guardados en base de datos")
        conexion.close()

        # Actualizamos el tiempo de inicio y el tiempo fin del payload
        new_startdate = enddate
        # print("el valor del new_startdate es ", new_startdate)
        new_enddate = int(new_startdate) + 14400 # 4 horas
        # print("el valor del new_enddate es ", new_enddate)
        enddate = new_enddate
        # print("el valor del enddate es ", enddate)

        new_startdateymd = time.strftime('%Y-%m-%d', time.localtime(float(new_startdate)))
        # print("el valor del new_startdateymd es ", new_startdateymd)
        new_enddateymd = new_startdateymd

        nuevo_startdate_formateado = datetime.datetime.fromtimestamp(new_startdate)
        print()
        print("El tiempo de inicio para el siguiente peticion es ", new_startdate)
        print(nuevo_startdate_formateado)
        print()

        payload_activity = changepayload_date(payload_activity, new_startdateymd, new_enddateymd)
        payload_health = changepayload_time(payload_health, new_startdate, new_enddate)
        payload_workouts = changepayload_date(payload_workouts, new_startdateymd, new_enddateymd)
        payload_sleep_sum = changepayload_date(payload_sleep_sum, new_startdateymd, new_enddateymd)
        payload_sleep = changepayload_time(payload_sleep, new_startdate, new_enddate)
        payload_ecg = changepayload_time(payload_ecg, new_startdate, new_enddate)
        payload_high = changepayload_time(payload_high, new_startdate, new_enddate)

        time.sleep(14400)
else:
    print("Error - Introduce el access token, el refresh token y el userid")
    print('Ejemplo: nombre_programa access_token refresh_token userid')
