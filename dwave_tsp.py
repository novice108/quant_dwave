from collections import defaultdict
import networkx as nx

# ------- Set up our graph -------
# Create empty graph
G = nx.complete_graph(4)
G.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1), (1, 2, .1), (1, 3, .5), (2, 3, .1)})

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dimod
import dwave_networkx as dnx

ans = dnx.traveling_salesperson (G, sampler=dimod.ExactSolver(), start=0)
print("ExactSolver [0 1 2 3] ") 
print(ans) #Calculated by Electronic computer

# ------- Set up our QUBO dictionary -------
Q = defaultdict(int) # Initialize our Q matrix
# Update Q matrix for every edge in the graph
for i, j in G.edges:
    Q[(i,i)]+= -1
    Q[(j,j)]+= -1
    Q[(i,j)]+= 2

# ------- Run our QUBO on the QPU -------
# Set up QPU parameters
chainstrength = 1.0
numruns = 100
Q = dnx.traveling_salesperson_qubo(G)

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler())
d_answer = dnx.traveling_salesperson(G, sampler, start=0)
print("QuantumSolver")
print(d_answer) #Calculated by Quantum Computer or Hybrid Server (Electronic+Quantum)
