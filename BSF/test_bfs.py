import unittest
from edgegraph import GraphEL, VertexEL, EdgeEL
from cursor import bfs


class TestBFS(unittest.TestCase):
    """Test suite for BFS function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.graph = GraphEL()
    
    def test_single_vertex(self):
        """Test BFS with a graph containing only one vertex"""
        v1 = VertexEL("A")
        self.graph.add_vertex(v1)
        
        result = bfs(self.graph, v1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
    
    def test_linear_graph(self):
        """Test BFS on a linear graph: A-B-C"""
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        
        e1 = EdgeEL(1, v1, v2)
        e2 = EdgeEL(2, v2, v3)
        
        self.graph.add_edge(e1)
        self.graph.add_edge(e2)
        
        result = bfs(self.graph, v1)
        
        # Should have 3 levels
        self.assertEqual(len(result), 3)
        # Level 0: A
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
        # Level 1: B
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1][0], v2)
        # Level 2: C
        self.assertEqual(len(result[2]), 1)
        self.assertEqual(result[2][0], v3)
    
    def test_simple_graph_multiple_adjacent(self):
        """Test BFS on a graph where one vertex has multiple neighbors"""
        # Graph: A-B, A-C, A-D (A connected to B, C, D)
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        v4 = VertexEL("D")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v1, v3))
        self.graph.add_edge(EdgeEL(3, v1, v4))
        
        result = bfs(self.graph, v1)
        
        # Should have 2 levels: A, then B,C,D
        self.assertEqual(len(result), 2)
        # Level 0: A
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
        # Level 1: B, C, D (order may vary)
        self.assertEqual(len(result[1]), 3)
        self.assertIn(v2, result[1])
        self.assertIn(v3, result[1])
        self.assertIn(v4, result[1])
    
    def test_tree_structure(self):
        """Test BFS on a tree structure"""
        # Tree:     A
        #          / \
        #         B   C
        #        / \   \
        #       D   E   F
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        v4 = VertexEL("D")
        v5 = VertexEL("E")
        v6 = VertexEL("F")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v1, v3))
        self.graph.add_edge(EdgeEL(3, v2, v4))
        self.graph.add_edge(EdgeEL(4, v2, v5))
        self.graph.add_edge(EdgeEL(5, v3, v6))
        
        result = bfs(self.graph, v1)
        
        # Should have 3 levels
        self.assertEqual(len(result), 3)
        # Level 0: A
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
        # Level 1: B, C
        self.assertEqual(len(result[1]), 2)
        self.assertIn(v2, result[1])
        self.assertIn(v3, result[1])
        # Level 2: D, E, F
        self.assertEqual(len(result[2]), 3)
        self.assertIn(v4, result[2])
        self.assertIn(v5, result[2])
        self.assertIn(v6, result[2])
    
    def test_graph_with_cycle(self):
        """Test BFS on a graph with a cycle"""
        # Triangle: A-B, B-C, C-A
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v2, v3))
        self.graph.add_edge(EdgeEL(3, v3, v1))
        
        result = bfs(self.graph, v1)
        
        # Should have 2 levels (cycle should not cause infinite loop)
        # Level 0: A
        # Level 1: B and C (both are neighbors of A)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
        # Level 1: B and C (both at same distance from A)
        self.assertEqual(len(result[1]), 2)
        self.assertIn(v2, result[1])
        self.assertIn(v3, result[1])
        # Check all vertices are present
        all_vertices = set()
        for level in result:
            for v in level:
                all_vertices.add(v)
        self.assertEqual(all_vertices, {v1, v2, v3})
    
    def test_disconnected_components(self):
        """Test BFS returns only reachable vertices from disconnected components"""
        # Two disconnected components: A-B and C-D
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        v4 = VertexEL("D")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v3, v4))
        
        result = bfs(self.graph, v1)
        
        # Should only return A and B (reachable from A)
        self.assertEqual(len(result), 2)
        all_vertices = set()
        for level in result:
            for v in level:
                all_vertices.add(v)
        self.assertEqual(all_vertices, {v1, v2})
        self.assertNotIn(v3, all_vertices)
        self.assertNotIn(v4, all_vertices)
    
    def test_bfs_from_different_start(self):
        """Test BFS starting from a different vertex in the same graph"""
        # Graph: A-B-C
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v2, v3))
        
        # Start from middle vertex
        result = bfs(self.graph, v2)
        
        # Should have 2 levels: B, then A and C
        self.assertEqual(len(result), 2)
        # Level 0: B
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v2)
        # Level 1: A, C
        self.assertEqual(len(result[1]), 2)
        self.assertIn(v1, result[1])
        self.assertIn(v3, result[1])
    
    def test_complex_graph(self):
        """Test BFS on a more complex graph structure"""
        # Graph:
        #    A - B - D
        #    |   |
        #    C   E
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        v4 = VertexEL("D")
        v5 = VertexEL("E")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v1, v3))
        self.graph.add_edge(EdgeEL(3, v2, v4))
        self.graph.add_edge(EdgeEL(4, v2, v5))
        
        result = bfs(self.graph, v1)
        
        # Should have 3 levels
        self.assertEqual(len(result), 3)
        # Level 0: A
        self.assertEqual(result[0][0], v1)
        # Level 1: B, C
        self.assertEqual(len(result[1]), 2)
        self.assertIn(v2, result[1])
        self.assertIn(v3, result[1])
        # Level 2: D, E
        self.assertEqual(len(result[2]), 2)
        self.assertIn(v4, result[2])
        self.assertIn(v5, result[2])
    
    def test_empty_graph(self):
        """Test BFS on an empty graph with a vertex that exists"""
        v1 = VertexEL("A")
        self.graph.add_vertex(v1)
        
        result = bfs(self.graph, v1)
        
        # Should return just the start vertex
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], v1)
    
    def test_result_is_list_of_tuples(self):
        """Test that the result is correctly formatted as list of tuples"""
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        
        self.graph.add_edge(EdgeEL(1, v1, v2))
        
        result = bfs(self.graph, v1)
        
        # Check type
        self.assertIsInstance(result, list)
        for level in result:
            self.assertIsInstance(level, tuple)
            for vertex in level:
                self.assertIsInstance(vertex, VertexEL)
    
    def test_all_vertices_visited_once(self):
        """Test that all reachable vertices are visited exactly once"""
        # Create a graph with multiple paths
        v1 = VertexEL("A")
        v2 = VertexEL("B")
        v3 = VertexEL("C")
        v4 = VertexEL("D")
        
        # A-B, A-C, B-D, C-D (D reachable via two paths)
        self.graph.add_edge(EdgeEL(1, v1, v2))
        self.graph.add_edge(EdgeEL(2, v1, v3))
        self.graph.add_edge(EdgeEL(3, v2, v4))
        self.graph.add_edge(EdgeEL(4, v3, v4))
        
        result = bfs(self.graph, v1)
        
        # Collect all vertices
        all_vertices = []
        for level in result:
            all_vertices.extend(level)
        
        # Should have exactly 4 unique vertices
        self.assertEqual(len(set(all_vertices)), 4)
        self.assertEqual(len(all_vertices), 4)  # No duplicates
        self.assertEqual(set(all_vertices), {v1, v2, v3, v4})


if __name__ == '__main__':
    unittest.main()

