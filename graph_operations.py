import numpy as np
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
    node_id = len(pos) + 1
    pos[node_id] = (x, y)
    G.add_node(node_id)
    redrawGraph(ax, G, pos, [], canvas)

def draw_edge(ax, pos, node1, node2, weight, canvas):
    x1, y1 = pos[node1]
    x2, y2 = pos[node2]
    if node1 != node2:
        rad = 0.35
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", color="black", lw=1,
            connectionstyle=f"arc3,rad={rad}", shrinkA=12, shrinkB=12, mutation_scale=15
        )
        ax.add_patch(arrow)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        offset_x, offset_y = (y2 - y1) * rad, (x1 - x2) * rad
        text_x, text_y = mid_x + offset_x, mid_y + offset_y
        ax.text(text_x, text_y, str(weight), color="red", fontsize=8, ha="center", va="center")
    else:
        rad = 0.3
        loop = FancyArrowPatch(
            (x1, y1), (x1, y1), arrowstyle="-|>", color="black", lw=1,
            connectionstyle=f"arc3,rad={rad}", shrinkA=10, shrinkB=10, mutation_scale=20
        )
        ax.add_patch(loop)
        ax.text(x1, y1 + rad * 1.5, str(weight), color="red", fontsize=12, ha="center")
