import time
import heapq
from heuristics import heuristic_value
from successors import successors
from board import goal

class Node:
    __slots__ = ("id","parent","state","action","cost","depth","heuristic","value")
    def __init__(self, node_id, parent, state, action, cost, depth, heuristic, value):
        self.id = node_id
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
        self.depth = depth
        self.heuristic = heuristic
        self.value = value

    def path(self):
        n = self
        camino = []
        while n is not None:
            camino.append(n)
            n = n.parent
        camino.reverse()
        return camino

    def __str__(self):
        pid = "none" if self.parent is None else self.parent.id
        return f"[{self.id},{pid},{self.action},{self.state},{self.cost},{self.depth},{self.heuristic},{self.value}]"


class Frontier:
    """
    Misma política de desempate: primero por value ascendente y, a igualdad,
    por id ascendente. Con heapq garantizamos mismo orden de extracción.
    """
    def __init__(self):
        self._heap = []

    def is_empty(self):
        return not self._heap

    def add(self, node):
        heapq.heappush(self._heap, (node.value, node.id, node))

    def pop(self):
        return heapq.heappop(self._heap)[2]


def search(level, strategy, max_depth=None, heuristic_id=0):
    # Asegura alias exacto como antes
    if strategy == "ASTAR":
        strategy = "AStar"
    else:
        strategy = strategy.upper() if strategy not in ("AStar",) else strategy

    next_id = 0
    TN = EN = CN = DF = 0
    t0 = time.perf_counter()

    # Cache local de heurística para evitar recomputaciones
    h_cache = {}

    def h(state):
        key = (state, heuristic_id)
        v = h_cache.get(key)
        if v is None:
            v = heuristic_value(state, heuristic_id)
            h_cache[key] = v
        return v

    if strategy in ("GBF", "AStar"):
        h0 = h(level)
        v0 = h0 if strategy == "GBF" else (0 + h0)
        root = Node(next_id, None, level, "___", 0, 0, h0, v0)
    else:
        root = Node(next_id, None, level, "___", 0, 0, 0, 0)

    next_id += 1
    TN += 1

    frontier = Frontier()
    frontier.add(root)

    use_depth_map = strategy in ("BFS", "DFS", "UCS")
    visit_depth = {} if use_depth_map else None
    visit_set = set() if not use_depth_map else None

    solution = None

    while not frontier.is_empty():
        node = frontier.pop()

        if goal(node.state):
            solution = node
            break

        if strategy == "DFS" and max_depth is not None and node.depth == max_depth:
            CN += 1
            continue

        if use_depth_map:
            prev = visit_depth.get(node.state)
            if prev is not None and prev <= node.depth:
                CN += 1
                continue
            visit_depth[node.state] = node.depth
        else:
            if node.state in visit_set:
                CN += 1
                continue
            visit_set.add(node.state)

        EN += 1

        # Misma ordenación determinista por acción
        children = successors(node.state)
        children.sort(key=lambda x: x[0])

        for acc, est, _ in children:
            depth = node.depth + 1

            node_id = next_id
            next_id += 1
            TN += 1

            pasos = int(acc[2:])
            real_cost = 6 - pasos
            new_cost = node.cost + real_cost

            if depth > DF:
                DF = depth

            if strategy == "BFS":
                val = depth
                heur_val = 0
            elif strategy == "DFS":
                val = -depth
                heur_val = 0
            elif strategy == "UCS":
                val = new_cost
                heur_val = 0
            elif strategy == "GBF":
                heur_val = h(est)
                val = heur_val
            else:  # AStar
                heur_val = h(est)
                val = new_cost + heur_val

            new_node = Node(node_id, node, est, acc, new_cost, depth, heur_val, val)
            frontier.add(new_node)

    t1 = time.perf_counter()
    ET = int((t1 - t0) * 1_000_000)

    path = solution.path() if solution else []
    stats = {"ET": ET, "TN": TN, "EN": EN, "CN": CN, "DF": DF}
    return path, stats


def solver(level, strategy, depth=None, show_stats=False, heuristic_id=0):
    # Se mantiene exactamente la misma API/prints
    md = depth if (strategy.upper() == "DFS" or strategy == "AStar" and depth is not None) else depth
    camino, stats = search(level, strategy, depth if strategy.upper() == "DFS" else None, heuristic_id)

    for n in camino:
        print(n)

    if show_stats:
        print(f"TN: {stats['TN']}")
        print(f"EN: {stats['EN']}")
        print(f"CN: {stats['CN']}")
        print(f"DF: {stats['DF']}")
