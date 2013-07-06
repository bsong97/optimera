# Product mix problem
# Hansen produces orange, apple, grape and mixed fruit juice
# Hansen has four plants located at California, Washington, Oregon and British Columbia
# Each of four plants has different available hours that can produce different type of juice
# 
# The aim is to maximise the profit with the limited hours of production available 

# At high level, pyomo consists of:
    # Variables that are calculated during the optimization
    # Objectives (function) that take data and variables, and is either maximized or minimzed
    # Constraints that limit values of 
 
"""This is a fictional case that models the production of fruit juices by Hansen

It has three main sections:
- model
- objective
- constraint

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo hansen.py
    python hansen.py

"""

# Import
from coopr.pyomo import (ConcreteModel,
                         Objective, 
                         Var, 
                         NonNegativeReals, 
                         maximize, 
                         Constraint)

# Plant data
Products = ['Orange', 'Apple', 'Grape', 'Mixed']
ProfitRate = {'Orange':3, 'Apple':2, 'Grape':1, 'Mixed':5}
Plants = ['California', 'Oregon', 'BritishColumbia', 'Washington']
HoursAvailable = {'California':4, 'Oregon':12, 'Washington':18, 'BritishColumbia':9}
HoursPerUnit = {('Orange', 'California'):0.0051,
                ('Orange', 'Oregon'):0.0048,
                ('Orange', 'Washington'):0.0047,
                ('Orange', 'BritishColumbia'):0,
                ('Apple', 'California'):0.0063,
                ('Apple', 'Oregon'):0.0061,
                ('Apple', 'Washington'):0.0059,
                ('Apple', 'BritishColumbia'):0.0063,
                ('Grape', 'California'):0.0088,
                ('Grape', 'Oregon'):0.0087,
                ('Grape', 'Washington'):0.,
                ('Grape', 'BritishColumbia'):0.,
                ('Mixed', 'California'):0.012,
                ('Mixed', 'Oregon'):0.0123,
                ('Mixed', 'Washington'):0.,
                ('Mixed', 'BritishColumbia'):0.,}

                
# Concrete Model instantiates the data of the problem, such as hours available from the plant
model = ConcreteModel()
# Decision variables
model.WeeklyProd = Var(Products, within=NonNegativeReals)

# Objective - to maximize profit
# meaning: for each product, calculate the profit rate * production, sum all these at the end
model.obj = Objective(expr = sum(ProfitRate[i] * model.WeeklyProd[i] for i in Products), 
                      sense=maximize)

# Constraint - uses a Capacity Rule function
# meaning: for each product, the HoursPerUnit for each product in each plant 
# should not exceed the hours available for all plant                 
def CapacityRule(model, p):
    """User defined capacity rule - 
    Accepts a pyomo ConcreteModel as the first positional argument,
    and a plant index as a second positional argument"""
    return sum(HoursPerUnit[i,p] * model.WeeklyProd[i] for i in Products) <= HoursAvailable[p]
    
model.Capacity = Constraint(Plants, rule=CapacityRule)
    

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
    

# Expected result:
# Maximum profit = 2352.94
#