import networkx as nx
from matplotlib.patches import FancyArrowPatch

def redrawGraph(ax, G, pos, stable_set, canvas):
    ax.clear()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.axis("off")
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=700,
        node_color=["red" if node in stable_set else "skyblue" for node in G.nodes()],
        alpha=0.9,
    )
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="white")
    for node1, node2, data in G.edges(data=True):
        draw_edge(ax, pos, node1, node2, data.get("weight", 1), canvas)
    canvas.draw()

def addNode(G, pos, x, y, ax, canvas):
    if hasattr(G, 'graph_designer') and hasattr(G.graph_designer, 'node_counter'):
        node_id = G.graph_designer.node_counter  # Use node_counter instead of len(G.nodes)
        pos[node_id] = (x, y)
        G.add_node(node_id)
        G.graph_designer.node_counter += 1  # Increment the node counter
        redrawGraph(ax, G, pos, [], canvas)

def draw_edge(ax, pos, node1, node2, weight, canvas):
    if node1 != node2:
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        rad = 0.1  # Réglage de la courbure pour un rendu esthétique

        # Création de la flèche
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            color="black",
            lw=1,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=15,
            shrinkB=15,
            mutation_scale=20
        )
        ax.add_patch(arrow)

        # Position du texte pour les poids
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        offset_x, offset_y = (y2 - y1) * rad * 0.5, (x1 - x2) * rad * 0.5
        text_x, text_y = mid_x + offset_x, mid_y + offset_y
        ax.text(text_x, text_y, str(weight), color="darkblue", fontsize=7, ha="center", va="center", backgroundcolor="white")

        canvas.draw()
