import pandas as pd


def write_dict(data_frame, *args):
    dic = {}
    for row in data_frame.itertuples():
        dic[row[1]] = {}
        i = 2
        for arg in args:
            dic[row[1]][arg] = row[i]
            i += 1
    return dic


dfs = pd.read_excel('datos.xlsx', sheet_name=None)
# Keys:
tamaño_bodega = 'Tamaño de bodega'
info_herramientas = 'Información sobre herramientas'
info_insumos = 'Información sobre insumos'
info_trabajadores = 'Información sobre trabajadores'
cant_insumos_bodega = 'Cant. de insumos en bodega'
cant_herramientas_bodega = 'Cant. herramientas en bodega'
herramientas_para_proyecto = 'Herramientas para proyectos'
herramientas_para_proyecto_ma = 'Herramientas para proyectos MA'
insumos_para_proyecto = 'Insumos para cada proyecto'
insumos_para_proyecto_ma = 'Insumos para cada proyecto MA'
trabajadores_para_proyecto = 'Trabajadores para cada proyecto'
ganancias_por_proyecto = 'Ganancias por proyecto'
ganancias_por_proyecto_ma = 'Ganancias por proyecto MA'
tiempos_por_proyecto = 'Tiempos por proyecto'

# Variables que contendran la info
volumen_bodega = 0
herramientas = {}
insumos = {}

###### Volumen bodega
test_tamaño_bodega = dfs[tamaño_bodega]

for row in test_tamaño_bodega.itertuples():
    volumen_bodega = row[1]


###### Herramientas
test_herramientas = dfs[info_herramientas]

for row in test_herramientas.itertuples():
    herramientas[row[1]] = {}
    herramientas[row[1]]['costos'] = row[2]
    herramientas[row[1]]['volumen'] = row[3]

###### Insumos
test_insumos = dfs[info_insumos]

for row in test_insumos.itertuples():
    herramientas[row[1]] = {}
    herramientas[row[1]]['costos'] = row[2]
    herramientas[row[1]]['volumen'] = row[3]


###### Trabajadores
test_trabajadores = dfs[info_trabajadores]
trabajadores = write_dict(test_trabajadores, 'cantidad')


###### Cantidad de insumos en bodega
test_stock_insumos = dfs[cant_insumos_bodega]
stock_insumos = write_dict(test_stock_insumos, 'cantidad')

###### Cantidad de herramientas en bodega
test_stock_herramientas = dfs[cant_herramientas_bodega]
stock_herramientas = write_dict(test_stock_herramientas, 'cantidad')

###### Herramientas, insumos, trabajadores, ganancias y tiempo para ambos tipos de proyectos
proyectos = {i: {'herramientas': {}, 'insumos': {}, 'trabajadores': {}} for i in range(1, 25)}

test_herramientas_proyectos = dfs[herramientas_para_proyecto]
for i, row in enumerate(test_herramientas_proyectos.itertuples()):
    if i >= 3:
        for j in range(1, 13):
            proyectos[j]['herramientas'][i-2] = row[j + 1]

test_herramientas_proyectos_ma = dfs[herramientas_para_proyecto_ma]
for i, row in enumerate(test_herramientas_proyectos_ma.itertuples()):
    if i >= 3:
        for j in range(13, 25):
            proyectos[j]['herramientas'][i-2] = row[j - 11]

test_insumos_proyectos = dfs[insumos_para_proyecto]
for i, row in enumerate(test_insumos_proyectos.itertuples()):
    if i >= 3:
        for j in range(1, 13):
            proyectos[j]['insumos'][i-2] = row[j + 1]

test_insumos_proyectos_ma = dfs[insumos_para_proyecto_ma]
for i, row in enumerate(test_insumos_proyectos_ma.itertuples()):
    if i >= 3:
        for j in range(13, 25):
            proyectos[j]['insumos'][i-2] = row[j - 11]

test_trabajadores_proyectos = dfs[trabajadores_para_proyecto]
for i, row in enumerate(test_trabajadores_proyectos.itertuples()):
    if i >= 2:
        for j in range(1, 13):
            proyectos[j]['trabajadores'][i-2] = row[j + 1]
            proyectos[j + 12]['trabajadores'][i-2] = row[j + 1]
        
test_ganancias = dfs[ganancias_por_proyecto]
for i, row in enumerate(test_ganancias.itertuples()):
    if i == 1:
        for j in range(1, 13):
            proyectos[j]['ganancias'] = row[j + 1]

test_ganancias_ma = dfs[ganancias_por_proyecto_ma]
for i, row in enumerate(test_ganancias_ma.itertuples()):
    if i == 1:
        for j in range(13, 25):
            proyectos[j]['ganancias'] = row[j - 11]

test_tiempo_proyectos = dfs[tiempos_por_proyecto]
for i, row in enumerate(test_tiempo_proyectos.itertuples()):
    if i == 1:
        for j in range(1, 13):
            proyectos[j]['tiempo'] = row[j + 1]
            proyectos[j + 12]['tiempo'] = row[j + 1]
