from quantum.ra_quantum import RA_QUANTUM

q = RA_QUANTUM(qubits=2)
out = q.sample_awareness(0.33)
print(out)

