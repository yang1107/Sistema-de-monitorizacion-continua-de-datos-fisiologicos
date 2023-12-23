# -*- coding: utf-8 -*-


def changepayload_time(payload,startdate,enddate):
    prop = {}
    new_payload = payload.split('&')
    #Actualizamos el valor del startdate y enddate
    for item in new_payload:
        key, value = item.split('=')
        if key == 'startdate':
            value = startdate
        if key == 'enddate':
            value = enddate
        prop[key] = value

    #unimos los contenidos del prop con = y luego con & para formar el nuevo payload
    return '&'.join([key + '=' + str(value) for key, value in prop.items()])

def changepayload_date(payload,startdateymd,enddateymd):
    aux_sleep = {}
    payload_sleep_aux = payload.split('&')

    for item in payload_sleep_aux:
        key, value = item.split('=')
        if key == 'startdateymd':
            value = startdateymd
        if key == 'enddateymd':
            value = enddateymd
        aux_sleep[key] = value

    return'&'.join([key + '=' + value for key, value in aux_sleep.items()])
