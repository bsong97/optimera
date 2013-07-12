# Example: CSTR or van de vusse reaction
# A -> B -> C
# 2A -> D
# B is desired product, but C and D are undesired products

# Goal is to produce B from feed containing A
# Objective is to solve for optimal reactor volume that produces
# maximum outlet concentration for B

# Steady state mole balance:
    # A: F/V*c_af - F/V*c_a - k1*c_a - 2*k3*c_a**2 = 0
    # B: -F/V*c_b + k1*c_a - k2*c_b = 0
    # C: -F/V*c_c + k2*c_b = 0
    # D: -F/V*c_d + k3*c_a**2 = 0
        

# Kinetic and concentration data in the process
c_af = 10           # gmol/m3
k1 = float(5/6)     # min-1
k2 = float(5/3)     # min-1
k3 = float(1/6000)  # m3/mol.min

# Import
from coopr.pyomo import *

# Instantiate model
model = ConcreteModel()

# Decision variable - the space velocity SV = F/V
model.vol = Var(SV)

# Objective
model.obj = Objective()