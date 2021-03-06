#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

def connecta_banco():
    return sqlite3.connect('./database/webservice.db')

def create_database():
    conn = sqlite3.connect('./database/webservice.db')

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE Forecast 
                        (id INTEGER primary key, nome_cidade TEXT,nome_estado TEXT,
                        nome_pais TEXT, data TEXT,chuva_prec REAL, chuva_prob REAL,
                        temperature_max REAL, temperature_min REAL)''')
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
        con.cursor().executemany('INSERT INTO Forecast VALUES (NULL,?,?,?,?,?,?,?,?)', l)
        con.commit()
        
    return 1

def analise(data_inicial, data_final):

    with connecta_banco() as con:
        #con.text_factory=bytes
        sql = '''
                SELECT F.nome_cidade, F.temperature_max,
	                (SELECT AVG(chuva_prec) FROM FORECAST WHERE F.nome_cidade = nome_cidade)
                FROM FORECAST F
                WHERE F.temperature_max = (SELECT MAX(temperature_max) FROM FORECAST)
                    AND F.data >= ? AND F.data <= ?
                GROUP BY F.nome_cidade, F.temperature_max;
                '''
        return formata_retorno(con.cursor()
                                    .execute(sql, (data_inicial, data_final))
                                    .fetchall()
                              )
    
#    return 


def formata_retorno(retorno):
    l = []
    for linha in retorno:
        l.append({'cidade':linha[0], 'temperatura_max':linha[1],'precipitacao_avg':linha[2]})
    return l

