from data_structure import Vector


class Queue(Vector):

    def __init__(self, *args, **kwargs):
        """
        Constructor

        Args:
            same as vector
            
            default_capacity (int): default initial fixed size
            default_element (object): default element in vector
            initial_iter (iterable): initial elements to initialize vector
        """
        super(Queue, self).__init__(*args, **kwargs)

    def head(self):
        """
        Returns the top element of the queue        
        """
        return self.get(i = self._size - 1)

    def tail(self):
        """
        Returns the element on the tail of the queue        
        """
        return self.get(i = 0)

    def enqueue(self, element):
        """
        Adds given element to the tail of queue 
        """
        self.insert(0, element)

    def dequeue(self):
        """
        Pops the element at the head of the queue        
        """
        top = self.head()
        self.remove(self._size - 1)

        return top