from flask import Flask, render_template, request, jsonify
from backend.logic import Graph
from backend.file_handler import load_graph, save_graph

app = Flask(__name__, template_folder="templates", static_folder="../static")
graph = load_graph()


@app.route('/')
def index():
    return render_template('index.html')


# --- API ENDPOINTS (For JavaScript Integration) ---

@app.route('/api/get_graph', methods=['GET'])
def get_graph_data():
    """Converts the internal graph dictionary to a format suitable for Vis.js"""
    nodes = set()
    edges = []

    # The graph is stored as adjacency_list in backend/logic.py
    for node, neighbors in graph.adjacency_list.items():
        nodes.add(node)
        for neighbor, weight in neighbors.items():
            nodes.add(neighbor)
            # Add edge (avoiding duplicates for undirected display if preferred,
            # but keeping all for directed logic)
            edges.append({
                "from": node,
                "to": neighbor,
                "label": str(weight),
                "arrows": "to"
            })

    node_data = [{"id": n, "label": n} for n in nodes]
    return jsonify({"nodes": node_data, "edges": edges})


@app.route('/api/add_edge', methods=['POST'])
def api_add_edge():
    data = request.json
    node1 = data.get('node1')
    node2 = data.get('node2')
    weight = float(data.get('weight'))

    graph.add_edge(node1, node2, weight)  # Uses logic from logic.py
    save_graph(graph)  # Uses file_handler.py

    return jsonify({"status": "success", "message": f"Edge added: {node1} -> {node2}"})


# NEW: Endpoint to remove an edge (used by script.js)
@app.route('/api/remove_edge', methods=['POST'])
def api_remove_edge():
    data = request.json
    node1 = data.get('node1')
    node2 = data.get('node2')

    graph.remove_edge(node1, node2)  # Uses logic from logic.py
    save_graph(graph)  # Uses file_handler.py

    return jsonify({"status": "success"})


# NEW: Endpoint to clear all graph data (used by script.js)
@app.route('/api/clear_database', methods=['POST'])
def api_clear_database():
    graph.clear_graph()  # Uses logic from logic.py
    save_graph(graph)  # Uses file_handler.py
    return jsonify({"status": "success"})


@app.route('/api/shortest_path', methods=['POST'])
def api_shortest_path():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    method = data.get('method')

    # Initialize variables for safe use
    path = None
    cost = None
    visit_order = []

    if method == "bfs":
        # FIX: Correctly unpacks the two return values: path and visit_order
        path, visit_order = graph.bfs_shortest_path(start, end)
        cost = 0  # BFS is unweighted
    else:
        # FIX: Correctly unpacks the three return values: cost, path, and visit_order
        cost, path, visit_order = graph.dijkstra_shortest_path(start, end)

    if path:
        # FIX: Include visit_order in the response for frontend visualization
        return jsonify({"status": "success", "path": path, "cost": cost, "visit_order": visit_order})
    else:
        return jsonify({"status": "error", "message": "No path found"})


if __name__ == '__main__':
    app.run(debug=True)