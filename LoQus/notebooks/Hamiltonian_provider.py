from time import process_time
import numpy as np
# Visualization tool
from qiskit.visualization import *
import matplotlib.pyplot as plt
import matplotlib.axes as axes

import itertools
import networkx as nx
import time
import math

from qiskit.algorithms.optimizers import GradientDescent
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile, execute
from qiskit.utils  import QuantumInstance, algorithm_globals
from qiskit.circuit import ParameterVector
from qiskit.opflow import Z, I, X, Y, ListOp, PauliExpectation, CVaRExpectation, StateFn, CircuitSampler, CircuitStateFn, ListOp

from qiskit.algorithms import VQE, QAOA

import plotly.graph_objects as go

from qiskit import BasicAer
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

import qiskit.tools.jupyter
# %qiskit_version_table

# Ignore Deprecation Warnings
import warnings
warnings.filterwarnings("ignore")


# Classes for solving the VRP problem

class Initializer():

    def __init__(self, n, b):
        self.n = n
        self.b = b

    def generate_instance(self):

        n = self.n
        b = self.b
        
        # np.random.seed(33)
        np.random.seed(100*n + b)

        xc = (np.random.rand(n) - 0.5) * 50
        yc = (np.random.rand(n) - 0.5) * 50

        instance = np.zeros([n, n])
        for ii in range(0, n):
            for jj in range(ii + 1, n):
                instance[ii, jj] = (xc[ii] - xc[jj]) ** 2 + (yc[ii] - yc[jj]) ** 2
                instance[jj, ii] = instance[ii, jj]

        return xc, yc, instance
    
    
try:
    import cplex
    from cplex.exceptions import CplexError
except: 
    print("Warning: Cplex not found.")

class ClassicalOptimizer:

    def __init__(self, instance,n,K):

        self.instance = instance
        self.n = n  # number of nodes
        self.K = K  # number of vehicles


    def compute_allowed_combinations(self):
        f = math.factorial
        return f(self.n) / f(self.K) / f(self.n-self.K)


    def cplex_solution(self):

        # refactoring
        instance = self.instance
        n = self.n
        K = self.K

        my_obj = list(instance.reshape(1, n**2)[0])+[0. for x in range(0,n-1)]
        my_ub = [1 for x in range(0,n**2+n-1)]
        my_lb = [0 for x in range(0,n**2)] + [0.1 for x in range(0,n-1)]
        my_ctype = "".join(['I' for x in range(0,n**2)]) + "".join(['C' for x in range(0,n-1)])

        my_rhs = 2*([K] + [1 for x in range(0,n-1)]) + [1-0.1 for x in range(0,(n-1)**2-(n-1))] + [0 for x in range(0,n)]
        my_sense = "".join(['E' for x in range(0,2*n)]) + "".join(['L' for x in range(0,(n-1)**2-(n-1))])+"".join(['E' for x in range(0,n)])

        try:
            my_prob = cplex.Cplex()
            self.populatebyrow(my_prob,my_obj,my_ub,my_lb,my_ctype,my_sense,my_rhs)

            my_prob.solve()

        except CplexError as exc:
            print(exc)
            return

        x = my_prob.solution.get_values()
        x = np.array(x)
        cost = my_prob.solution.get_objective_value()

        return x,cost
    

    def populatebyrow(self,prob,my_obj,my_ub,my_lb,my_ctype,my_sense,my_rhs):

        n = self.n
    
        prob.objective.set_sense(prob.objective.sense.minimize)
        prob.variables.add(obj = my_obj, lb = my_lb, ub = my_ub, types = my_ctype)
    
        prob.set_log_stream(None)
        prob.set_error_stream(None)
        prob.set_warning_stream(None)
        prob.set_results_stream(None)

        rows = []
        for ii in range(0,n):
            col = [x for x in range(0+n*ii,n+n*ii)]
            coef = [1 for x in range(0,n)]
            rows.append([col, coef])

        for ii in range(0,n):
            col = [x for x in range(0+ii,n**2,n)]
            coef = [1 for x in range(0,n)]

            rows.append([col, coef])

        # Sub-tour elimination constraints:
        for ii in range(0, n):
            for jj in range(0,n):
                if (ii != jj)and(ii*jj>0):

                    col = [ii+(jj*n), n**2+ii-1, n**2+jj-1]
                    coef = [1, 1, -1]

                    rows.append([col, coef])

        for ii in range(0,n):
            col = [(ii)*(n+1)]
            coef = [1]
            rows.append([col, coef])

        prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs)

        

