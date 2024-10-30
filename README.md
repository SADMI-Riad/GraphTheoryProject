# Graph Theory Application

### Authors:
- **Sadmi Mohammed Riad**: 3rd Year ISIL, USTHB
- **Mezghenna Mohanned**: 3rd Year Software Engineering, USTHB

## Project Overview

The Graph Theory Application is an interactive, educational tool designed to support the creation, visualization, and manipulation of graphs. It integrates a suite of graph algorithms and visualization tools to make complex concepts accessible and engaging.

## Features

- **Graph Creation & Manipulation**: Interactive creation of vertices and edges with easy-to-use visual controls.
- **Algorithm Visualizations**: Dynamic animations for each algorithm, making abstract concepts more accessible and engaging.

## Technologies Used

<div align="center">
    <img src="https://img.icons8.com/color/48/000000/python.png" alt="Python" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg" alt="Matplotlib" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" alt="NumPy" width="60" />
</div>

---

## Algorithms

Each algorithm is implemented with a focus on educational clarity and interactive visualization.

- **Welsh-Powell Graph Coloring**:
  - **Purpose**: This algorithm assigns colors to nodes in a way that no two adjacent nodes share the same color. The algorithm minimizes the number of colors, making it suitable for chromatic number calculations and graph coloring challenges.
  - **Visualization**: Animates each step of the coloring process, showcasing how the algorithm prioritizes high-degree nodes for efficient color allocation.

- **Prim’s Minimum Spanning Tree (MST)**:
  - **Purpose**: Prim’s algorithm constructs a minimum spanning tree by selecting the cheapest edge connecting the tree to a new vertex. It’s widely used in network design to create efficient, minimal-cost connections.
  - **Visualization**: Displays the growth of the spanning tree in real-time, highlighting each added edge and demonstrating the principle of building a tree with minimal weight.

- **Dijkstra’s Shortest Path**:
  - **Purpose**: Calculates the shortest path from a selected source node to all other nodes in the graph, optimizing travel distances. Dijkstra’s algorithm is foundational for navigation, logistics, and network routing applications.
  - **Visualization**: Shows the incremental path expansion, enabling users to see how the algorithm evaluates and updates the shortest paths dynamically.

- **Bellman-Ford Algorithm**:
  - **Purpose**: Similar to Dijkstra’s, but capable of handling graphs with negative weights. Bellman-Ford not only finds the shortest path from a source node but also detects negative weight cycles, making it critical for applications involving debt calculation, economic models, and more.
  - **Visualization**: Demonstrates each relaxation step of the algorithm, illustrating how distances are updated, and highlights any detected cycles.

- **Maximal Stable Set Calculation**:
  - **Purpose**: Identifies a stable set in which no two nodes are adjacent, offering insight into graph stability. This is applicable in fields like scheduling, matching, and resource allocation.
  - **Visualization**: Highlights the nodes in the maximal stable set, offering a clear visual representation of non-adjacent, stable nodes.

## Getting Started

### Prerequisites

To run the application, install the following dependencies:

- Python 3.x
- PyQt5
- Matplotlib
- NetworkX
- NumPy

Install dependencies with:
```bash
pip install -r requirements.txt
