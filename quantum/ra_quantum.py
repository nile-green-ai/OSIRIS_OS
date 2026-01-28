"""
RA_QUANTUM
Quantum Awareness Sampling Layer
Bridges OSIRIS_RA into quantum state space
"""

from qiskit import QuantumCircuit, Aer, execute
import math

class RA_QUANTUM:
    def __init__(self, qubits=2):
        self.qubits = qubits
        self.backend = Aer.get_backend("qasm_simulator")

    def sample_awareness(self, awareness_level: float):
        """
        Map awareness -> rotation angle
        """
        theta = awareness_level * math.pi

        qc = QuantumCircuit(self.qubits, self.qubits)

        for q in range(self.qubits):
            qc.ry(theta, q)
            qc.h(q)

        qc.measure(range(self.qubits), range(self.qubits))

        job = execute(qc, self.backend, shots=256)
        result = job.result().get_counts()

        return {
            "theta": theta,
            "distribution": result
        }

