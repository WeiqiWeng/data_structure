import unittest

from data_structure import TreeNode, BinaryTree

class TestBinaryTree(unittest.TestCase):

    @classmethod
    def setUpClass(self):                
        self.initial_list = [i for i in range(5)]

    @classmethod
    def tearDownClass(self):
        print("All tests for binary tree completed")

    def _generate_binary_tree(self):
        
        binary_tree = BinaryTree()
        binary_tree.deserialize([0,1,2,None,4,None,6,7])
        
        return binary_tree

    def _generate_full_binary_tree(self):
        """
        Generates a 3-level full binary tree
        """
        full_binary_tree = BinaryTree()
        full_binary_tree.deserialize([0,1,2,3,4,5,6])
        
        return full_binary_tree

    def _generate_left_tree(self):
        """
        Generates a binary tree with each node having only left child

        called left tree for simplicity
        """
        left_tree = BinaryTree()
        left_tree.deserialize([0,1,None,2,None,3])

        return left_tree

    def _generate_right_tree(self):
        """
        Generates a binary tree with each node having only right child
        
        called right tree for simplicity
        """
        right_tree = BinaryTree()
        right_tree.deserialize([0,None,1,None,2,None,3])

        return right_tree

    def setUp(self):
        # print("Initializing binary tree")
        self.full_binary_tree = self._generate_full_binary_tree()
        self.binary_tree = self._generate_binary_tree()  
        self.left_tree = self._generate_left_tree()
        self.right_tree = self._generate_right_tree()      
        self.empty_tree = BinaryTree()

    def tearDown(self):
        pass

    def test_serialize(self):
        """
        Tests tree serialization
        """
        self.assertEqual([0,1,2,None,4,None,6,7], self.binary_tree.serialize())
        self.assertEqual([0,1,None,2,None,3], self.left_tree.serialize())
        self.assertEqual([0,None,1,None,2,None,3], self.right_tree.serialize())
        self.assertEqual([0,1,2,3,4,5,6], self.full_binary_tree.serialize())
        self.assertEqual([], self.empty_tree.serialize())

    def test_deserialize(self):
        """
        Tests tree deserialization
        """
        self.assertEqual([0,1,2,None,4,None,6,7], self.binary_tree.deserialize([0,1,2,None,4,None,6,7]).serialize())
        self.assertEqual([0,1,None,2,None,3], self.left_tree.deserialize([0,1,None,2,None,3]).serialize())
        self.assertEqual([0,None,1,None,2,None,3], self.right_tree.deserialize([0,None,1,None,2,None,3]).serialize())
        self.assertEqual([0,1,2,3,4,5,6], self.full_binary_tree.deserialize([0,1,2,3,4,5,6]).serialize())
        self.assertEqual([], self.empty_tree.deserialize([]).serialize())

    def test_copy_from_iterable(self):
        """
        Tests tree construction
        """

        # full binary tree
        self.assertEqual(7, self.full_binary_tree.size())
        self.assertEqual(2, self.full_binary_tree.depth())
        self.assertEqual(True, self.full_binary_tree.is_full_binary_tree())        
        self.assertEqual([
            [(0, 2, 0)], 
            [(1, 1, 1), (2, 1, 1)], 
            [(3, 0, 2), (4, 0, 2), (5, 0, 2), (6, 0, 2)]], self.full_binary_tree._level_order_traversal())
        self.assertEqual(False, self.full_binary_tree.empty())

        # binary tree
        self.assertEqual(6, self.binary_tree.size())
        self.assertEqual(3, self.binary_tree.depth())
        self.assertEqual(False, self.binary_tree.is_full_binary_tree())
        self.assertEqual([
            [(0, 3, 0)], 
            [(1, 2, 1), (2, 2, 1)], 
            [(4, 1, 2), (6, 1, 2)], 
            [(7, 0, 3)]], self.binary_tree._level_order_traversal())

        # empty tree
        self.assertEqual(True, self.empty_tree.empty())

        # left tree
        self.assertEqual(4, self.left_tree.size())
        self.assertEqual(3, self.left_tree.depth())
        self.assertEqual([
            [(0, 3, 0)], 
            [(1, 2, 1)], 
            [(2, 1, 2)], 
            [(3, 0, 3)]], self.left_tree._level_order_traversal())

        # right tree
        self.assertEqual(4, self.right_tree.size())
        self.assertEqual(3, self.right_tree.depth())
        self.assertEqual([
            [(0, 3, 0)], 
            [(1, 2, 1)],  
            [(2, 1, 2)], 
            [(3, 0, 3)]], self.right_tree._level_order_traversal())

    def test_insert_root(self):
        """
        Tests inserting new root node
        """

        new_root = TreeNode(-1, 0)
        self.binary_tree.insert_root(new_root)

        self.assertEqual(7, self.binary_tree.size())
        self.assertEqual(4, self.binary_tree.depth())
        self.assertEqual(-1, self.binary_tree.root().data())

        self.assertEqual([
            [(-1, 4, 0)],
            [(0, 3, 1)],      
            [(1, 2, 2), (2, 2, 2)],
            [(4, 1, 3), (6, 1, 3)],
            [(7, 0, 4)]], self.binary_tree._level_order_traversal())
            
    def test_insert_left_subtree(self):
        """
        Tests inserting a left subtree to the binary tree
        """

        # inerts full binary tree below the left child node of root as left child
        subtree_root = self.binary_tree.root().left_child()
        self.binary_tree.insert_left_subtree(subtree_root, self.full_binary_tree)

        self.assertEqual(13, self.binary_tree.size())
        self.assertEqual(4, self.binary_tree.depth())
        self.assertEqual([
            [(0, 4, 0)],
            [(1, 3, 1), (2, 3, 1)],      
            [(0, 2, 2), (4, 2, 2), (6, 2, 2)], 
            [(1, 1, 3), (2, 1, 3), (7, 1, 3)],
            [(3, 0, 4), (4, 0, 4), (5, 0, 4), (6, 0, 4)]], self.binary_tree._level_order_traversal())

        # inerts full binary tree below root as left child
        self.binary_tree = self._generate_binary_tree()
        subtree_root = self.binary_tree.root()
        full_binary_tree = self._generate_full_binary_tree()
        self.binary_tree.insert_left_subtree(subtree_root, full_binary_tree)

        self.assertEqual(10, self.binary_tree.size())
        self.assertEqual(3, self.binary_tree.depth())
        self.assertEqual([
            [(0, 3, 0)],
            [(0, 2, 1), (2, 2, 1)],      
            [(1, 1, 2), (2, 1, 2), (6, 1, 2)], 
            [(3, 0, 3), (4, 0, 3), (5, 0, 3), (6, 0, 3)]], self.binary_tree._level_order_traversal())

    def test_insert_right_subtree(self):
        """
        Tests inserting a right subtree to the binary tree
        """

        # inerts full binary tree below the left child node of root as left child
        subtree_root = self.binary_tree.root().left_child()
        self.binary_tree.insert_right_subtree(subtree_root, self.full_binary_tree)

        self.assertEqual(11, self.binary_tree.size())
        self.assertEqual(4, self.binary_tree.depth())
        
        self.assertEqual([
            [(0, 4, 0)],
            [(1, 3, 1), (2, 3, 1)],      
            [(0, 2, 2), (6, 2, 2)],
            [(1, 1, 3), (2, 1, 3)],
            [(3, 0, 4), (4, 0, 4), (5, 0, 4), (6, 0, 4)]], self.binary_tree._level_order_traversal())

        self.binary_tree = self._generate_binary_tree()
        subtree_root = self.binary_tree.root()
        full_binary_tree = self._generate_full_binary_tree()
        self.binary_tree.insert_right_subtree(subtree_root, full_binary_tree)
        self.assertEqual([
            [(0, 3, 0)],
            [(1, 2, 1), (0, 2, 1)],      
            [(4, 1, 2), (1, 1, 2), (2, 1, 2)], 
            [(7, 0, 3), (3, 0, 3), (4, 0, 3), (5, 0, 3), (6, 0, 3)]], self.binary_tree._level_order_traversal())

        self.assertEqual(11, self.binary_tree.size())
        self.assertEqual(3, self.binary_tree.depth())
        self.assertEqual(3, self.binary_tree.root().height())
        
    def test_remove_subtree(self):
        """
        Tests removing subtree
        """
        self.full_binary_tree.remove_subtree(self.full_binary_tree.root().left_child())

        self.assertEqual(4, self.full_binary_tree.size())
        self.assertEqual(2, self.full_binary_tree.depth())
        self.assertEqual([
            [(0, 2, 0)],
            [(2, 1, 1)],      
            [(5, 0, 2), (6, 0, 2)]], self.full_binary_tree._level_order_traversal())

        self.binary_tree.remove_subtree(self.binary_tree.root().right_child())

        self.assertEqual(4, self.binary_tree.size())
        self.assertEqual(3, self.binary_tree.depth())
        self.assertEqual(0, self.binary_tree.root().data())
        self.assertEqual(1, self.binary_tree.root().left_child().data())
        self.assertEqual(2, self.binary_tree.root().left_child().height())
        self.assertEqual(4, self.binary_tree.root().left_child().right_child().data())
        self.assertEqual(1, self.binary_tree.root().left_child().right_child().height())
        self.assertEqual(7, self.binary_tree.root().left_child().right_child().left_child().data())
        self.assertEqual(0, self.binary_tree.root().left_child().right_child().left_child().height())

        self.binary_tree.remove_subtree(self.binary_tree.root())
        self.assertEqual(0, self.binary_tree.size())
        self.assertEqual(0, self.binary_tree.depth())
        self.assertEqual(None, self.binary_tree.root())

    def test_split_subtree(self):
        """
        Tests splitting subtree
        """
        subtree_root = self.binary_tree.split_subtree(self.binary_tree.root().left_child())
        subtree = BinaryTree(subtree_root)

        self.assertEqual(3, subtree.size())
        self.assertEqual(2, subtree.depth())
        self.assertEqual([
            [(1, 2, 0)],
            [(4, 1, 1)],      
            [(7, 0, 2)]], subtree._level_order_traversal())

        self.assertEqual(3, self.binary_tree.size())
        self.assertEqual(2, self.binary_tree.depth())
        self.assertEqual(2, self.binary_tree.root().height())
        self.assertEqual([
            [(0, 2, 0)],
            [(2, 1, 1)],      
            [(6, 0, 2)]], self.binary_tree._level_order_traversal())

    def test_preorder_traversal(self):
        """
        Tests pre-order traversal
        """
        self.assertEqual([0,1,4,7,2,6], self.binary_tree.preorder_traversal())
        self.assertEqual([0,1,3,4,2,5,6], self.full_binary_tree.preorder_traversal())
        self.assertEqual([], self.empty_tree.preorder_traversal())

    def test_inorder_traversal(self):
        """
        Tests in-order traversal
        """
        self.assertEqual([1,7,4,0,2,6], self.binary_tree.inorder_traversal())
        self.assertEqual([3,1,4,0,5,2,6], self.full_binary_tree.inorder_traversal())
        self.assertEqual([], self.empty_tree.inorder_traversal())

    def test_postorder_traversal(self):
        """
        Tests post-order traversal
        """
        self.assertEqual([7,4,1,6,2,0], self.binary_tree.postorder_traversal())
        self.assertEqual([3,4,1,5,6,2,0], self.full_binary_tree.postorder_traversal())
        self.assertEqual([], self.empty_tree.postorder_traversal())

    def test_level_order_traversal(self):
        """
        Tests level order traversal
        """
        self.assertEqual([
            [(0, 3, 0)], 
            [(1, 2, 1), (2, 2, 1)], 
            [(4, 1, 2), (6, 1, 2)], 
            [(7, 0, 3)]], self.binary_tree.level_order_traversal())
        self.assertEqual([
            [(0, 2, 0)], 
            [(1, 1, 1), (2, 1, 1)], 
            [(3, 0, 2), (4, 0, 2), (5, 0, 2), (6, 0, 2)]], self.full_binary_tree._level_order_traversal())
        self.assertEqual([], self.empty_tree.level_order_traversal())

        self.assertEqual([0,1,2,4,6,7], self.binary_tree.level_order_traversal(flatten=True))
        self.assertEqual([0,1,2,3,4,5,6], self.full_binary_tree.level_order_traversal(flatten=True))
        self.assertEqual([], self.empty_tree.level_order_traversal(flatten=True)) 