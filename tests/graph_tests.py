import unittest

import numpy as np

from data_structure import Graph, GraphNode, GraphEdge


class TestGraph(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 0 ---> 1               7
        # | \                    |\
        # |  \                   | \
        # |   \                  |  \
        # |    \                 |   \
        # v     v                v    v
        # 2     3 --> 4          8 --> 9
        # |\        ^
        # | \     /
        # |  \   /
        # |   \ /
        # v    v 
        # 6    5

        adjacency_matrix = np.array(
            [[0, 0.5, 1, 2, 0,   0, 0, 0, 0,   0], 
             [0, 0,   0, 0, 0,   0, 0, 0, 0,   0], 
             [0, 0,   0, 0, 0,   2, 1, 0, 0,   0], 
             [0, 0,   0, 0, 0.4, 0, 0, 0, 0,   0], 
             [0, 0,   0, 0, 0,   0, 0, 0, 0,   0], 
             [0, 0,   0, 0, 2.5, 0, 0, 0, 0,   0], 
             [0, 0,   0, 0, 0,   0, 0, 0, 0,   0],
             [0, 0,   0, 0, 0,   0, 0, 0, 1.5, 2],
             [0, 0,   0, 0, 0,   0, 0, 0, 0,   0.5],
             [0, 0,   0, 0, 0,   0, 0, 0, 0,   0]])

        self.directed_graph_nodes = [GraphNode(data=i * 2) for i in range(10)]
        
        directed_graph_edges = []
        for i in range(10):
            for j in range(10):
                if adjacency_matrix[i, j]:
                    directed_graph_edges.append(GraphEdge(start=i, end=j, weight=adjacency_matrix[i, j]))

        self.directed_graph_edges = directed_graph_edges

    @classmethod
    def tearDownClass(self):
        print ("All tests for graph completed")

    def setUp(self):
        # print("Initializing graph")
        self.directed_graph = Graph(node_set=self.directed_graph_nodes, edge_set=self.directed_graph_edges)

    def tearDown(self):
        pass

    def test_depth_first_search(self):
        """
        docstring
        """
        self.assertEqual([[0, 1, 2, 5, 4, 6, 3], [7, 8, 9]], self.directed_graph.depth_first_traversal())
        
        for i in range(10):
            self.assertEqual(i*2, self.directed_graph.depth_first_search(target_data=i*2).data)
        
        self.assertEqual(None, self.directed_graph.depth_first_search(target_data=7))

    def test_breadth_first_search(self):
        """
        docstring
        """
        self.assertEqual([[0, 1, 2, 3, 5, 6, 4], [7, 8, 9]], self.directed_graph.breadth_first_traversal())
        
        for i in range(10):
            self.assertEqual(i*2, self.directed_graph.breadth_first_search(target_data=i*2).data)
        
        self.assertEqual(None, self.directed_graph.breadth_first_search(target_data=7))

    def test_topological_sort(self):
        """
        docstring
        """
        adjacency_matrix = np.array(
            [[0, 0, 1, 1, 0, 0], 
             [0, 0, 1, 0, 0, 0], 
             [0, 0, 0, 1, 1, 1], 
             [0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 1], 
             [0, 0, 0, 0, 0, 0]])

        directed_graph_nodes = [GraphNode(data=i * 2) for i in range(6)]
        
        directed_graph_edges = []
        for i in range(6):
            for j in range(6):
                if adjacency_matrix[i, j]:
                    directed_graph_edges.append(GraphEdge(start=i, end=j, weight=adjacency_matrix[i, j]))

        directed_graph = Graph(node_set=directed_graph_nodes, edge_set=directed_graph_edges)
        self.assertEqual([[0,2,4,5,3], [1]], directed_graph.topological_sort())
        self.assertEqual([[0,1,2,5,4,6,3], [7,8,9]], self.directed_graph.topological_sort())
        