# Product mix problem
# Wyndor produces door and windows
# Each of three plants with different with available hours that can produce doors and windows
# 
# The aim is to maximise the profit available in the limited hours of production

# At high level, pyomo consists of:
    # Variables that are calculated during the optimization
    # Objectives (function) that take data and variables, and is either maximized or minimzed
    # Constraints that limit values of 
 
"""Wyndor model from Hillier and Hillier *Introduction to Management Science*

It has three main sections:
- model
- objective
- constraint

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo wyndor.py

"""

# Import
from coopr.pyomo import (ConcreteModel,
                         Objective, 
                         Var, 
                         NonNegativeReals, 
                         maximize, 
                         Constraint)

# Plant data
Products = ['Doors', 'Windows']
ProfitRate = {'Doors':300, 'Windows':500}
Plants = ['Door Fab', 'Window Fab', 'Assembly']
HoursAvailable = {'Door Fab':4, 'Window Fab':12, 'Assembly':18}
HoursPerUnit = {('Doors', 'Door Fab'):1,
                ('Windows', 'Window Fab'):2,
                ('Doors', 'Assembly'):3,
                ('Windows', 'Assembly'):2,
                ('Windows', 'Door Fab'):0,
                ('Doors', 'Window Fab'):0}
                
# Concrete Model
model = ConcreteModel() # instantiates the data of the problem, such as hours available from the plant
# Decision variables
model.WeeklyProd = Var(Products, within=NonNegativeReals)

# Objective
model.obj = Objective(expr = sum(ProfitRate[i] * model.WeeklyProd[i] for i in Products), 
                      sense=maximize)
                      
def CapacityRule(model, p):
    """User defined capacity rule - 
    Accepts a pyomo Concrete Model as the first positional argument,
    and a plant index as a second positional argument
    """
    return sum(HoursPerUnit[i,p] * model.WeeklyProd[i] for i in Products) <= HoursAvailable[p]
    
# Constraint
model.Capacity = Constraint(Plants, rule=CapacityRule)
    

#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python wyndor.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()