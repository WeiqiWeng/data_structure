from collections import namedtuple

import numpy as np

GraphNode = namedtuple('GraphNode', ['data'])
GraphEdge = namedtuple('GraphEdge', ['start', 'end', 'weight'])

ERROR_TOLERANCE = 1e-8
UNDISCOVERED = 1
DISCOVERED = 2
VISITED = -1
DUMMY_START_NODE_INDEX = -1


def queue_pop(candidates):
    """
    docstring
    """
    return candidates.pop()

def queue_concat(accessible_nodes, candidates):
    """
    docstring
    """
    # candidates already in container go first: FIFO
    return accessible_nodes[::-1] + candidates

def stack_pop(candidates):
    """
    docstring
    """
    return candidates.pop()

def stack_concat(accessible_nodes, candidates):
    """
    docstring
    """
    # candidates just pushed in container go first
    return candidates + accessible_nodes[::-1]

def get_linked_nodes(
    next_node, 
    adjacency_matrix, 
    node_status, 
    candidate_index_range, 
    previous_node_tracking):
    
    accessible_nodes = adjacency_matrix[next_node] * node_status
    accessible_nodes = candidate_index_range[accessible_nodes > 0]
    node_status[accessible_nodes] = DISCOVERED
    accessible_nodes_indexes = []

    for node in accessible_nodes:
        parent_node_recorded = previous_node_tracking.get(node, None)
        if parent_node_recorded is not None:
            if parent_node_recorded == next_node:
                raise ValueError('Cyclic loop found')
            else:
                continue
        else:
            previous_node_tracking[node] = next_node
            accessible_nodes_indexes.append(node)

    return accessible_nodes_indexes


class Graph(object):
    
    def __init__(self, node_set, edge_set):

        self._node_set = node_set

        self._node_set_size = len(node_set)
        self._adjacency_matrix = self.get_adjacency_matrix(edge_set)
        self._directed = self.check_symmetric(self._adjacency_matrix)
        self._edge_set_size = self.get_edge_set_size(self._adjacency_matrix)

    def get_adjacency_matrix(self, edge_set):
        """
        docstring
        """
        adjacency_matrix = np.zeros((self._node_set_size, self._node_set_size))

        for edge in edge_set:
            adjacency_matrix[edge.start, edge.end] = edge.weight

        return adjacency_matrix

    def check_symmetric(self, matrix):
        """
        docstring
        """
        return np.allclose(matrix, matrix.T, atol=ERROR_TOLERANCE)

    def get_edge_set_size(self, matrix):
        """
        docstring
        """
        edge_count = np.sum(self._adjacency_matrix > 0)

        if not self._directed:
            edge_count //= 2
        
        return edge_count

    def indegree(self, node_index):
        """
        docstring
        """
        return np.sum(self._adjacency_matrix[:, node_index] > 0)

    def outdegree(self, node_index):
        """
        docstring
        """
        return np.sum(self._adjacency_matrix[node_index, :] > 0)

    def is_leaf(self, node_index):
        """
        docstring
        """
        return self.outdegree(node_index) == 0 and self.indegree(node_index) > 0

    def is_isolated(self, node_index):
        """
        docstring
        """
        return self.indegree(node_index) + self.outdegree(node_index) == 0

    def priority_first_path(
        self, 
        starting_node_index, 
        node_status, 
        get_next_candidate, 
        concat_candidates, 
        get_accessible_nodes_indexes):
        """
        docstring
        """
        path = [DUMMY_START_NODE_INDEX]
        # parent node in graph structure
        candidates = [starting_node_index]
        candidate_index_range = np.arange(self._node_set_size)
        # 1: undiscovered 2: discovered -1: visited
        if node_status is None:
            node_status = UNDISCOVERED * np.ones(self._node_set_size, dtype=np.int8)
        node_status[starting_node_index] = DISCOVERED
        # tracks the previous node before one node gets visited
        previous_node_tracking = {starting_node_index: -1}

        while candidates:
            next_node = get_next_candidate(candidates)

            if node_status[next_node] != VISITED:
                path.append(next_node)
                node_status[next_node] = VISITED
                
                accessible_nodes_indexes = get_accessible_nodes_indexes(
                    next_node, self._adjacency_matrix, node_status, candidate_index_range, previous_node_tracking)
            
                candidates = concat_candidates(accessible_nodes_indexes, candidates)
            else:
                raise ValueError('Cyclic loop found')
        
        return path[1:], node_status

    def priority_first_traversal(
        self, 
        get_next_candidate, 
        concat_candidates):
        """
        docstring
        """
        
        paths = []
        # accessible = np.ones(self._node_set_size, dtype=np.int8)
        accessible_count = self._node_set_size
        node_status = UNDISCOVERED * np.ones(self._node_set_size, dtype=np.int8)

        last_starting_node_index = 0

        while accessible_count:

            starting_node_index = -1
            for i in range(last_starting_node_index, self._node_set_size):
                if node_status[i] != VISITED:
                    starting_node_index = i
                    break
            
            if starting_node_index < 0:
                break
                
            last_starting_node_index = starting_node_index

            # if self.is_leaf(starting_node_index):
            #     paths.append([starting_node_index])
            #     accessible[starting_node_index] = 0
            #     accessible_count -= 1
            #     continue
            
            try:
                path, node_status = self.priority_first_path(
                    starting_node_index, 
                    node_status, 
                    get_next_candidate, 
                    concat_candidates, 
                    get_linked_nodes)
                accessible_count -= len(path)
            except Exception as e:
                print(e)
                return None

            paths.append(path)

        return paths

    def depth_first_traversal(self):
        """
        docstring
        """
        return self.priority_first_traversal(stack_pop, stack_concat)

    def breadth_first_traversal(self):
        """
        docstring
        """
        return self.priority_first_traversal(queue_pop, queue_concat)

    def depth_first_search(self, target_data):
        """
        docstring
        """
        node = None
        paths = self.depth_first_traversal()

        for path in paths:
            for current_node in path:
                if self._node_set[current_node].data == target_data:
                    return self._node_set[current_node]

        return node

    def breadth_first_search(self, target_data):
        """
        docstring
        """
        node = None
        paths = self.breadth_first_traversal()

        for path in paths:
            for current_node in path:
                if self._node_set[current_node].data == target_data:
                    return self._node_set[current_node]

        return node

    def topological_sort(self):
        """
        docstring
        """
        node_status = UNDISCOVERED * np.ones(self._node_set_size, dtype=np.int8)
        candidate_index_range = np.arange(self._node_set_size)
        zero_indegree_nodes = candidate_index_range[np.sum(self._adjacency_matrix, axis=0) == 0]
        topological_order = []

        for starting_node in zero_indegree_nodes:
            if node_status[starting_node] != VISITED:
                path, node_status = self.priority_first_path(
                    starting_node, 
                    node_status, 
                    queue_pop, 
                    queue_concat, 
                    get_linked_nodes)
                topological_order.append(path)

        return topological_order
            

        
            



