# Graph Theory Application

### Authors:
- **Sadmi Mohammed Riad**: 3rd Year ISIL, USTHB
- **Mezghenna Mohanned**: 3rd Year Software Engineering, USTHB

## Project Overview

The Graph Theory Application is an interactive, educational tool designed to support the creation, visualization, and manipulation of graphs. Developed with a focus on clarity and user interactivity, it combines the power of graph algorithms and visualization tools to simplify complex concepts in graph theory. This application is intended for students, researchers, and enthusiasts who wish to explore graph structures, understand core algorithms, and see them in action through intuitive animations.

Graph theory is fundamental in various domains, such as computer science, mathematics, logistics, and network analysis. This project brings these concepts to life with an easy-to-use graphical interface and detailed algorithm animations, allowing users to experiment and learn through interaction.

---

## Features

### Core Functionalities

1. **Graph Creation & Manipulation**:
   - Interactive creation of vertices (nodes) and edges (connections) on a canvas.
   - Add weights to edges, representing costs, distances, or connections.
   - Real-time updates and visual cues for modifying and interacting with graph components.
   - Save and load graph states using the Pickle library, allowing for project continuity and graph data management.

2. **Algorithm Visualizations**:
   - Dynamic animations to visualize each step in graph algorithms, enhancing understanding of each process.
   - Adjustable speed settings for each animation to allow users to view steps at their own pace.
   - Real-time visual highlights for nodes and edges involved in current steps of each algorithm.

3. **Graph Data Structures**:
   - Robust data handling using `NetworkX` for efficient graph representation and operations.
   - Incorporates essential graph properties like node degree, edge weight, adjacency, and connectivity.
   - Supports both directed and undirected graphs for a wide range of applications.

### User-Friendly GUI

- **Canvas Design**: Users can create nodes by clicking directly on the canvas, with draggable edges connecting nodes.
- **Algorithm Execution Panel**: Easy-to-use buttons for executing each algorithm, with options for stopping, pausing, or replaying animations.
- **Visualization and Feedback**: Each algorithm provides real-time visual feedback, with color-coded highlights for nodes and edges, helping users grasp complex processes intuitively.

---

## Technologies Used

<div align="center">
    <img src="https://img.icons8.com/color/48/000000/python.png" alt="Python" width="60" />
    <img src="https://img.icons8.com/color/48/000000/qt.png" alt="PyQt5" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/3/30/Networkx_logo.svg" alt="NetworkX" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg" alt="Matplotlib" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" alt="NumPy" width="60" />
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Pickle_Rick.png/600px-Pickle_Rick.png" alt="Pickle" width="60" />
</div>

- **Python**: Core programming language, selected for its versatility and ease of integration with scientific libraries.
- **PyQt5**: Framework used to build the graphical user interface, enabling interactive features and a responsive design.
- **NetworkX**: Library for creating, analyzing, and visualizing graph structures. Essential for algorithm implementation and data handling.
- **Matplotlib**: Used for generating visualizations and plots of graph structures.
- **NumPy**: Provides essential support for mathematical operations and array handling.
- **Pickle**: Allows saving and loading of graph data, ensuring continuity in graph design and experimentation.

---

## Algorithms

Each algorithm is implemented to demonstrate key concepts in graph theory, with visualizations aiding understanding.

- **Welsh-Powell Graph Coloring**:
  - **Purpose**: This algorithm assigns colors to graph nodes such that no two adjacent nodes share the same color. By minimizing colors, it finds an optimal coloring solution useful in scheduling, register allocation, and more.
  - **Process**: Nodes are sorted by degree (number of connections), and each node is assigned the lowest possible color not yet used by adjacent nodes.
  - **Visualization**: Animates the process of selecting nodes and assigning colors, showcasing how the algorithm prioritizes high-degree nodes for efficient color allocation.

- **Prim’s Minimum Spanning Tree (MST)**:
  - **Purpose**: Constructs a minimum spanning tree (MST) of a weighted, connected graph, finding a subset of edges connecting all vertices with minimal total weight. This is valuable in network design, such as for road, electrical, or computer networks.
  - **Process**: Starts with a single node and repeatedly adds the cheapest edge that expands the tree, ensuring minimal weight while avoiding cycles.
  - **Visualization**: Highlights edges as they’re added to the MST, providing a step-by-step view of the tree's growth.

- **Dijkstra’s Shortest Path**:
  - **Purpose**: Computes the shortest path from a selected source node to all other nodes, optimizing travel distances or costs. Dijkstra’s algorithm is a foundational tool in navigation, logistics, and network routing.
  - **Process**: The algorithm maintains a set of nodes with known shortest paths and incrementally updates distances to other nodes until the shortest paths to all reachable nodes are determined.
  - **Visualization**: Illustrates incremental path expansion, enabling users to see how the algorithm updates the shortest paths dynamically.

- **Bellman-Ford Algorithm**:
  - **Purpose**: Similar to Dijkstra’s but can handle graphs with negative weights. It finds the shortest path from a source node while also detecting any negative weight cycles.
  - **Process**: Repeatedly relaxes edges (updating distances) to ensure optimal paths, continuing until all paths are determined or a cycle is detected.
  - **Visualization**: Shows each edge relaxation step, providing insight into how the algorithm manages updates and highlights any detected negative cycles.

- **Maximal Stable Set Calculation**:
  - **Purpose**: Finds a maximal set of non-adjacent nodes, useful in resource allocation, scheduling, and independent set analysis.
  - **Process**: Iteratively selects nodes that aren’t adjacent to already selected nodes, ensuring that no two nodes in the set are connected.
  - **Visualization**: Highlights selected nodes, providing a visual representation of the stable set within the graph.

---

## Getting Started

### Prerequisites

To run the application, you’ll need the following dependencies:

- **Python 3.x**: Core programming language for running the application.
- **PyQt5**: Required for the graphical interface, enabling interactive visual elements.
- **Matplotlib**: For plotting and visualizing graph components.
- **NetworkX**: Essential for graph representation, manipulation, and analysis.
- **NumPy**: Provides support for mathematical operations and data handling.

Install dependencies with:
```bash
pip install -r requirements.txt
