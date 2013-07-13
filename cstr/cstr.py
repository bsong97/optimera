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
k1 = 5.0/6.0        # min-1
k2 = 5.0/3.0        # min-1
k3 = 1.0/6000.0     # m3/mol.min

# Import
from coopr.pyomo import *

# Instantiate model
model = ConcreteModel()

# Decision variable - the space velocity SV = F/V
model.sv = Var(initialize=1.0, within=PositiveReals)
model.ca = Var(initialize=5000.0, within=PositiveReals)
model.cb = Var(initialize=2000.0, within=PositiveReals)
model.cc = Var(initialize=2000.0, within=PositiveReals)
model.cd = Var(initialize=1000.0, within=PositiveReals)

# Objective - maximize concentration of B
model.obj = Objective(expr=model.cb, sense=maximize)

# Constraints - they have to obey the ODEs
def ode_1(model):
    return model.sv*c_af - model.sv*model.ca - k1*model.ca - 2.0*k3*model.ca**2.0 == 0
    
def ode_2(model):
    return -model.sv*model.cb - k1*model.ca - k2*model.cb == 0

def ode_3(model):
    return -model.sv*model.cc + k2*model.cb == 0
    
def ode_4(model):
    return -model.sv*model.cd + k3*model.ca**2.0 == 0
    
model.ca_bal = Constraint(rule=ode_1)
model.cb_bal = Constraint(rule=ode_2)
model.cc_bal = Constraint(rule=ode_3)
model.cd_bal = Constraint(rule=ode_4)


#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python cstr.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()