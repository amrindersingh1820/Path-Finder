from flask import Flask, render_template, request


from backend.logic import Graph
from backend.file_handler import load_graph, save_graph

app = Flask(__name__)
graph = load_graph()

@app.route('/')
def index():
   
    return render_template('index.html')

@app.route('/add_edge', methods=['POST'])
def add_edge():
    node1 = request.form['node1']
    node2 = request.form['node2']
    weight = float(request.form['weight'])
    graph.add_edge(node1, node2, weight)

    save_graph(graph)
    return render_template('index.html', message=f"Edge added: {node1} - {node2} ({weight})")

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    
    start = request.form['start']
    end = request.form['end']
    method = request.form['method']

    if method == "bfs":
        path = graph.bfs_shortest_path(start, end)
        cost = "Unweighted Path"
    else:
        cost, path = graph.dijkstra_shortest_path(start, end)

    if path:
        return render_template('result.html', path=path, cost=cost)
    else:
        return render_template('result.html', path=None, cost=None)

if __name__ == '__main__':
    app.run(debug=True)
