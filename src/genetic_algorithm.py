#!/usr/bin/env python
# coding: utf-8

# 1. Create a string that translates into a quantum circuit - different strings, encode different gates/templates
# 2. Randomly generate agents (agents are quantum circuits)
# 3. Train all agents and use combination of energy and circuit complexity as fitness
# 4. Do "natural selection", cross between agents to create offspring and randomly mutate agents
# 5. Repeat for some generations

import os, sys
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("./")

from vqe import ground_state_energy_VQE
import random
import pennylane as qml
from pennylane import qchem
import numpy as np

def string_to_gate(string, n_qubits):
    # first six bits of string define gate time, rest define which qubits to apply to
    n_params = 0
    complexity = 0 # ad-hoc value to assess complexity of gate
    gate_string = string[:6]
    qubit_string = string[6:]
    qubit_seed = int(qubit_string, 2)
    qubits = np.random.RandomState(seed=qubit_seed).permutation(n_qubits)
    if gate_string == '000000':
        def gate(theta):
            qml.RX(theta, wires=qubits[0])
        n_params = 1
        complexity = 2
    elif gate_string == '000001':
        def gate(theta):
            qml.RY(theta, wires=qubits[0])
        n_params = 1
        complexity = 2
    elif gate_string == '000010':
        def gate(theta):
            qml.RZ(theta, wires=qubits[0])
        n_params = 1
        complexity = 2
    elif gate_string == '000100':
        def gate():
            qml.CY(wires=qubits[:2])
        complexity = 2
    elif gate_string == '000101':
        def gate():
            qml.CZ(wires=qubits[:2])
        complexity = 2
    elif gate_string == '000110':
        def gate(theta):
            qml.CRX(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '000111':
        def gate(theta):
            qml.CRY(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '001000':
        def gate(theta):
            qml.CRZ(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '001001':
        def gate():
            qml.PauliX(wires=qubits[0])
    elif gate_string == '001010':
        def gate():
            qml.PauliY(wires=qubits[0])
    elif gate_string == '001011':
        def gate():
            qml.PauliZ(wires=qubits[0])
    elif gate_string == '001100':
        def gate(theta):
            qml.PhaseShift(theta, wires=qubits[0])
        n_params = 1
        complexity = 1
    elif gate_string == '001101':
        def gate():
            qml.QubitCarry(wires=qubits[:4])
        complexity = 3
    elif gate_string == '001111':
        def gate():
            qml.QubitSum(wires=qubits[:3])
        complexity = 3
    elif gate_string == '010000':
        def gate(theta, phi, omega):
            qml.Rot(theta, phi, omega, wires=qubits[0])
        n_params = 3
        complexity = 2
    elif gate_string == '010001':
        def gate():
            qml.S(wires=qubits[0])
    elif gate_string == '010010':
        def gate():
            qml.SQISW(wires=qubits[:2])
        complexity = 2
    elif gate_string == '010011':
        def gate():
            qml.SWAP(wires=qubits[:2])
        complexity = 1
    elif gate_string == '010100':
        def gate():
            qml.SX(wires=qubits[0])
        complexity = 1
    elif gate_string == '010101':
        def gate(theta):
            qml.SingleExcitation(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '010110':
        def gate(theta):
            qml.SingleExcitationPlus(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '010111':
        def gate(theta):
            qml.SingleExcitationMinus(theta, wires=qubits[:2])
        n_params = 1
        complexity = 3
    elif gate_string == '011000':
        def gate():
            qml.Toffoli(wires=qubits[:3])
        complexity = 2
    elif gate_string == '011001':
        def gate(theta):
            qml.U1(theta, wires=qubits[0])
        n_params = 1
        complexity = 1
    elif gate_string == '011010':
        def gate(theta, phi):
            qml.U2(theta, phi, wires=qubits[0])
        n_params = 2
        complexity = 1
    elif gate_string == '011011':
        def gate(theta, phi, delta):
            qml.U3(theta, phi, delta, wires=qubits[0])
        n_params = 3
        complexity = 2
    elif gate_string == '011101':
        def gate(theta):
            qml.DoubleExcitation(theta, wires=qubits[:4])
        n_params = 1
        complexity = 4
    elif gate_string == '011110':
        def gate(theta):
            qml.DoubleExcitationPlus(theta, wires=qubits[:4])
        n_params = 1
        complexity = 4
    elif gate_string == '011111':
        def gate(theta):
            qml.DoubleExcitationMinus(theta, wires=qubits[:4])
        n_params = 1
        complexity = 4
    else:
        gate = None
    return gate, n_params, complexity


def genome_to_circuit(genome, n_qubits, n_gates):
    """
    # Set string and transform it into a quantum circuit.

    """
    gates = []
    n_params = []
    total_complexity = 0
    gene_length = len(genome) // n_gates
    for i in range(n_gates):
        gene = genome[i * gene_length : (i+1) * gene_length]
        gate, n, complexity = string_to_gate(gene, n_qubits)
        if gate is not None:
            gates.append(gate)
            n_params.append(n)
            total_complexity += complexity

    def circuit(params):
        param_counter = 0
        for gate, n in zip(gates, n_params):
            if n == 0:
                gate()
            elif n == 1:
                gate(params[param_counter])
            elif n == 2:
                gate(params[param_counter], params[param_counter + 1])
            elif n == 3:
                gate(params[param_counter], params[param_counter + 1], params[param_counter + 2])
            param_counter += n
    total_params = sum(n_params)
    return circuit, total_params, total_complexity

class Agent:
    """
    1. Create a population of agents
    2. Evaluate the fitness of each one
    3. Select between the best agents
    4. Breed between them
    5. Random mutate genes of the genome of the agent
    """

    def __init__(self, length):
        self.string = ''.join(str(random.randint(0,1)) for _ in range(length))
        self.fitness = -1
        self.energy = 0

    def __str__(self):
        return ' String: ' + str(self.string) + ' Fitness: ' + str(np.round(self.fitness,6)) + ' Energy: ' + str(self.energy)


def init_agents(population, length):
    return [Agent(length) for _ in range(population)]


def ga(population, generations, threshold, str_len, n_qubits, n_gates, H, initial_state):
    agents = init_agents(population, str_len)

    for generation in range(generations):
        print("Generation: ", str(generation))

        agents = fitness(agents, n_qubits, n_gates, H, initial_state)
        agents = selection(agents)
        agents = crossover(agents, str_len, population)
        agents = mutation(agents, str_len)

        if any(agent.fitness >= threshold for agent in agents):
            print("\U0001F986 Thereshold has been met! Winning genome: ", agents[0].string)
            return agents[0].string

    return agents[0].string

def fitness(agents, n_qubits, n_gates, H, initial_state):
    for agent in agents:
        genome = agent.string
        circuit, n_params, total_complexity = genome_to_circuit(genome, n_qubits, n_gates)
        energy = ground_state_energy_VQE(H, initial_state, circuit, n_params)
        agent.fitness = -energy - total_complexity * 0.0001
        agent.energy = energy
    return agents

def selection(agents):
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print('\n'.join(map(str, agents)))

    # Natural selection
    kill_param = 0.2 # take the top 20% of the individuals
    agents = agents[:int(kill_param * len(agents))]
    return agents

def crossover(agents, str_len, population):
    offspring = []
    for _ in range( int((population - len(agents))/2)):
        # TODO: don't breed parents that are the same
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        child1 = Agent(str_len)
        child2 = Agent(str_len)
        split = random.randint(0,str_len)
        child1.string = parent1.string[0:split] + parent2.string[split:str_len]
        child2.string = parent2.string[0:split] + parent1.string[split:str_len]

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)
    return agents

def mutation(agents, str_len):
    chance_of_mutation = 0.20
    for agent in agents:
        for idx, param in enumerate(agent.string):
            if random.uniform(0.0,1.0) <= chance_of_mutation:
                agent.string = agent.string[0:idx] + str(random.randint(0,1)) + agent.string[idx+1:str_len]

    return agents


if __name__ == "__main__":
    molecule = 'h2'
    # molecule = 'h2o'
    if molecule == 'h2o':
        # for the water molecule, with 4 frozen orbitals
        symbols = ["H", "O", "H"]
        coordinates = np.array([-0.0399, -0.0038, 0.0, 1.5780, 0.8540, 0.0, 2.7909, -0.5159, 0.0])
        H, n_qubits = qchem.molecular_hamiltonian(
            symbols,
            coordinates,
            active_electrons=4,
            active_orbitals=4
        )
        initial_state = qchem.hf_state(4, 8)

    # for the hydrogen molecule
    else:
        symbols = ["H", "H"]
        coordinates = np.array([0.0, 0.0 , -0.6614, 0.0, 0.0, 0.6614])
        H, n_qubits = qchem.molecular_hamiltonian(
            symbols,
            coordinates
        )
        initial_state = qchem.hf_state(2, 4)

    dev = qml.device('default.qubit', wires=n_qubits)

    # You can tune these parameters
    population = 10
    generations = 5
    threshold = 200
    n_gates = 6
    str_len = n_gates * (6 + 5)

    #Run genetic algorithm
    final_circuit = ga(population, generations, threshold, str_len,
                       n_qubits, n_gates, H, initial_state)
