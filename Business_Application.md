# Business Application of Quantum Algorithm for the Sensitivity Analysis of Business Risks


# Quantum algorithm

- Problem definition: 
Quantum algorithms are known for super-polynomial speedup over their classical counterparts.
They can be applied to various real-world problems such as cryptography, optimisation, and simulations. 

- Compilation (Processor design / gate implementation)

- Performance analysis: 
 Following the methology by Deutsche Börse Group we present a quantum algorithm (namely Grover's algorithm) to address the sensitivity analysis for a business risk model, which found to be computationally too expensive to perform by classical algorithms. 
Grover's algorithm (1996) is known for its ability to address unstructured search problems, which are basic problems in computer science.
Here, we implement and analysis the risk modeling and its representation on quantum circuits using this algorithm and the Quantum Amplitude Estimation (QAE). 
The fact that quantum algorithms are faster than a classical ones can be tested by the code execution runtime, measured by the number of elementary operations used by an algorithm, and can be done using the quantum circuit model. 
The quantum program employed here is fast (as compared to classical ones, e.g. quasi-Monte Carlo methods), requires low number of qubits (~200), and has an interesting nested structure: Grover's algorithm\QAE\Quantum risk model.

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
