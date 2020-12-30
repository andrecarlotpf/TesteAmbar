#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

def connecta_banco():
    return sqlite3.connect('/home/local/CONDUCTOR/andre.filho/Dev/Python/Envs/AmbarTech/appV2/TesteAmbar/app/database/webservice.db')

def create_database():
    conn = sqlite3.connect('./database/webservice.db')

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE Forecast (
                        id INTEGER primary key, 
                        nome_cidade TEXT NOT NULL,
                        nome_estado TEXT NOT NULL,
                        nome_pais TEXT NOT NULL, 
                        data TEXT NOT NULL,
                        chuva_prec REAL NOT NULL, 
                        chuva_prob REAL NOT NULL,
                        temperature_max REAL NOT NULL, 
                        temperature_min REAL NOT NULL,
                        UNIQUE(nome_cidade, data))''')
    conn.close()
    return 1

def insert_into_db(forecast_json):
    
    cidade = forecast_json['name']
    estado = forecast_json['state']
    pais = forecast_json['country']
    
    l = []
    for data_object in forecast_json['data']:
        data = data_object['date']
        rain_prec = data_object['rain']['precipitation']
        rain_prob = data_object['rain']['probability']
        temp_max = data_object['temperature']['max']
        temp_min = data_object['temperature']['min']
        l.append(tuple((cidade, estado, pais, data, rain_prec,
                        rain_prob, temp_max, temp_min)))
    
    with connecta_banco() as con:
        for tupla in l:
            con.cursor().execute('INSERT OR REPLACE INTO Forecast VALUES (NULL,?,?,?,?,?,?,?,?)', tupla)
            con.commit()
    return 1

def analise_temperatura(data_inicial, data_final):
    lista_cidades = []
    with connecta_banco() as con:
        sql = '''
                SELECT F.nome_cidade, F.temperature_max,
	                (SELECT AVG(chuva_prec) FROM FORECAST WHERE F.nome_cidade = nome_cidade)
                FROM FORECAST F
                WHERE F.temperature_max = (SELECT MAX(temperature_max) FROM FORECAST)
                    AND F.data >= ? AND F.data <= ?
                GROUP BY F.nome_cidade, F.temperature_max;
                '''
        retorno = con.cursor().execute(sql, (data_inicial, data_final)).fetchall()
        for item in retorno:
            lista_cidades.append({'cidade':item[0], 'temperatura_max':item[1],'precipitacao_avg':item[2]})
    return lista_cidades


def analise_media_precipitacao(data_inicial, data_final):
    lista_cidades = []
    with connecta_banco() as con:
        sql = '''
                SELECT F.nome_cidade, AVG(F.chuva_prec)
                FROM FORECAST F
                WHERE F.data >= ? AND F.data <= ?
                GROUP BY F.nome_cidade;
                '''
        retorno = con.cursor().execute(sql, (data_inicial, data_final)).fetchall()
        for item in retorno:
            lista_cidades.append({'cidade':item[0], 'precipitacao_avg':item[1]})
    return lista_cidades




