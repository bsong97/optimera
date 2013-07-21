# Rosenbrock problem
# with two-variable Rosenbrock function
# f(x) = (1-x)2 + 100(y-x2)2
# The global minimum is in the bottom of a banana shaped valley at (1,1)


"""
Solve two-variable Rosenbrock function

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo rosenbrock.py

To display the what ratio of products need to produce to maximize the profit:

    cat results.yml
    
"""

# Import
from coopr.pyomo import (AbstractModel,
                         Var,
                         Objective,
                         minimize)
                
# Abstract Model instantiates the data of the problem, such as hours available from the plant
model = AbstractModel()

# Decision variables
model.x = Var()
model.y = Var()

# Objective - to maximize the function f(x)
def rosenbrock(model):
    return (1.0-model.x)**2 + 100.0*(model.y - model.x**2)**2

#model.objective = Objective(rule=rosenbrock, sense=minimize)
model.objective = Objective(expr=(1.0-model.x)**2 + 100.0*(model.y - model.x**2)**2, sense=minimize)


# Constraint - there is no constraint               


#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python rosenbrock.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()



# Expected result:
# x=1, y=1