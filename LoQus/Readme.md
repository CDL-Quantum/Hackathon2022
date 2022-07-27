# 1- Vehicle Routing Problem (VRP)

Vehicle Routing Problem (VRP) is a combinatorial optimization problem asking: "What is the optimal set of routes for vehicles to deliver to a given set of customers?" When optimizing the route option between fixed points, many constraints – e.g. vehicle number and capacities – need to be considered. VRP has proved to be NP-hard. As a result, the size of problems that can be optimized using classical methods is constrained by the computational resources.

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/VRP.png)

Except using classical combinatorial optimization and mathematical programming to solve VRP, people also proposed applying quantum computing on this problem. Quantum annealers and quantum gate devices are two major paradigms.

In this hackathon, we are going to apply filtering-Variational Quantum Eigensolver (F-VQE), which is a combination of quantum annealing process and quantum gates, to solve VRP. It should even give how many times faster compared to VQE? acceleration on top of the Variational Quantum Eigensolver (VQE) or Quantum Approximate Optimization Algorithm (QAOA).

# 2- How we solved the problem

### **Problem Hamiltonian:**

From VRP one can construct a binary polynomial optimization with equality constraints only by considering cases in which K=n-1 (K is the number of vehicles and n is the number of nodes or depos). In these cases the sub-tour elimination constraints are not necessary and the problem is only on the variable z. In particular, we can write an augmented Lagrangian as (source [here](https://qiskit.org/documentation/optimization/tutorials/07_examples_vehicle_routing.html))

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/VRP_Ham.png)

where A is a big enough parameter.

### **Filtering VQE & CVAR & Qiskit Runtime:**

Our strategy is to provide an algorithm to deliver a solution that is much faster and more accurate compared with the state-of-the-art algorithms (namely VQE and QAOA) for solving combinatorial optimization problems on gate-based quantum computers.

As a first solution, we proceeded with a new algorithm called [Filtering-VQE](https://arxiv.org/abs/2106.10055), claimed to outperform VQE and QAOA with faster convergence to the optimal solution. Our work was to implement the algorithm at the first stage and utilize this new quantum heuristic algorithm to solve VRP. See the code.

Second, in order to improve this variational quantum optimization and increases the likelihood of finding the right solution, we are working on combining the filtering VQE approach with a method called [CVAR](https://arxiv.org/pdf/1907.04769.pdf), which make the expectation value computation more accurate. As a consequence, we anticipate significantly faster and more precise results. This is a developing project.

On the other hand, IBM quantum offers Qiskit runtime to dramatically accelerate development and execution of quantum-enabled workloads by reducing the number of iterative processes in our computation. We intend to run our algorithm on Qiskit Runtime to leverage the simultaniouslty execution of multiple circuits in order to speed up our algorithm and output results much faster. We intend to use Qiskit runtime at the level of computing the gradient calculation, where we use the parameter shift rule to lead to a number of circuits executed equivalent to two times the number of parameters in the circuit for each iteration. Thanks to the QISKIT runtime, we can execute those circuits at the same time. This is a work in progress.

The below figure shows how we envision our developed algorithm. In order to maximize the likelihood of finding the ideal answer with fewer iterations, we first combine FVQE with CVAR. Second, In order to significantly shorten the runtime of our method and enable a more effective quantum approach for our vehicule routing problem, we make use of Qiskit runtime.

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/plan.png)

To briefly introduce Filtering VQE: By designing a quantum hamiltonian according to the fitness function of the given problem, the optimal route can be encoded in the lowest energy state of a qubit system. F-VQE provides an acceleration on the relaxation process of the quantum system. 

The basic idea is after applying a filtering operator F on state $\psi$, the probability of state $\psi$ will be modified by the prefactor $f^2/<F^2>$ (see equation below). Function f is chosen to be monotonically decreasing with energy Ex. So higher energy states will have smaller weight after this operation and lower energy states will increase the portion. This operation can speed up the relaxation process.

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/probability.png)

It is achieved by applying an operator (see below for a list of possible filtering operators) in each iteration that changes the probability (weight) of states according to the energy of that state. And with the extra operator, the quantum system will relax to its minimum energy state with much less iteration.

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/foperators.png)

### **FVQE results:**

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/fvqe.png)

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/histogram.png)

As we can see, filtering VQE has better convergence to the exact solution of our problem. It only requires a few iterations to reach a better estimate of the solution.

![alt text](https://github.com/walid-mk/Hackathon2022/blob/main/LoQus/path.png)

# 3- Business Part 

Quantum technology can provide a faster solution for the Vehicle Routing Problem. This way, we aim to offer a software for delivery managers that can handle many constraints and provide an optimal solution in a reasonable amount of time. Our software will take in account many factors of VRP such as: arrival and departure time gap, effective loading, vehicle limitation and number of stops on the route. Thus, delivery managers will be provided with a solution that minimizes costs and maximizes the efficiency of last mile deliveries.

It has been estimated that, for delivery companies that use route optimization softwares, the increase in productivity can be over 15% and the reduction of CO2 emissions can be about 30%.Our software aims to provide a better logistic, financial and ecological performance.

We address the route optimization software market. As customers, we target the industries that want to plan and optimize the routes of drivers to increase route efficiency and deliver in less time.

Examples of market segments can be On-demand Food Delivery, Retail & fast moving consumer goods, field services, ride hailing and taxi services.
The route optimization software market is expanding: from $M 4,325.40 in 2020 it is projected to grow to $M 16,252.04 with a CAGR of 14.2%. 

**Sources**

Allied Market Research. (2022, March). Route Optimization Software Market (No. A04093). https://www.alliedmarketresearch.com/route-optimization-software-market 

Altexsoft. (2019, September 18). How to Solve Vehicle Routing Problems:Route Optimization Software and Their APIs. https://www.altexsoft.com/blog/business/how-to-solve-vehicle-routing-problems-route-optimization-software-and-their-apis/ 

Mordor Intelligence. (2021). Route Optimization Software Market Size. https://www.mordorintelligence.com/industry-reports/route-optimization-software-marketù

# Contributors

* Walid El Maouaki
* Francesco Zappulla
* Ruolan Xue
* Dikshant Dulal
