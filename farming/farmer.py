# A farmer has a piece of land to be planted of Z km2 with barley, wheat, rice, maize, or different combinations. 
# The farmer has a limited amount of fertilizer, F kilograms, and pesticide, P kilograms.

# Every km2 of barley requires F1 kg of fertilizer, P1 kg of pesticide
# Every km2 of wheat requires F2 kg of fertilizer, P2 kg of pesticide
# Every km2 of rice requires F3 kg of fertilizer, P3 kg of pesticide
# Every km2 of maize requires F4 kg of fertilizer, P4 kg of pesticide

# Let S1 be selling price of barley per km2
# Let S2 be selling price of wheat per km2
# Let S3 be selling price of rice per km2
# Let S4 be selling price of maize per km2

# We denote the area of planted with barley, wheat, rice and maize as x1, x2, x3, x4
# The revenue can be maximized by choosing optimal values for x1, x2, x3 and x4.
 
# Objective: Maximize revenue for the corresponding season
 # S1*x1 + S2*x2 + S3*x3 + S4*x4
 
# Constraints:
 # x1 + x2 + x3 + x4 <= L               limit on total land
 # F1*x1 + F2*x2 + F3*x3 + F4*x4 <= F   limit on total fertilizer
 # P1*x1 + P2*x2 + P3*x3 + P4*x4 <= P   limit on total pesticide
 # x1 >= 0, x2 >= 0, x3 >= 0, x4 >= 0   cannot plant negative area
 
"""This is a fictional case that models the production of four different plants

It has three main sections:
- model
- objective
- constraint

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo farmer.py
    python farmer.py

To display how big is the area to produce each plant:

    cat results.yml
    
"""

# Import
from coopr.pyomo import (ConcreteModel,
                         Objective, 
                         Var, 
                         NonNegativeReals, 
                         maximize, 
                         Constraint)

# Information provided
Area = 100                                                      # Farmer has 100km2
Plants = ['Barley', 'Wheat', 'Rice', 'Maize']
SellingPrice = {'Barley':300, 'Wheat':200, 'Rice':250, 'Maize':380}     # selling price per km2
Resource = ['fertilizer', 'pesticide']                          # fertilizer and pesticide are constraints
Resource_available = {'fertilizer':1260, 'pesticide':780}       # amount of fertilizer and pesticide available
Resource_required = {('Barley', 'fertilizer'):4,
                     ('Wheat', 'fertilizer'):12,
                    ('Rice', 'fertilizer'):18,
                    ('Maize', 'fertilizer'):19,
                    ('Barley', 'pesticide'):5,
                    ('Wheat', 'pesticide'):4,
                    ('Rice', 'pesticide'):3,
                    ('Maize', 'pesticide'):6,}

                
# Concrete Model instantiates the data of the problem
model = ConcreteModel()
# Decision variables - varying the combination of plant types
model.SeasonProd = Var(Plants, within=NonNegativeReals)

# Objective - to maximize profit
# meaning: for each product, calculate the profit rate * production, sum all these at the end
model.obj = Objective(expr = sum(SellingPrice[i] * model.SeasonProd[i] for i in Plants), 
                      sense=maximize)

# Constraint - uses a Capacity Rule function
# meaning: for each plant, the resource used should not exceed the total resource available
def CapacityRule(model, p):
    """User defined capacity rule - 
    Accepts a pyomo ConcreteModel as the first positional argument,
    and a plant index as a second positional argument"""
    return sum(Resource_required[i,p] * model.SeasonProd[i] for i in Plants) <= Resource_available[p]
    
model.Capacity = Constraint(Resource, rule=CapacityRule)
    

#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python hansen.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()

# Results obtained:
# Revenue: 49653
# What to plant:
    # Rice: 40.77 km2
    # Barley: 131.54 km2
# fertilizer and pesticide are fully utilized