# Graph Theory Application

A powerful and interactive tool for creating, visualizing, and manipulating graphs with real-time algorithm animations.

<div align="center">
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
    <img src="https://img.shields.io/badge/license-GPL--3.0-blue" alt="License">
    <img src="https://img.shields.io/badge/release-v1.0-blue" alt="Release Version">
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python Version">
</div>

---

## Overview

The Graph Theory Application provides an intuitive interface for graph theory operations, including graph creation, manipulation, and algorithm animations. This project aims to support students, researchers, and developers in exploring graph theory concepts through interactive visuals. The application includes implementations of various graph algorithms with real-time visual feedback, making abstract graph theory concepts accessible and engaging.

---

## Features

- **Graph Creation & Manipulation**: Interactive creation of vertices and edges with easy-to-use visual controls.
- **Algorithm Visualizations**:
  - **Welsh-Powell Graph Coloring**: Assign colors to graph nodes such that no two adjacent nodes share the same color, minimizing the number of colors.
  - **Prim’s Minimum Spanning Tree**: Visualize the minimum spanning tree of a weighted graph, connecting all nodes with the smallest possible edge weights.
  - **Dijkstra’s Shortest Path**: Find the shortest path in a graph from a source node, useful for navigation and pathfinding.
  - **Bellman-Ford Algorithm**: Compute shortest paths for graphs with negative weights, detecting negative weight cycles if they exist.
- **Stable Set Calculation**: Identify maximal sets of non-adjacent nodes, useful in resource allocation and scheduling problems.

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

- **Python 3.x**
- **PyQt5**
- **Matplotlib**
- **NetworkX**
- **NumPy**

Install dependencies with:
```bash
pip install -r requirements.txt
