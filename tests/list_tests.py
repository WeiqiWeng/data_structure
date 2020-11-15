import unittest
import sys
sys.path.append('../')
from data_structure import List, ListNode

class TestList(unittest.TestCase):

    @classmethod
    def setUpClass(self):                
        self.initial_list = [i for i in range(5)]
        self.another_list = [1,2,4,1,1,3,1,3,3,1,1,3,4]
        self.random_list = [1,5,6,6,6,7,10,10,10,29,31,31]

    @classmethod
    def tearDownClass(self):
        print ("All tests for list completed")

    def setUp(self):
        # print("Initializing list")
        self.list = List(initial_iterable=self.initial_list)

    def tearDown(self):
        pass

    def build_testing_node_sequence(self):
        node_1 = ListNode(-2)
        node_0 = ListNode(-1)
        node_2 = ListNode(-3)
        node_1.insert_precursor(node_0)
        node_1.insert_successor(node_2)

        return node_0 
    
    def test_constructor(self):
        """Test constructor"""
        self.assertEqual(self.initial_list, self.list.serialize())
        self.assertEqual(5, self.list.size())
        self.list.copy_from(self.another_list)
        self.assertEqual(13, self.list.size())
        self.assertNotEqual(self.initial_list, self.list.serialize())

    def test_copy_from(self):
        """Test copying from iterable"""
        self.list.copy_from(self.random_list)        
        self.assertEqual(self.random_list, self.list.serialize())

    def test_get(self):
        """Test get"""
        self.assertEqual(True, isinstance(self.list.get(2), ListNode))
        self.assertEqual(2, self.list.get(2)._data)

    def test_indexing(self):
        """Test indexing"""
        for i in range(5):        
            self.assertEqual(i, self.list[i])

    def test_set(self):
        """Test setting"""
        self.list[0] = -1        
        self.assertEqual(-1, self.list[0])
        self.list[4] = -2
        self.assertEqual(-2, self.list[4])

    def test_insertion(self):
        """Test insertion"""
        self.list.insert_node_sequence(2, self.build_testing_node_sequence())        
        self.assertEqual([0,1,-1,-2,-3,2,3,4], self.list.serialize())
        self.list.copy_from(self.initial_list)        
        self.list.insert_node_sequence(0, self.build_testing_node_sequence())                
        self.assertEqual([-1,-2,-3,0,1,2,3,4], self.list.serialize())
        self.list.copy_from(self.initial_list)
        self.list.insert_node_sequence(4, self.build_testing_node_sequence())
        self.assertEqual([0,1,2,3,-1,-2,-3,4], self.list.serialize())
        self.list.copy_from(self.initial_list)
        self.list.insert_node_sequence(5, self.build_testing_node_sequence())
        self.assertEqual([0,1,2,3,4,-1,-2,-3], self.list.serialize())
        self.assertEqual(8, self.list.size())

    def test_remove(self):
        """Test removing"""
        self.list.remove_through_index(0)
        self.assertEqual([1,2,3,4], self.list.serialize())
        self.list.remove_through_index(2)
        self.assertEqual([1,2,4], self.list.serialize())
        self.list.remove_through_index(2)
        self.assertEqual([1,2], self.list.serialize())
        self.list.insert_node_sequence(2, self.build_testing_node_sequence())        
        self.list.remove_through_index(2, 4)
        self.assertEqual([1,2,-3], self.list.serialize())
        self.list.insert_node_sequence(3, self.build_testing_node_sequence())
        self.list.remove_through_index(0, 4)
        self.assertEqual([-2,-3], self.list.serialize())
        self.list.insert_node_sequence(0, self.build_testing_node_sequence())
        # [-1,-2,-3,-2,-3]
        self.list.remove_through_index(2, 5)
        self.assertEqual([-1,-2], self.list.serialize())

    def test_remove_node(self):
        """Test remove a node"""
        test_node = self.build_testing_node_sequence()        
        node_1 = test_node.successor()
        self.list.remove_node(node_1)
        self.assertEqual(-1, test_node.data())
        self.assertEqual(-3, test_node.successor().data())

        test_node = self.build_testing_node_sequence()        
        node_1 = test_node.successor()
        self.list.remove_node(test_node)
        self.assertEqual(-2, node_1.data())
        self.assertEqual(None, node_1.precursor())
        self.assertEqual(-3, node_1.successor().data())

        test_node = self.build_testing_node_sequence()        
        node_2 = test_node.successor().successor()
        self.list.remove_node(node_2)
        self.assertEqual(-1, test_node.data())        
        self.assertEqual(-2, test_node.successor().data())
        self.assertEqual(None, test_node.successor().successor())

    def test_deduplicate(self):
        """Test deduplication"""
        self.list.copy_from(self.another_list)
        self.list.deduplicate()
        self.assertEqual(4, len(self.list))
        self.assertEqual([1,2,4,3], self.list.serialize())

        self.list.copy_from(self.initial_list)
        self.list.deduplicate()
        self.assertEqual(5, len(self.list))
        self.assertEqual([0,1,2,3,4], self.list.serialize())

    def test_uniquify(self):
        """Test deduplication of a sorted list"""
        self.list.copy_from(self.random_list)
        self.list.uniquify()
        self.assertEqual(7, len(self.list))
        self.assertEqual([1,5,6,7,10,29,31], self.list.serialize())

        self.list.copy_from(self.random_list)
        self.list.remove_through_index(len(self.list) - 1)
        self.list.uniquify()
        self.assertEqual(7, len(self.list))
        self.assertEqual([1,5,6,7,10,29,31], self.list.serialize())

    def test_find(self):
        """Test finding an element"""
        self.assertEqual(0, self.list.find(0).data())
        self.assertEqual(4, self.list.find(4).data())
        self.assertEqual(3, self.list.find(3).data())
        self.assertEqual(None, self.list.find(-1))

if __name__ == '__main__':

    unittest.main(verbosity=1)        
        