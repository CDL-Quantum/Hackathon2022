# Business Application of Quantum Algorithm for the Sensitivity Analysis of Business Risks


# Quantum algorithms

- Problem definition: 
Quantum algorithms are known for super-polynomial speedup over their classical counterparts.
They can be applied to various real-world problems such as cryptography, optimization, and simulations. 

- Performance analysis: 
 Following the methodology by Deutsche Börse Group we present a quantum algorithm (namely Grover's algorithm) to address the sensitivity analysis for a business risk model, which found to be computationally too expensive to perform by classical algorithms. 
Grover's algorithm (1996) is known for its ability to address unstructured search problems, which are basic problems in computer science.
Here, we implement and analysis the risk modeling and its representation on quantum circuits using this algorithm and the Quantum Amplitude Estimation (QAE). 
The fact that quantum algorithms are faster than a classical ones can be tested by the code execution runtime, measured by the number of elementary operations used by an algorithm, and can be done using the quantum circuit model.
The quantum program employed here is fast (as compared to classical ones, e.g. quasi-Monte Carlo methods), requires low number of qubits (~200), and has an interesting nested structure: Grover's algorithm\QAE\Quantum risk model.


# Business risk model and analysis: 
The impact of external adverse developments on future revenues in any business can be addressed within a risk model.
A risk model estimates the overall likelihood of impacts that would threaten the business.
Thus we are dealing with a probablity problem.
To define the problem, a threshold $A$ for a financial impact is defined.
The probability $P(A)$ shows probability that the financial impact bigger than $A$, and $P_{max}$ is the maximal acceptable value of $P(A)$.
In the business risk model, to avoide loss, an action needs to taken when $P(A)$ reaches it maximum value $P_{max}$.
The estimated $P(A)$ is based on some estimated parameters (inputs) and we are interested in finding the parameter(s) that when changed
slightly, influence the output of the model such that $P(A)>P_{max}$.

The business risks is implemented as follows:
An intrinsic probability $P_i$ is defined for each relevant event (risk item, e.g. a change in stock market). An item ($i$th) is also assigned a probability to trigger another item ($j$th) with with the transition probability $P_{ij}$.
Each triggered risk item (e.g. by other items) generates a specific loss. 
The sum of the losses of the triggered items gives the total loss for a specific scenario. 
Finally, the model is evaluated by brute force (cf. ref [1] for the details).


- Compilation (circuit representation):
The implementation of the quantum program and simulations are done using Qiskit, as illustrated in the Risk_Analysis_Hackathon.ipynb file.
As shown the oracles we consider lower the success probability by a constant factor compared to standard oracles. 
A success probability of at least 81% (rather than nearly 100% in conventional Grover) is achieved, which is inherited from the QAE. 


# Quantum implementation
The sensitivity analysis of the risk model is considered as a quantum program that analyzes the impact of varying each input parameter in three steps:
1. Implementing the risk model as a quantum algorithm,
2. Implementing QAE on the outputs of the risk model,
3. Search sensitive parameters with Grover's algorithm.

For the first step, the structure of the model is translated into a quantum circuit.
In the quantum formalism the risk items are represented by qubits.
A risk item can be put into a superposition of being triggered with probability $P$ and not being triggered with probability $1-P$
by appying a rotation operator
$U_3(\theta,\phi,\lambda)$
on a qubit, with a $\theta$ that fulfil the relation $\sin(\theta/2)=P$, and the phases $\phi$ and $\lambda$ can be set to zero.
Such quantum implementation of the model turns out to be remarkably efficient as compared to the implementation on a classical computer.


# Potential customers

Potential customers for the Sensitivity Analysis of Business Risks includes banks, and any financial institute dealing with risk analysis
and any company dealing with portfolio..

Such analyses can be found in a wide range of applications such as ..


# References

[1] M.C. Braun et al., A Quantum Algorithm for the Sensitivity Analysis of Business Risks (2021), https://arxiv.org/abs/2103.05475

[2] A. Montanaro, Quantum algorithms: an overview, npj Quantum Inf 2, 15023 (2016).

[3] S. Woerner and D.J. Egger, Quantum risk analysis, npj Quantum Inf 5, 15 (2019).
