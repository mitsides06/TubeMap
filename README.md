# Tube Map Pathfinding Simulator

## Project Description
This project presents an implementation of Dijkstra's algorithm tailored to optimize route finding within the London Tube network. It enables users to determine the fastest route between any two given stations, taking into account the intricate layout and connectivity of the Tube system.

## Project Structure

```
Project folder/
├─ data/
│  ├─ london.json
├─ network/
│  ├─ path.py
│  ├─ graph.py
├─ tube/
│  ├─ components.py
│  ├─ map.py
├─ main.py
```

### `data/`

Contains the JSON file `london.json` describing the London Tube map.

### `network/`

- `path.py` contains the `PathFinder` class, used to compute the shortest path between two stations.


- `graph.py` contains the `NeighbourGraphBuilder` class, used to generate the abstract graph representing the Tube Map.


### `tube/`

- `components.py` contains the definitions of the following classes:
  - `Station`
  - `Line`
  - `Connection`

- `map.py` contains the definition `TubeMap` class, used to read the data from a JSON file (for instance: `data/london.json`).

### `main.py`

Contains a test of the full pipeline:
1. Reading the JSON file using the class `TubeMap`.
2. Computing the shortest path between two stations using `PathFinder` and printing it.
