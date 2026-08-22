import sys, os
sys.path.insert(0, os.path.abspath("."))
import networkx as nx
from backend.pipeline import ingest_folder
from backend.graphs import money_graph

bundle = ingest_folder("data/final/uploads")
bank = bundle.get("bank", [])
mg = money_graph(bank)
print("Money graph nodes:", mg.number_of_nodes(), "edges:", mg.number_of_edges())

ug = mg.to_undirected()
print("Undirected nodes:", ug.number_of_nodes(), "edges:", ug.number_of_edges())

try:
    comm = list(nx.community.greedy_modularity_communities(ug, best_n=8))
    print("Greedy modularity communities (with best_n=8):", len(comm))
except Exception as e:
    print("Greedy modularity (best_n=8) FAILED:", type(e), e)

try:
    comm2 = list(nx.community.greedy_modularity_communities(ug))
    print("Greedy modularity communities (default):", len(comm2))
except Exception as e:
    print("Greedy modularity (default) FAILED:", type(e), e)

try:
    bridges = list(nx.bridges(ug))
    print("Bridges count:", len(bridges))
except Exception as e:
    print("Bridges FAILED:", type(e), e)

try:
    bc = nx.betweenness_centrality(mg, k=min(80, mg.number_of_nodes()), normalized=True)
    print("Betweenness centrality computed for nodes:", len(bc))
except Exception as e:
    print("Betweenness FAILED:", type(e), e)
