import json
from backend.logic import Graph

def save_graph(graph, filename="database/data.db"):
    with open(filename, "w") as f:
        json.dump(graph.adjacency_list, f)

def load_graph(filename="database/data.db"):
    g = Graph()
    try:
        with open(filename, "r") as f:
            g.adjacency_list = json.load(f)
    except FileNotFoundError:
        pass
    return g
