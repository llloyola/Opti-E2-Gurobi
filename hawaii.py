from gurobipy import GRB, Model, quicksum
from test import volumen_bodega, herramientas, insumos, proyectos, trabajadores
import pandas as pd


# Creamos el modelo
model = Model('HawaiiChile')

# Número de proyectos
# Ejemplo de 10 proyectos
N = [i for i in range(1, 11)]

# Tipos de proyectos
tipos = ['HEATING', 'VENTILATING', 'AIR CONDITIONED', 'HVAC']
servicios = ['Proyectos & Ingenieria', 'Montaje y equipos', 'Mantenimiento y reparaciones']
# tipos_de_proyectos = ['{} {}'.format(tipo, servicio) for servicio in servicios for tipo in tipos]
tipos_de_proyectos = list(range(1, 25))

# Herramientas
H = herramientas

# Insumos
K = insumos

# Períodos (días)
# Ejemplo de 40 días
T = [i for i in range(1, 61)]

# Tipos de trabajadores
# 1: Ingenieros
# 2: Técnicos
# 3: Ayudantes de Técnicos
# 4: Montajistas
# 5: Ayudantes de Montajistas
J = [i for i in range(1, 6)]
# Alterantivamente, se podría dejar como
# J = ['Ingenieros', 'Técnicos', 'Ayudantes de Técnicos', 'Montajistas', 'Ayudantes de Montajistas']

# Parámetros
V = volumen_bodega
vh_h = {i: herramientas[i]['volumen'] for i in herramientas}
vk_k = {i: herramientas[i]['volumen'] for i in insumos}
Wj = trabajadores
ch_h = {i: herramientas[i]['costos'] for i in herramientas}
ck_k = {i: herramientas[i]['costos'] for i in insumos}
IK_k0 = 0
IH_h0 = 0
kk_ka = 0
ww_ja = {}
tt_a = {a: proyectos[a]['tiempo'] for a in tipos_de_proyectos}
p = 0.5

M = float('inf')

# Definimos las distintas variables
X = model.addVars(N, tipos_de_proyectos, T, GRB.BINARY)
Y = model.addVars(N, tipos_de_proyectos, T, GRB.BINARY)
LK = model.addVars(N, K, T, GRB.CONTINUOUS)
LH = model.addVars(N, H, T, GRB.INTEGER)
IK = model.addVars(K, T, GRB.CONTINUOUS)
IH = model.addVars(H, T, GRB.INTEGER)
S = model.addVars(N, T, GRB.BINARY)

#Actualizamos el modelo
model.update()

# RESTRICCIONES
# R1:
model.addConstrs(
    (
        quicksum(X[i, a, t] * ww_ja[j][a] for i in N for a in tipos_de_proyectos) <= Wj[j]
        for j in J
        for t in T
    )
)

# R2: 
model.addConstrs(
    (
        quicksum(X[i, a, t] for a in tipos_de_proyectos) <= 1
        for i in N
        for t in T
    )
)

# R3:
model.addConstrs(
    (
        quicksum(x[i, a, t] for t in T) <= tt_a[a]
        for i in N
        for a in tipos_de_proyectos
    )
)

# R4:
model.addConstrs(
    (
        tt_a[a] * Y[i, a, t] <= quicksum(X[i, a, m] for m in range(t + 5, t + 4 + tt_a[a] + 1))
        for a in tipos_de_proyectos
        for t in T[:-4 - tt_a[a]]
        for i in N if S[i][t] == 1
    )
)

# R5:
model.addConstr(
        quicksum(Y[i, a, t] for a in tipos_de_proyectos[:12] for t in T for i in N) <= (p / 100) * quicksum(Y[i, a, t] for a in tipos_de_proyectos for t in T for i in N)
)

# R6:
model.addConstrs(
    (
        quicksum(LK[i, k, t] for k in K) + quicksum(LH[i, h, t] for h in H) <= M * S[i, t]
        for i in N
        for t in T
    )
)

