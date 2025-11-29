from edgegraph import *


def bfs(graph: GraphEL, start: VertexEL) -> list:
    if start is None or graph is None:
        raise ValueError("Invalid graph or vertex")
    if start not in graph.vertices():
        return []
    current_level = [start]
    visited = {start}
    out = []
    while current_level:
        out.append(tuple(current_level))
        next_level = []
        for u in current_level:
            for v in graph.adjacent(u):
                if v not in visited:
                    visited.add(v)
                    next_level.append(v)
        current_level = next_level
    return out


if __name__ == "__main__":
    g = GraphEL()

    v1 = VertexEL("A")
    v2 = VertexEL("B")
    v3 = VertexEL("C")
    v4 = VertexEL("D")

    g.add_edge(EdgeEL(1, v1, v2))
    g.add_edge(EdgeEL(2, v1, v3))
    g.add_edge(EdgeEL(3, v1, v4))

    result = bfs(g, v1)
    print(result)
