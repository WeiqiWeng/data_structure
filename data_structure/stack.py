from data_structure import Vector

class Stack(Vector):
    
    def __init__(self, *args, **kwargs):
        """
        Constructor

        Args:
            same as vector
            
            default_capacity (int): default initial fixed size
            default_element (object): default element in vector
            initial_iter (iterable): initial elements to initialize vector
        """
        super(Stack, self).__init__(*args, **kwargs)

    def top(self):
        """
        Returns top element of the stack        
        """
        return self.get(i=self._size - 1)

    def push(self, element):
        """
        Pushes given element onto top of stack
        """
        self.append(element)

    def pop(self):
        """
        Gets top element of the stack
        """
        top = self.top()
        self.remove(self._size - 1)

        return top