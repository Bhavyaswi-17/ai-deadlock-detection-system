import networkx as nx
import matplotlib.pyplot as plt

class RagVisualizer:
    def __init__(self, processes, resources, allocation_matrix, max_matrix, available, deadlocked_processes=None):
        self.processes = processes
        self.resources = resources
        self.allocation = allocation_matrix
        self.maxm = max_matrix
        self.available = available
        self.deadlocked = deadlocked_processes if deadlocked_processes else []

    def visualize(self):
        G = nx.DiGraph()

        # ------------------------------- Add process node -------------------------------
        for i in range(self.processes):
            node = f"P{i+1}"
            color = "red" if i in self.deadlocked else "skyblue"
            G.add_node(node, color=color, shape="s")

        # ------------------------------- Add resource node -------------------------------
        for j in range(self.resources):
            node = f"R{j+1}"
            G.add_node(node, color="lightgreen", shape="o")

        # ------------------------------- Add allocation edges R -> P-------------------------------
        for i in range(self.processes):
            for j in range(self.resources):
                if self.allocation[i][j] > 0:
                    G.add_edge(f"R{j+1}", f"P{i+1}",
                               label=f"alloc {self.allocation[i][j]}")

        # ------------------------------- Compute need matrix for requests -------------------------------
        need = []
        for i in range(self.processes):
            row = []
            for j in range(self.resources):
                row.append(self.maxm[i][j] - self.allocation[i][j])
            need.append(row)
        # ------------------------------- Add request edges P -> R -------------------------------
        for i in range(self.processes):
            for j in range(self.resources):
                if need[i][j] > 0:
                    G.add_edge(f"P{i+1}", f"R{j+1}",
                               label=f"req {need[i][j]}")
        # ------------------------------- Draw the graph-------------------------------
        pos = nx.spring_layout(G, seed=42)
        node_colors = [G.nodes[n]['color'] for n in G.nodes()]

        nx.draw(
            G, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=3000,
            font_size=10
        )

        # Draw edge labels
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.title("Resource Allocation Graph (RAG)")
        plt.show()
