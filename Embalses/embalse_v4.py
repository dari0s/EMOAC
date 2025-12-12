import pandas as pd 
import numpy as np 
import os, sys, time 
import matplotlib as plt 
import openpyxl   

# Lectura de Archivos

ruta_carpeta = os.getcwd()

archivo_PLP = 'IPLP20250902'

plp = pd.read_excel(archivo_PLP + '.xlsm', sheet_name = 'Centrales', header = None, engine = 'openpyxl')
plp_barras = pd.read_excel(archivo_PLP + '.xlsm', sheet_name = 'Barras', header = None, engine = 'openpyxl')    

'''
data = pd.read_csv('Dam_Embalses.csv',sep = ',')
data_a = pd.read_csv('Dam_Vend_Objetivo.csv', sep = ',')
embalses = pd.read_excel('dicref_v2.xlsx',engine = 'openpyxl')
embalses_extra = pd.read_excel('embalses_extra.xlsx', engine = 'openpyxl') 
'''
# Series corespondientes a Volumen Final de Embalses 
'''
data_header = data.head()
data_vend = data['vend']
data_vend_a = data_a['vend']
'''
# Se busca posición del header CENTRALES

def encontrar(bd,header : str):
    filas = bd.shape[0]
    columnas = bd.shape[1]
    pivot_fila = 0
    pivot_columna = 0
    for i in range(filas):
        for j in range(columnas):
            if (bd.iloc[i][j] == header):
                pivot_fila = i
                pivot_columna = j
                break
    return (pivot_fila,pivot_columna)

contenido_coordenadas = plp.iloc[encontrar(plp,'INDICE')[0]][encontrar(plp,'INDICE')[1]]

plp = pd.read_excel(archivo_PLP + '.xlsm', sheet_name = 'Centrales', header = encontrar(plp,'INDICE')[0], engine = 'openpyxl')
plp_barras = pd.read_excel(archivo_PLP + '.xlsm', sheet_name = 'Barras', header = encontrar(plp_barras,'Nº')[0],engine='openpyxl')

plp.rename(columns={ 'Unnamed: 1': 'Nombre Central','Inicial':'Cota_Inicial',
                    'Final':'Cota_Final','Mínima':'Cota_Mínima',
                    'Máxima':'Cota_Máxima',"Inicial.1":"Vol_Inicial",
                    "Final.1":"Vol_Final",'Mínimo':'Vol_Mínimo',
                    'Máximo':'Vol_Máximo'}, inplace=True)

plp_barras.rename(columns= {'Nº': 'Numero'}, inplace=True)

print(plp_barras.head())


# Cota m.s.n.m {'Inicial', 'Final', 'Mínima', 'Máxima'}
# Volumen Embalse {'Inicial.1', 'Final.1', 'Mínimo', 'Máximo'}

plp = plp[['Nombre Central','Tipo de Central','Conectada a la Barra',
            'Cota_Inicial','Cota_Final','Cota_Mínima','Cota_Máxima',
            'Vol_Inicial','Vol_Final','Vol_Mínimo','Vol_Máximo']]

# Reemplazar Nombre Barras

# merge es con 'Numero' = 'ID Barra' desde el PLP

plp = plp.merge(plp_barras[['Numero', 'BARRA']], on='Numero', how='left')
plp['Conectada a la Barra'] = plp_barras['BARRA']

# Borrar columna temporal

plp = plp.drop(columns=['BARRA'])

# Centrales C/ Embalses

centrales_embalses = plp[(plp['Tipo de Central'] == "E")] 

print(centrales_embalses.columns)
print(centrales_embalses.head())
print(plp_barras.head())

## Salida : Guardar Archivo // 

ruta_archivo = os.path.join(ruta_carpeta, f'Embalses_Semanal.xlsx')

with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
    centrales_embalses.to_excel(writer, index=False, sheet_name='Embalses')



