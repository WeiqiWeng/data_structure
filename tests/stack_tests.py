import unittest

from data_structure import Stack


class TestStack(unittest.TestCase):

    @classmethod
    def setUpClass(self):                
        self.initial_list = [i for i in range(5)]

    @classmethod
    def tearDownClass(self):
        print ("All tests for stack completed")

    def setUp(self):
        # print("Initializing stack")
        self.stack = Stack(8, 0, initial_iter=self.initial_list)

    def tearDown(self):
        pass

    def test_top(self):
        """
        Test getting top element        
        """
        self.assertEqual(4, self.stack.top())

    def test_push(self):
        """
        Test pushing to stack top
        """
        self.stack.push(5)
        self.assertEqual(5, self.stack.top())

    def test_pop(self):
        """
        Test popping
        """
        self.stack.push(5)
        self.assertEqual(5, self.stack.top())
        self.assertEqual(6, len(self.stack))

        for x in range(5, -1, -1):
            self.assertEqual(x, self.stack.pop())

        self.assertEqual(0, self.stack.size())
        


if __name__ == '__main__':

    unittest.main(verbosity=1)  