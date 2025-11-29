import unittest

from edgegraph import EdgeEL, GraphEL, VertexEL
from cursor import pld_graph


def build_graph(edge_specs):
    """
    Utility helper to construct a GraphEL from iterable of
    (edge_name, tail_name, head_name, value) tuples.
    """

    graph = GraphEL()
    vertices = {}

    def get_vertex(name):
        if name not in vertices:
            vertices[name] = VertexEL(name)
            graph.add_vertex(vertices[name])
        return vertices[name]

    for edge_name, tail_name, head_name, value in edge_specs:
        tail = get_vertex(tail_name)
        head = get_vertex(head_name)
        edge = EdgeEL(edge_name, tail, head)
        edge.set_value(value)
        graph.add_edge(edge)

    return graph


class TestPalindromicGraph(unittest.TestCase):
    def assertPalindromesEqual(self, actual, expected):
        actual_set = {tuple(p) for p in actual}
        expected_set = {tuple(p) for p in expected}
        self.assertEqual(actual_set, expected_set)

    def test_none_graph_raises(self):
        with self.assertRaises(ValueError):
            pld_graph(None)

    def test_empty_graph_has_no_palindromes(self):
        graph = GraphEL()
        self.assertEqual(pld_graph(graph), [])

    def test_single_palindrome_path(self):
        graph = build_graph(
            [
                ("e1", "A", "B", 1),
                ("e2", "B", "C", 2),
                ("e3", "C", "D", 1),
            ]
        )
        self.assertPalindromesEqual(pld_graph(graph), {(1, 2, 1)})

    def test_multiple_palindromes_on_same_path(self):
        # Path values along the perimeter: 1-0-1-0-1
        graph = build_graph(
            [
                ("e1", "A", "B", 1),
                ("e2", "B", "C", 0),
                ("e3", "C", "D", 1),
                ("e4", "D", "E", 0),
                ("e5", "E", "F", 1),
            ]
        )
        expected = {(1, 0, 1), (0, 1, 0), (1, 0, 1, 0, 1)}
        self.assertPalindromesEqual(pld_graph(graph), expected)

    def test_duplicate_paths_only_counted_once(self):
        # Two distinct ways to generate values [5, 6, 5]
        graph = build_graph(
            [
                ("e1", "A", "B", 5),
                ("e2", "B", "C", 6),
                ("e3", "C", "D", 5),
                ("e4", "A", "E", 5),  # alternate branch to B
                ("e5", "E", "B", 6),
            ]
        )
        expected = {(5, 6, 5), (5, 6, 6, 5), (6, 5, 5, 6)}
        self.assertPalindromesEqual(pld_graph(graph), expected)

    def test_forest_with_and_without_palindromes(self):
        graph = build_graph(
            [
                ("t1", "T1", "T2", 3),
                ("t2", "T2", "T3", 4),
                ("t3", "T3", "T4", 3),
                # second component has no palindrome
                ("s1", "S1", "S2", 8),
                ("s2", "S2", "S3", 9),
            ]
        )
        expected = {(3, 4, 3)}
        self.assertPalindromesEqual(pld_graph(graph), expected)

    def test_unique_value_middle_truncates_search(self):
        # The unique value 9 must be the center; ensure longer non-palindromes are ignored.
        graph = build_graph(
            [
                ("u1", "U1", "U2", 7),
                ("u2", "U2", "U3", 9),  # unique value
                ("u3", "U3", "U4", 7),
                ("u4", "U4", "U5", 5),
            ]
        )
        expected = {(7, 9, 7)}
        self.assertPalindromesEqual(pld_graph(graph), expected)


if __name__ == "__main__":
    unittest.main()

