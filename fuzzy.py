import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Creación de las variables de entrada y salida
temperatura = ctrl.Antecedent(np.arange(0, 51, 1), 'temperatura')
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
ajuste = ctrl.Consequent(np.arange(-30, 31, 1), 'ajuste')

# Creación de los conjuntos difusos y funciones de membresía
temperatura['baja'] = fuzz.trimf(temperatura.universe, [0, 0, 18])
temperatura['ideal'] = fuzz.trimf(temperatura.universe, [18, 24, 30])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [30, 30, 40])

humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 50])
humedad['alta'] = fuzz.trimf(humedad.universe, [50, 100, 100])

ajuste['enfriar'] = fuzz.trimf(ajuste.universe, [-30, -15, 0])
ajuste['mantener'] = fuzz.trimf(ajuste.universe, [-10, 0, 10])
ajuste['calentar'] = fuzz.trimf(ajuste.universe, [0, 15, 30])

# Reglas difusas
regla1 = ctrl.Rule(temperatura['baja'] | humedad['alta'], ajuste['calentar'])
regla2 = ctrl.Rule(temperatura['ideal'], ajuste['mantener'])
regla3 = ctrl.Rule(temperatura['alta'], ajuste['enfriar'])

# Sistema de control y simulación
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])
simulacion = ctrl.ControlSystemSimulation(sistema_control)

# Entrada de datos simulados
simulacion.input['temperatura'] = 29.9
simulacion.input['humedad'] = 40

# Cálculo de la salida
simulacion.compute()
ajuste_calculado = simulacion.output['ajuste']

# Interpretar la salida y decidir la acción
if ajuste_calculado > 0:
    accion = "Calentar"
elif ajuste_calculado < 0:
    accion = "Enfriar"
else:
    accion = "Mantener"

print(f"Acción recomendada: {accion}")

# Convertir a entero y evitar la notación científica
ajuste_entero = int(ajuste_calculado)
print(ajuste_entero)

temperatura.view()
humedad.view()
ajuste.view(sim=simulacion)

plt.show()
