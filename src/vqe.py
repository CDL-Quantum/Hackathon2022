import pennylane as qml
from pennylane import numpy as np

def ground_state_energy_VQE(H, initial_state, circuit, n_params, total_complexity=None):
    """Perform VQE to find the ground state energy of the H2O Hamiltonian.

    Args:
        - circuit (func) : a function that describes the circuit

    Returns:
        - (float): The ground state energy
    """
    ##
    n_qubits = len(initial_state)
    dev = qml.device("default.qubit", wires=n_qubits)
    hf_state = initial_state

    @qml.qnode(dev)
    def cost_fn(param):
        qml.BasisState(hf_state, wires=range(n_qubits))
        circuit(param)
        return qml.expval(H)

    # Circuit for printing
    @qml.qnode(dev)
    def xcircuit():
        qml.BasisState(hf_state, wires=range(n_qubits))
        circuit(theta)
        return qml.probs(wires=range(n_qubits))

    if n_params == 0:
        cost = cost_fn(0)
        theta = 0
        print(qml.draw(xcircuit)())
        return cost

    opt = qml.AdamOptimizer(stepsize=0.5)
    theta = np.random.normal(0, 0.1, n_params)
    max_iterations = 150
    conv_tol = 1e-09
    energy = 10000000
    for n in range(max_iterations):
        prev_energy = energy
        theta, energy = opt.step_and_cost(cost_fn, theta)
        conv = np.abs(energy - prev_energy)
        if conv <= conv_tol:
            break
    print(qml.draw(xcircuit)())
    return energy