# R7:
model.addConstrs(
    (
        quicksum(LH[i, h, t] for h in H) + quicksum(LK[i, k, t] for k in K) >= S[i][t]
        for i in N
        for t in T
    )
)

# R8.1:
model.addConstrs(
    (
        X[i, a, t] == quicksum(Y[i, a, m] for m in range(t - tt_a - 4, t - 5 + 1))
        for a in tipos_de_proyectos
        for t in T[tt_a[a] + 5:]
        for i in N if S[i][t] == 1
        
    )
)

# R8.2:
model.addConstrs(
    (
        X[i, a, t] == quicksum(Y[i, a, m] for m in range(t - tt_a + 1, t + 1))
        for a in tipos_de_proyectos
        for t in T[tt_a[a]:]
        for i in N if S[i][t] == 0
        
    )
)

# R10:
model.addConstrs(
    (
        quicksum(Y[i, a, t] * proyectos[a]['herramientas'][h] for i in N for a in tipos_de_proyectos) + IH[h, t] == IH[h, t - 1] + quicksum(LH[i, h, t] for i in N) + quicksum(Y[i, a, t - tt_a[a] - 4 - 1] * proyectos[a]['herramientas'][h] for a in tipos_de_proyectos if t - tt_a[a] - 4 - 1 >= 1 for i in N if S[i][t] == 1) + quicksum(Y[i, a, t - tt_a[a] + 1 - 1] * proyectos[a]['herramientas'][h] for a in tipos_de_proyectos if t - tt_a[a] + 1 - 1 >= 1 for i in N if S[i][t] == 0)
        for t in T[1:]
        for h in H
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, 1] * proyectos[a]['herramientas'][h] for i in N for a in tipos_de_proyectos) + IH[h, 1] == IH[h, 0] + quicksum(LH[i, h, 1] for i in N)
        for h in H
    )
)

# R11
model.addConstrs(
    (
        quicksum(Y[i, a, t] * proyectos[a]['insumos'][k] for i in N for a in tipos_de_proyectos) + IK[k, t] == IK[k, t - 1] + quicksum(LK[i, k, t] for i in N)
        for t in T[1:]
        for k in K
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, 1] * proyectos[a]['insumos'][k] for i in N for a in tipos_de_proyectos) + IK[k, 1] == IK[k, 0] + quicksum(LK[i, k, 1] for i in N)
        for k in K
    )
)

# R12
model.addConstrs(
    (
        quicksum(Y[i, a, m] * proyectos[a]['herramientas'][h] * vh_h[h] for h in H for m in range(t - 4, t + 1) for a in tipos_de_proyectos for i in N if S[i][t] == 1) + quicksum(Y[i, a, m] * proyectos[a]['insumos'][k] * vk_k[k] for k in K for m in range(t - 4, t + 1) for a in tipos_de_proyectos for i in N if S[i][t] == 1) + quicksum(IH[h, t] * vh_h[h] for h in H) + quicksum(IK[k, t] * vk_k[k] for k in K) <= V
        for t in T[4:]
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, m] * proyectos[a]['herramientas'][h] * vh_h[h] for h in H for m in range(1, t + 1) for a in tipos_de_proyectos for i in N if S[i][t] == 1) + quicksum(Y[i, a, m] * proyectos[a]['insumos'][k] * vk_k[k] for k in K for m in range(1, t + 1) for a in tipos_de_proyectos for i in N if S[i][t] == 1) + quicksum(IH[h, t] * vh_h[h] for h in H) + quicksum(IK[k, t] * vk_k[k] for k in K) <= V
        for t in T[:4]
    )
)

# Gap para encontrar solución
# model.setParam("MIPGap", 0.05)

# Función Objetivo
obj = quicksum(Y[i, a, t] * proyectos[a]['ganancias'] for a in tipos_de_proyectos for i in N for t in T) - (quicksum(ch_h[h] * LH[i, h, t] for h in H for t in T for i in N) + quicksum(ck_k * LK[i, k, t] for k in K for t in T for i in N))
model.setObjective(obj, GRB.MAXIMIZE)