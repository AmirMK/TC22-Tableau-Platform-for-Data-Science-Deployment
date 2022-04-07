from ortools.algorithms import pywrapknapsack_solver
from tabpy.tabpy_tools.client import Client


#Build the optimization model to solve Knapsack problem
def Optimize_Coverage(Population,Cost, Budget):
    
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.Init(Population, [Cost], [Budget[0]])   
    solver.Solve()         
    solution=[False]*len(Population)
    for i in range(len(Population)):
        if solver.BestSolutionContains(i):            
            solution[i]=True
    return solution




# Connect to TabPy server using the client library
client = Client('http://localhost:9004/')


# Deploy Optimize_Coverage function on TabPy 
client.deploy('Optimize_Coverage',
                  Optimize_Coverage,
                  'Optimize total coverage by considering resource limitation', override = True)

