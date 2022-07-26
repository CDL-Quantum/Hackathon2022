# Business Application of Quantum Algorithm for the Sensitivity Analysis of Business Risks


# Quantum algorithm

- Problem definition: 
Quantum algorithms are known for super-polynomial speedup over their classical counterparts.
They can be applied to various real-world problems such as cryptography, optimisation, and simulations. 

- Performance analysis: 
 Following the methology by Deutsche Börse Group we present a quantum algorithm (namely Grover's algorithm) to address the sensitivity analysis for a business risk model, which found to be computationally too expensive to perform by classical algorithms. 
Grover's algorithm (1996) is known for its ability to address unstructured search problems, which are basic problems in computer science.
Here, we implement and analysis the risk modeling and its representation on quantum circuits using this algorithm and the Quantum Amplitude Estimation (QAE). 
The fact that quantum algorithms are faster than a classical ones can be tested by the code execution runtime, measured by the number of elementary operations used by an algorithm, and can be done using the quantum circuit model. 
The quantum program employed here is fast (as compared to classical ones, e.g. quasi-Monte Carlo methods), requires low number of qubits (~200), and has an interesting nested structure: Grover's algorithm\QAE\Quantum risk model.


# The business risk model and analysis: 
The impact of external adverse developments on future revenues in any business can be addressed within a risk model.
A risk model estimates the overall likelihood of impacts that would threaten the business.
Thus we are dealing with a probablity problem.
To define the problem, a threshold $A$ for a financial impact is defined.
The probability $P(A)$ shows probability that the financial impact bigger than $A$, and $P_{max}$ is the maximal acceptable value of $P(A)$.
In the business risk model, to avoide loss, an action needs to taken when $P(A)$ reaches it maximum value $P_{max}$.

The estimated $P(A)$ is based on some estimated parameters (inputs) and we are interested in finding the parameter(s) that when changed
slightly, influence the output of the model such that $P(A)>P_{max}$.

- Compilation (Processor design / gate implementation):
The implementation of the quantum program and simulations are done using Qiskit.

In this work (to-be rephrased):
we show that the oracles we consider lower the success probability by a constant factor compared to standard oracles. 
we achieve a success probability of at least 81% (rather than nearly 100% in conventional Grover), which is inherited from the QAE. 


# Potential customers

Potential customers for the Sensitivity Analysis of Business Risks includes banks, and any financial institute dealing with risk analysis
and any company dealing with portfolio..

Such analyses can be found in a wide range of applications such as ..


# References

[1] M.C. Braun et al., A Quantum Algorithm for the Sensitivity Analysis of Business Risks (2021), https://arxiv.org/abs/2103.05475

[2] A. Montanaro, Quantum algorithms: an overview, npj Quantum Information (2016) 2, 15023.

[3]

[4]

[5]
