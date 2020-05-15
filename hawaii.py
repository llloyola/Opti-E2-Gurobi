from gurobipy import GRB, Model, quicksum
import pandas


def max_pos(a, b):
    minimo = min(a, b)
    return minimo if minimo >= 1 else max(a, b)


# Creamos el modelo
model = Model('HawaiiChile')

# Número de proyectos
# Ejemplo de 10 proyectos
N = [i for i in range(10)]

# Tipos de proyectos
tipos = ['HEATING', 'VENTILATING', 'AIR CONDITIONED', 'HVAC']
servicios = ['Proyectos & Ingenieria', 'Montaje y equipos', 'Mantenimiento y reparaciones']
tipos_de_proyectos = ['{} {}'.format(tipo, servicio) for servicio in servicios for tipo in tipos]

# Herramientas
H = []

# Insumos
K = []

# Períodos (días)
# Ejemplo de 40 días
T = [i for i in range(40)]

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
V = 0
vh_h = 0
vk_k = 0
Wj = {}
ch_h = 0
ck_k = 0
IK_k0 = 0
IH_h0 = 0
hh_ha = 0
kk_ka = 0
ww_ja = {}
bb_a = 0
tt_a = {}
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
        quicksum(X[i, a, t] * ww_ja[j][a] for i in N for a in tipos_de_proyectos[:12]) <= Wj[j]
        for j in J
        for i in T
    )
)

# R2: 
model.addConstrs(
    (
        quicksum(X[i, a, t] for a in tipos_de_proyectos[:12]) <= 1
        for i in N
        for t in T
    )
)

# R3:
model.addConstrs(
    (
        quicksum(x[i, a, t] for t in T) <= tt_a[a]
        for i in N
        for a in tipos_de_proyectos[:12]
    )
)

# R4:
model.addConstrs(
    (
        tt_a[a] * Y[i, a, t] <= quicksum(X[i, a, m] for m in range(t + 5, t + 4 + tt_a[a] + 1))
        for a in tipos_de_proyectos[:12]
        for t in T[:-4 - tt_a[a]]
        for i in N if S[i][t] == 1
    )
)

# R5:
model.addConstr(
        quicksum(Y[i, a, t] for a in tipos_de_proyectos[:12] for t in T for i in N) <= (p / 100) * quicksum(Y[i, a, t] for a in tipos_de_proyectos[:24] for t in T for i in N)
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
        for a in tipos_de_proyectos[:12]
        for t in T[tt_a[a] + 5:]
        for i in N if S[i][t] == 1
        
    )
)

# R8.2:
model.addConstrs(
    (
        X[i, a, t] == quicksum(Y[i, a, m] for m in range(t - tt_a + 1, t + 1))
        for a in tipos_de_proyectos[:12]
        for t in T[tt_a[a]:]
        for i in N if S[i][t] == 0
        
    )
)

# R10:
model.addConstrs(
    (
        quicksum(Y[i, a, t] * hh_ha[h][a] for i in N for a in tipos_de_proyectos[:12]) + IH[h, t] == IH[h, t - 1] + quicksum(LH[i, h, t] for i in N) + quicksum(Y[i, a, t - tt_a[a] - 4 - 1] * hh_ha[h][a] for a in tipos_de_proyectos[:12] if t - tt_a[a] - 4 - 1 >= 1 for i in N if S[i][t] == 1) + quicksum(Y[i, a, t - tt_a[a] + 1 - 1] * hh_ha[h][a] for a in tipos_de_proyectos[:12] if t - tt_a[a] + 1 - 1 >= 1 for i in N if S[i][t] == 0)
        for t in T[1:]
        for h in H
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, 1] * hh_ha[h][a] for i in N for a in tipos_de_proyectos[:12]) + IH[h, 1] == IH[h, 0] + quicksum(LH[i, h, 1] for i in N)
        for h in H
    )
)

# R11
model.addConstrs(
    (
        quicksum(Y[i, a, t] * kk_ka[k][a] for i in N for a in tipos_de_proyectos[:12]) + IK[k, t] == IK[k, t - 1] + quicksum(LK[i, k, t] for i in N)
        for t in T[1:]
        for k in K
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, 1] * kk_ka[k][a] for i in N for a in tipos_de_proyectos[:12]) + IK[k, 1] == IK[k, 0] + quicksum(LK[i, k, 1] for i in N)
        for k in K
    )
)

# R12
model.addConstrs(
    (
        quicksum(Y[i, a, m] * hh_ha[h][a] * vh_h[h] for h in H for m in range(t - 4, t + 1) for a in tipos_de_proyectos[:12] for i in N of S[i][t] == 1) + quicksum(Y[i, a, m] * kk_ka[k][a] * vk_k[k] for k in K for m in range(t - 4, t + 1) for a in tipos_de_proyectos[:12] for i in N of S[i][t] == 1) + quicksum(IH[h, t] * vh_h[h] for h in H) + quicksum(IK[k, t] * vk_k[k] for k in K) <= V
        for t in T[4:]
    )
)

model.addConstrs(
    (
        quicksum(Y[i, a, m] * hh_ha[h][a] * vh_h[h] for h in H for m in range(1, t + 1) for a in tipos_de_proyectos[:12] for i in N of S[i][t] == 1) + quicksum(Y[i, a, m] * kk_ka[k][a] * vk_k[k] for k in K for m in range(1, t + 1) for a in tipos_de_proyectos[:12] for i in N of S[i][t] == 1) + quicksum(IH[h, t] * vh_h[h] for h in H) + quicksum(IK[k, t] * vk_k[k] for k in K) <= V
        for t in T[:4]
    )
)