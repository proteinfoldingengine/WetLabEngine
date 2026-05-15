import numpy as np

channels = {
    "conductance": 0.92,
    "lineage_continuity": 0.88,
    "topology_redundancy": 0.81,
    "repair_convertibility": 0.77,
    "defect_containment": 0.84,
}

weights = {
    "conductance": 0.28,
    "lineage_continuity": 0.21,
    "topology_redundancy": 0.17,
    "repair_convertibility": 0.19,
    "defect_containment": 0.15,
}

C_repair_min = 0.34

etas = np.array(list(channels.values()))
ws = np.array(list(weights.values()))

eta_channel = ws.sum() / np.sum(ws / etas)
repair_survival = np.exp(-C_repair_min)
eta_convert = eta_channel * repair_survival

print("eta_channel =", eta_channel)
print("repair_survival =", repair_survival)
print("eta_convert =", eta_convert)

M,R,L = 0.91,0.86,0.93
lambda0 = 0.62
B_t = 125.0

C_t = M*R*L + lambda0*eta_convert*B_t
print("C_t =", C_t)
