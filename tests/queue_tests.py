import unittest

from data_structure import Queue


class TestQueue(unittest.TestCase):

    @classmethod
    def setUpClass(self):                
        self.initial_list = [i for i in range(5)]

    @classmethod
    def tearDownClass(self):
        print ("All tests for queue completed")

    def setUp(self):
        # print("Initializing queue")
        self.queue = Queue(8, 0, initial_iter=self.initial_list)

    def tearDown(self):
        pass

    def test_head(self):
        """
        Test getting top element        
        """
        self.assertEqual(4, self.queue.head())

    def test_tail(self):
        """
        Test getting top element        
        """
        self.assertEqual(0, self.queue.tail())

    def test_enqueue(self):
        """
        Test pushing to stack top
        """
        self.queue.enqueue(5)
        self.assertEqual(5, self.queue.tail())
        self.assertNotEqual(5, self.queue.head())
        self.assertEqual(4, self.queue.head())
        self.assertEqual(6, self.queue.size())

    def test_dequeue(self):
        """
        Test popping
        """
        for x in range(4, -1, -1):
            self.assertEqual(x, self.queue.dequeue())

        self.assertEqual(0, self.queue.size())
        


if __name__ == '__main__':

    unittest.main(verbosity=1)  