from collections import defaultdict

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import networkx as nx

import matplotlib
matplotlib.use("agg")
#from matplotlib import pyplot as plt

# ------- Set up our graph -------

# Create empty graph
G = nx.complete_graph(4)
G.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1), (1, 2, .1), (1, 3, .5), (2, 3, .1)})

lg = 1 # lagrange
print("lg= ", lg)

import dwave_networkx as dnx
import dimod
#ans = dnx.traveling_salesperson (G, sampler=dimod.ExactSolver(), lagrange=lg, weight='weight', start=0)
ans = dnx.traveling_salesperson (G, sampler=dimod.ExactSolver(), start=0)
print("ExactSolver [0 1 2 3]") 
print(ans)


# ------- Set up our QUBO dictionary -------
#
# Initialize our Q matrix
Q = defaultdict(int)

# Update Q matrix for every edge in the graph
for i, j in G.edges:
    Q[(i,i)]+= -1
    Q[(j,j)]+= -1
    Q[(i,j)]+= 2

# ------- Run our QUBO on the QPU -------
# Set up QPU parameters
chainstrength = 1.0
numruns = 100

#Q = dnx.traveling_salesperson_qubo(G, lagrange=lg, weight='weight')
Q = dnx.traveling_salesperson_qubo(G)

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q, chain_strength=chainstrength, num_reads=numruns)
energies = iter(response.data())
print("response")
print(response)

#d_answer = dnx.traveling_salesperson(G, sampler, lagrange=lg, weight='weight', start=0)
d_answer = dnx.traveling_salesperson(G, sampler, start=0)
print("QuantumSolver")
print(d_answer)