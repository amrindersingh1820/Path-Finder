import heapq
from collections import deque


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        node = node.upper()
        if node not in self.adjacency_list:
            self.adjacency_list[node] = {}

    def add_edge(self, node1, node2, weight):
        node1, node2 = node1.upper(), node2.upper()
        self.add_node(node1)
        self.add_node(node2)
        self.adjacency_list[node1][node2] = weight
        self.adjacency_list[node2][node1] = weight  # Undirected

    def remove_edge(self, node1, node2):
        """Removes an edge between two nodes."""
        node1, node2 = node1.upper(), node2.upper()
        if node1 in self.adjacency_list and node2 in self.adjacency_list[node1]:
            del self.adjacency_list[node1][node2]
        # Since it's undirected, remove the reverse link too
        if node2 in self.adjacency_list and node1 in self.adjacency_list[node2]:
            del self.adjacency_list[node2][node1]

    def clear_graph(self):
        """Deletes all data."""
        self.adjacency_list = {}

    def bfs_shortest_path(self, start, end):
        start, end = start.upper(), end.upper()
        visited = set()
        visit_order = []
        queue = deque([(start, [start])])

        while queue:
            (node, path) = queue.popleft()
            if node not in visited:
                visited.add(node)
                visit_order.append(node)
                if node == end:
                    return path, visit_order
                for neighbor in self.adjacency_list.get(node, {}):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        return None, visit_order

    def dijkstra_shortest_path(self, start, end):
        start, end = start.upper(), end.upper()
        queue = [(0, start, [start])]
        visited = set()
        visit_order = []

        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node not in visited:
                visited.add(node)
                visit_order.append(node)
                if node == end:
                    return cost, path, visit_order
                for neighbor, weight in self.adjacency_list.get(node, {}).items():
                    if neighbor not in visited:
                        heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

        return float('inf'), [], visit_order