class ListNode:
    def __init__(
        self, 
        data=None, 
        precursor=None, 
        successor=None):
        """
        Constructor

        Args:
            data (object): data to be saved in node
            precursor (ListNode): precursor
            successor (ListNode): successor
        """
        self._data = data
        self._precursor = precursor
        self._successor = successor

    def data(self):
        """
        Returns data saved in node
        """
        return self._data

    def precursor(self):
        """
        Returns precursor
        """
        return self._precursor

    def successor(self):
        """
        Returns successor
        """
        return self._successor

    def insert_precursor(self, new_precursor):
        """
        Inserts given node as precursor

        Args:
            new_precursor (ListNode): given node to be inserted as precursor
        """
        new_precursor._precursor = self._precursor
        new_precursor._successor = self
        if self._precursor is not None:
            self._precursor._successor = new_precursor        
        self._precursor = new_precursor

    def insert_successor(self, new_successor):
        """
        Inserts given node as successor

        Args:
            new_successor (ListNode): given node to be inserted as successor
        """
        new_successor._successor = self._successor
        new_successor._precursor = self 
        if self._successor is not None:       
            self._successor._precursor = new_successor
        self._successor = new_successor
        

class List:
    def __init__(self, initial_iterable=None):
        """
        Constructor

        Args:
            initial_iterable (iterable): iterable object which has the data used to be saved in nodes of this list
        """
        self._head = ListNode(data=None, precursor=None, successor=None)
        self._tail = ListNode(data=None, precursor=self._head, successor=None)
        self._head._successor = self._tail        

        self._size = 0

        if initial_iterable is not None:
            self.copy_from(initial_iterable)

    def __getitem__(self, i):
        """
        Overloads item indexing

        Args:
            i (int): index
        
        Returns:
            data saved in the i-th element in list
        """
        return self.get(i).data()

    def __len__(self):
        """
        Overloads length computation

        Returns:
            length of the list
        """
        return self.size()

    def size(self):
        """
        Returns length of the list
        """
        return self._size

    def get(self, i):
        """
        Gets node through index

        Args:
            i (int): index

        Returns the i-th node in list
        """

        mid = self._size >> 1
        temp = self._head._successor

        if 0 <= i < mid:
            for _ in range(i):
                temp = temp._successor
        elif mid <= i <= self._size:
            temp = self._tail
            for _ in range(self._size - i):
                temp = temp._precursor
        else:
            raise IndexError('index out of range')

        return temp

    def serialize(self):
        """
        Serializes the list and returns elements as list

        Returns:
            elements as a list
        """        
        elements = []
        temp = self._head._successor

        while temp._successor is not None:
            elements.append(temp.data())
            temp = temp._successor            

        return elements

    def __str__(self):
        """
        Overloads print statement
        """
        try:
            element_str = [str(e) for e in self.serialize()]
        except Exception as e:
            print(e)
            return '<List> object'
        
        return '[{}]'.format(','.join(element_str))

    def __setitem__(self, i, value):
        """
        Overloads item indexing

        Args:
            i (int): index
            value (object): data to be saved in the i-th node
        """
        self.get(i)._data = value

    def copy_from(self, iterable):
        """
        Copies content from given iterable

        Args:
            iterable (iterable): iterable object from which contents are copied and put into list
        """                 
        temp = self._head
        self._size = 0

        for e in iterable:
            new_node = ListNode(data=e, precursor=temp)
            temp.insert_successor(new_node)
            temp = temp._successor
            self._size += 1

        temp._successor = self._tail
        self._tail._precursor = temp

    def insert_node_sequence(self, i, node_sequence):
        """
        Inserts a sequence of node at index i, e.g. inserting [-1,-2,-3] into [0,1,2,3] at 1 returns [0,-1,-2,-3,1,2,3]

        Args:
            i (int): index
            node_sequence (ListNode): sequence of node to be inserted in to this list
        """
        if node_sequence is None or node_sequence._precursor is not None:
            raise ValueError('first non-trivial node in sequence required')
        
        temp = self.get(i)
                
        temp._precursor._successor = node_sequence
        node_sequence._precursor = temp._precursor
        last_node = node_sequence

        node_sequence_count = 1
        while last_node._successor is not None:
            last_node = last_node._successor
            node_sequence_count += 1
        
        self._size += node_sequence_count

        last_node._successor = temp
        temp._precursor = last_node

    def remove_through_index(self, start, end=None):
        """
        Removes nodes with index [start, end)

        Args:
            start (int): starting index
            end (int): ending index
        """
        if end is None:
            end = start + 1

        if not (0 <= start < end <= self._size):
            raise IndexError('starting and ending index out of valid range')
        
        temp = self.get(start)
        last_node = temp._precursor        
        
        for _ in range(end - start):
            temp = temp._successor
            del temp._precursor
        
        last_node._successor = temp
        temp._precursor = last_node

        self._size -= (end - start)

    def remove_node(self, node):
        """
        Removes given node

        Args:
            node (ListNode): node to be removed            
        """
        if node._precursor is not None:
            node._precursor._successor = node._successor   
        if node._successor is not None:         
            node._successor._precursor = node._precursor
        
        del node        

    def deduplicate(self):
        """
        Deduplicates this list          
        """
        lookup = {}
        temp = self._head._successor

        while temp is not None:
            last_node = temp._successor
            data = temp.data()
            if lookup.get(data, False):
                self.remove_node(temp)
                self._size -= 1
            else:
                lookup[data] = True
            temp = last_node

    def uniquify(self):
        """
        Deduplicates this sorted list          
        """
        if self._size < 2:
            return

        slow = self._head._successor
        fast = slow._successor

        while fast is not None:
            if slow.data() == fast.data():                
                fast = fast._successor
                self._size -= 1
                del fast._precursor
            else:            
                slow._successor = fast
                fast._precursor = slow
                slow = slow._successor
                fast = slow._successor

    def find(self, value):
        """
        Finds the node given value

        Args:
            value (object): data to be saved in node

        Returns:
            the node with given value saved as data
        """
        temp = self._head._successor

        while temp is not None:
            if temp.data() == value:
                break
            temp = temp._successor

        return temp




    







            




            



    

        
    

    