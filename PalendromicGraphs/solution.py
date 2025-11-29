from edgegraph import *
from collections import Counter


def pld_graph(g: GraphEL) -> list:
    if g is None:
        raise ValueError("Bad graph")

    edges = g.edges()
    if not edges:
        return []

    value_counts = Counter(edge.get_value() for edge in edges)
    palindromic_paths = set()

    def _is_palindrome(values):
        if len(values) >= 3 and values == values[::-1]:
            palindromic_paths.add(tuple(values))

    def _dfs(current_vertex, current_path, used_edges, unique_index):
        _is_palindrome(current_path)

        for edge in g.incident(current_vertex):
            if edge in used_edges:
                continue

            next_vertex = edge.head() if edge.tail() == current_vertex else edge.tail()

            used_edges.add(edge)
            current_path.append(edge.get_value())

            new_unique_index = unique_index
            if new_unique_index is None and value_counts[current_path[-1]] == 1:
                new_unique_index = len(current_path) - 1

            should_continue = True
            if new_unique_index is not None:
                max_len = 2 * new_unique_index + 1
                if len(current_path) > max_len:
                    should_continue = False

            if should_continue:
                _dfs(next_vertex, current_path, used_edges, new_unique_index)

            current_path.pop()
            used_edges.remove(edge)

    for edge in edges:
        edge_value = edge.get_value()
        initial_unique_index = 0 if value_counts[edge_value] == 1 else None

        for start_vertex, next_vertex in (
            (edge.tail(), edge.head()),
            (edge.head(), edge.tail()),
        ):
            used = {edge}
            path = [edge_value]
            _dfs(next_vertex, path, used, initial_unique_index)

    return list(palindromic_paths)
