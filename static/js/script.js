var network = null;
var nodes = new vis.DataSet();
var edges = new vis.DataSet();

// Options for Cyberpunk Look
var options = {
    nodes: {
        shape: 'dot',
        size: 25,
        font: { size: 16, color: '#ffffff', face: 'Orbitron' },
        borderWidth: 2,
        color: { background: '#000000', border: '#00f2ff', highlight: '#ffffff' },
        shadow: { enabled: true, color: 'rgba(0,242,255,0.5)' }
    },
    edges: {
        width: 2,
        color: { color: 'rgba(255,255,255,0.2)', highlight: '#00f2ff' },
        smooth: { type: 'continuous' },
        font: { color: '#ffffff', strokeWidth: 0, align: 'top' }
    },
    physics: {
        stabilization: false,
        barnesHut: { gravitationalConstant: -3000, springLength: 120 }
    },
    interaction: { hover: true }
};

document.addEventListener("DOMContentLoaded", () => {
    var container = document.getElementById('mynetwork');
    network = new vis.Network(container, { nodes, edges }, options);
    fetchGraph();
});

function fetchGraph() {
    fetch('/api/get_graph')
        .then(res => res.json())
        .then(data => {
            nodes.clear();
            edges.clear();
            nodes.add(data.nodes);
            edges.add(data.edges);
        });
}

function addEdge() {
    const n1 = document.getElementById('node1').value;
    const n2 = document.getElementById('node2').value;
    const w = document.getElementById('weight').value;

    if(!n1 || !n2 || !w) return alert("Enter all fields");

    fetch('/api/add_edge', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ node1: n1, node2: n2, weight: w })
    }).then(() => {
        fetchGraph();
        document.getElementById('node1').value = '';
        document.getElementById('node2').value = '';
    });
}

async function findPath() {
    const start = document.getElementById('startNode').value;
    const end = document.getElementById('endNode').value;
    const method = document.getElementById('algoMethod').value;

    if(!start || !end) return alert("Enter Start and End nodes");

    resetVisuals();

    const response = await fetch('/api/shortest_path', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ start, end, method })
    });

    const data = await response.json();

    if(data.status === "error") {
        alert(data.message);
        return;
    }

    // Animate "Scanning"
    if(data.visit_order) {
        for (const nodeId of data.visit_order) {
            if(nodeId === start || nodeId === end) continue;
            nodes.update({id: nodeId, color: {background: '#333', border: '#ff9900'}, size: 30});
            await new Promise(r => setTimeout(r, 300));
            nodes.update({id: nodeId, color: {background: '#111', border: '#777'}, size: 25});
        }
    }

    highlightPath(data.path);

    document.getElementById('statsPanel').classList.remove('hidden');
    document.getElementById('costVal').innerText = data.cost;
    document.getElementById('visitedVal').innerText = data.visit_order.length;
    document.getElementById('pathStr').innerText = data.path.join(" ➔ ");
}

function highlightPath(path) {
    path.forEach(nodeId => {
        nodes.update({
            id: nodeId,
            color: { background: '#000', border: '#00ff44' },
            size: 35,
            shadow: { color: '#00ff44', size: 15 }
        });
    });

    for(let i=0; i<path.length-1; i++) {
        let u = path[i];
        let v = path[i+1];

        let edgeId = edges.get().find(e =>
            (e.from === u && e.to === v) || (e.from === v && e.to === u)
        )?.id;

        if(edgeId) {
            edges.update({
                id: edgeId,
                color: { color: '#00ff44', opacity: 1 },
                width: 4
            });
        }
    }
}

function resetVisuals() {
    const allNodes = nodes.getIds().map(id => ({
        id: id,
        color: { background: '#000000', border: '#00f2ff' },
        size: 25,
        shadow: { enabled: true, color: 'rgba(0,242,255,0.5)' }
    }));
    nodes.update(allNodes);

    const allEdges = edges.getIds().map(id => ({
        id: id,
        color: { color: 'rgba(255,255,255,0.2)' },
        width: 2
    }));
    edges.update(allEdges);

    document.getElementById('statsPanel').classList.add('hidden');
}

/* --- DATABASE MANAGEMENT FUNCTIONS --- */

function openDbModal() {
    document.getElementById('dbModal').classList.remove('hidden');
    fetchDbData();
}

function closeDbModal() {
    document.getElementById('dbModal').classList.add('hidden');
}

function fetchDbData() {
    fetch('/api/get_graph')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#dbTable tbody');
            tbody.innerHTML = '';

            data.edges.forEach(edge => {
                const row = `
                    <tr>
                        <td>${edge.from}</td>
                        <td>${edge.to}</td>
                        <td>${edge.label}</td>
                        <td>
                            <button onclick="deleteEdge('${edge.from}', '${edge.to}')" class="btn-sm">
                                <i class="fa-solid fa-trash"></i> Delete
                            </button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        });
}

function deleteEdge(n1, n2) {
    if(!confirm(`Delete connection between ${n1} and ${n2}?`)) return;

    fetch('/api/remove_edge', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ node1: n1, node2: n2 })
    }).then(() => {
        fetchDbData(); // Refresh Table
        fetchGraph();  // Refresh Graph in background
    });
}

function clearDatabase() {
    if(!confirm("WARNING: This will delete ALL data. Are you sure?")) return;

    fetch('/api/clear_database', { method: 'POST' })
    .then(() => {
        fetchDbData();
        fetchGraph();
        closeDbModal();
    });
}