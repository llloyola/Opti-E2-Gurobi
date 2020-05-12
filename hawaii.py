from gurobipy import GRB, Model, quicksum

# Creamos el modelo
model = Model('HawaiiChile')

# Número de proyectos
# Ejemplo de 10 proyectos
N = [i for i in range(10)]

# Tipos de proyectos
tipos = ['HEATING', 'VENTILATING', 'AIR CONDITIONED', 'HVAC']
servicios = ['Proyectos & Ingenieria', 'Montaje y equipos', 'Mantenimiento y reparaciones']
tipos_de_proyectos = ['{} - {}'.format(tipo, servicio) for servicio in servicios for tipo in tipos]

# Períodos (días)
# Ejemplo de 40 días
T = [i for i in range(40)]

# Herramientas
# FALTA

# Insumos
# FALTA

# Tipos de trabajadores
# 1: Ingenieros
# 2: Técnicos
# 3: Ayudantes de Técnicos
# 4: Montajistas
# 5: Ayudantes de Montajistas
J = [i for i in range(1, 6)]
# Alterantivamente, se podría dejar como
# J = ['Ingenieros', 'Técnicos', 'Ayudantes de Técnicos', 'Montajistas', 'Ayudantes de Montajistas']

# Definimos las distintas variables
X = model.addVars(N, tipos_de_proyectos, T, GRB.BINARY)
Y = model.addVars(N, tipos_de_proyectos, T, GRB.BINARY)
LK = model.addVars(, GRB.CONTINUOUS)
LH = model.addVars(, GRB.INTEGER)
IK = model.addVars(, GRB.CONTINUOUS)
IH = model.addVars(, GRB.INTEGER)
S = model.addVars(, GRB.BINARY)

#Actualizamos el modelo
model.update()