class QuantumOptimizer:

    def __init__(self, instance, n, K):

        self.instance = instance
        self.n = n
        self.K = K

    def binary_representation(self,x_sol=0):

        instance = self.instance
        n = self.n
        K = self.K

        A = np.max(instance) * 100  # A parameter of cost function

        # Determine the weights w
        instance_vec = instance.reshape(n ** 2)
        w_list = [instance_vec[x] for x in range(n ** 2) if instance_vec[x] > 0]
        w = np.zeros(n * (n - 1))
        for ii in range(len(w_list)):
            w[ii] = w_list[ii]

        # Some variables I will use
        Id_n = np.eye(n)
        Im_n_1 = np.ones([n - 1, n - 1])
        Iv_n_1 = np.ones(n)
        Iv_n_1[0] = 0
        Iv_n = np.ones(n-1)
        neg_Iv_n_1 = np.ones(n) - Iv_n_1

        v = np.zeros([n, n*(n-1)])
        for ii in range(n):
            count = ii-1
            for jj in range(n*(n-1)):

                if jj//(n-1) == ii:
                    count = ii

                if jj//(n-1) != ii and jj%(n-1) == count:
                    v[ii][jj] = 1.

        vn = np.sum(v[1:], axis=0)

        # Q defines the interactions between variables
        Q = A*(np.kron(Id_n, Im_n_1) + np.dot(v.T, v))

        # g defines the contribution from the individual variables
        g = w - 2 * A * (np.kron(Iv_n_1,Iv_n) + vn.T) - \
                2 * A * K * (np.kron(neg_Iv_n_1, Iv_n) + v[0].T)

        # c is the constant offset
        c = 2 * A * (n-1) + 2 * A * (K ** 2)

        try:
            max(x_sol)
            # Evaluates the cost distance from a binary representation of a path
            fun = lambda x: np.dot(np.around(x), np.dot(Q, np.around(x))) + np.dot(g, np.around(x)) + c
            cost = fun(x_sol)
        except:
            cost = 0

        return Q, g, c, cost

    def construct_problem(self, Q, g, c) -> QuadraticProgram:
        qp = QuadraticProgram()
        for i in range(n * (n - 1)):
            qp.binary_var(str(i))
        qp.objective.quadratic = Q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

def Hamilton(n,K,b):

    initializer = Initializer(n,b)
    xc, yc, instance = initializer.generate_instance()

    classical_optimizer = ClassicalOptimizer(instance,n,K)

    x = None
    z = None
    try:
        x, classical_cost = classical_optimizer.cplex_solution()
        # Put the solution in the z variable
        z = [x[ii] for ii in range(n**2) if ii//n != ii%n]
        # Print the solution
    except: 
        pass

    algorithm_globals.massive=True
    # Instantiate the quantum optimizer class with parameters: 
    quantum_optimizer = QuantumOptimizer(instance, n, K)

    try:
        if z is not None:
            Q, g, c, binary_cost = quantum_optimizer.binary_representation(x_sol = z)
        else:
            Q, g, c, binary_cost = quantum_optimizer.binary_representation()
    except NameError as e:
        pass

    qp = quantum_optimizer.construct_problem(Q, g, c)

    quantum_instance = QuantumInstance(BasicAer.get_backend('qasm_simulator'),
                                              seed_simulator=algorithm_globals.random_seed,
                                              seed_transpiler=algorithm_globals.random_seed)

    vqe = VQE(quantum_instance=quantum_instance)
    optimizer = MinimumEigenOptimizer(min_eigen_solver=vqe)
    H, offset = optimizer._convert(qp, optimizer._converters).to_ising()
    return H, offset