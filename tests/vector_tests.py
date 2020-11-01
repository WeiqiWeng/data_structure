import unittest

from data_structure import Vector

class TestVector(unittest.TestCase):

    @classmethod
    def setUpClass(self):                
        self.initial_list = [i for i in range(5)]
        self.another_list = [i for i in range(-1, -6, -1)]
        self.random_list = [5,1,4,2,3]

    @classmethod
    def tearDownClass(self):
        print ("All tests completed")

    def setUp(self):
        # print("Initializing vector")
        self.vector = Vector(8, 0, initial_iter=self.initial_list)

    def tearDown(self):
        pass
    
    def test_constructor(self):
        """Test constructor"""
        self.assertEqual(True, self.vector.compare_with_iterable(self.initial_list))
        self.assertNotEqual(True, self.vector.compare_with_iterable(self.another_list))

    def test_copy_from(self):
        """Test copying from iterable"""
        self.vector.copy_from(self.another_list)        
        self.assertEqual(True, self.vector.compare_with_iterable(self.another_list))

    def test_append(self):
        """Test appending element to vector"""                        
        self.vector.append(5)
        self.assertEqual(5, self.vector.get(5))
        self.assertEqual(8, self.vector._capacity) 
        self.vector.append(6)
        self.assertEqual(6, self.vector.get(6))
        self.assertEqual(8, self.vector._capacity)
        self.vector.append(7)        
        self.assertEqual(7, self.vector.get(7))
        self.assertEqual(8, self.vector._capacity)
        self.vector.append(8)        
        self.assertEqual(8, self.vector.get(8))
        self.assertEqual(16, self.vector._capacity)

    def test_put(self):
        """Test put opteration"""
        self.vector.put(0, 10)                
        self.assertEqual(10, self.vector.get(0))
        self.vector.put(1, 11)        
        self.assertEqual(11, self.vector.get(1))
        self.vector.put(4, 14)        
        self.assertEqual(14, self.vector.get(4))

    def test_get(self):
        """Test get opteration"""                        
        self.assertEqual(0, self.vector.get(0))             
        self.assertEqual(1, self.vector.get(1))        
        self.assertEqual(4, self.vector.get(4))
        self.assertEqual(self.initial_list[0:5], self.vector.get(0, 5))
        self.assertEqual(self.initial_list[0:1], self.vector.get(0, 1))
        self.assertEqual(self.initial_list[2:4], self.vector.get(2, 4))
    
    def test_size(self):
        """Test get opteration"""                        
        self.assertEqual(5, self.vector.size())             
        self.vector.append(5)
        self.vector.append(6)
        self.assertEqual(7, self.vector.size())

    def test_empty(self):
        """Test if the vector is empty"""                        
        self.assertEqual(False, self.vector.empty())
        self.vector.copy_from([])
        self.assertEqual(True, self.vector.empty())   

    def test_unsorted(self):
        """Test if the vector is unsorted"""                        
        self.assertEqual(-1, self.vector.unsorted(acending=True))
        self.assertEqual(1, self.vector.unsorted(acending=False))
        self.vector.put(3, 2)
        self.assertEqual(-1, self.vector.unsorted(acending=True))
        self.vector.put(3, -1)
        self.assertEqual(3, self.vector.unsorted(acending=True))
        self.vector.copy_from([5,4,3,2,1])
        self.assertEqual(-1, self.vector.unsorted(acending=False))
        self.assertEqual(1, self.vector.unsorted(acending=True))
        self.vector.put(3, 3)          
        self.assertEqual(-1, self.vector.unsorted(acending=False))
        self.vector.put(3, 5)
        self.assertEqual(3, self.vector.unsorted(acending=False))

    def test_search(self):
        """Test searching element from vector"""                        
        self.assertEqual(4, self.vector.get(self.vector.search(4)))
        self.assertEqual(2, self.vector.get(self.vector.search(2)))
        self.assertEqual(-1, self.vector.search(5))
        self.vector.copy_from(self.another_list)
        self.assertEqual(-4, self.vector.get(self.vector.search(-4)))
        self.assertEqual(-1, self.vector.get(self.vector.search(-1)))
        self.vector.copy_from(self.random_list)
        self.assertEqual(5, self.vector.get(self.vector.search(5)))
        self.assertEqual(3, self.vector.get(self.vector.search(3)))

    def test_insert(self):
        """Test inserting element into vector"""
        self.vector.insert(0, -1)                        
        self.assertEqual(-1, self.vector.get(0))
        self.assertEqual(6, self.vector.size())
        self.vector.insert(6, 5)
        self.assertEqual(5, self.vector.get(6))
        self.assertEqual(7, self.vector.size())
        self.assertEqual(True, self.vector.compare_with_iterable(range(-1, 6, 1)))

    def test_permute(self):
        """Test permutation"""                               
        self.vector.partial_permute(1, 2)
        self.assertEqual(True, self.vector.compare_with_iterable(self.initial_list))
        self.vector.partial_permute(1, 4) 
        self.assertNotEqual([1,2,3], set(self.vector.get(1, 4)))
        self.assertEqual(set([1,2,3]), set(self.vector.get(1, 4)))
        self.vector.permute()
        self.assertEqual(set(self.initial_list), set(self.vector.get(0, self.vector.size())))
        self.assertNotEqual(self.initial_list, set(self.vector.get(0, self.vector.size())))

    def test_remove(self):
        """Test removing element from vector"""                               
        self.vector.partial_remove(1, 2)        
        self.assertEqual(4, self.vector.size())
        self.assertEqual([0,2,3,4], self.vector.get(0, self.vector.size()))
        self.vector.partial_remove(1, 3) 
        self.assertEqual(2, self.vector.size())
        self.assertEqual([0,4], self.vector.get(0, self.vector.size()))
        self.vector.remove(1) 
        self.assertEqual(1, self.vector.size())
        self.assertEqual([0], self.vector.get(0, self.vector.size()))

    def test_deduplicate(self):
        """Test deduplicate vector"""                               
        self.vector.deduplicate()        
        self.assertEqual(5, self.vector.size())
        self.assertEqual([0,1,2,3,4], self.vector.get(0, self.vector.size()))
        self.vector.insert(5, 4) 
        self.assertEqual(6, self.vector.size())
        self.vector.deduplicate()
        self.assertEqual([0,1,2,3,4], self.vector.get(0, self.vector.size()))
        self.vector.insert(5, 4)
        self.vector.insert(2, 2)
        self.vector.deduplicate()
        self.assertEqual([0,1,2,3,4], self.vector.get(0, self.vector.size()))

    def test_bubblesort(self):
        self.vector.copy_from(self.random_list)
        self.vector.bubblesort(acending=True)
        self.assertEqual([1,2,3,4,5], self.vector.get(0, self.vector.size()))
        self.vector.bubblesort(acending=False)
        self.assertEqual([5,4,3,2,1], self.vector.get(0, self.vector.size()))

        self.vector.copy_from(self.random_list)
        self.vector.bubblesort(start=1, end=4, acending=True)
        self.assertEqual([5,1,2,4,3], self.vector.get(0, self.vector.size()))
        self.vector.bubblesort(start=1, end=4, acending=False)
        self.assertEqual([5,4,2,1,3], self.vector.get(0, self.vector.size()))

    def test_mergesort(self):
        self.vector.copy_from(self.random_list)
        self.vector.mergesort(acending=True)
        self.assertEqual([1,2,3,4,5], self.vector.get(0, self.vector.size()))
        self.vector.mergesort(acending=False)
        self.assertEqual([5,4,3,2,1], self.vector.get(0, self.vector.size()))

        self.vector.copy_from(self.random_list)
        self.vector.mergesort(low=1, high=4, acending=True)
        self.assertEqual([5,1,2,4,3], self.vector.get(0, self.vector.size()))
        self.vector.mergesort(low=1, high=4, acending=False)
        self.assertEqual([5,4,2,1,3], self.vector.get(0, self.vector.size()))


if __name__ == '__main__':

    unittest.main(verbosity=1)        
        