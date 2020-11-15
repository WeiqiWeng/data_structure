import random

DEFAULT_SIZE = 8

class Vector(object):
    def __init__(
        self, 
        default_capacity=DEFAULT_SIZE, 
        default_element=None, 
        initial_iter=None):
        """
        Constructor

        Args:
            default_capacity (int): default initial fixed size
            default_element (object): default element in vector
            initial_iter (iterable): initial elements to initialize vector
        """  
        self._size = 0
        self._default_capacity = default_capacity
        self._capacity = default_capacity
        self._default_element = default_element
        self._elements = [default_element for _ in range(default_capacity)]

        if initial_iter is not None:
            self.copy_from(initial_iter)

    def __str__(self):
        """
        Overloads print statement
        """
        try:
            element_str = [str(e) for e in self._elements[:self._size]]
        except Exception as e:
            print(e)
            return '<Vector> object'
        
        return '[{}]'.format(','.join(element_str))

    def __getitem__(self, index):
        """
        Overloads item indexing
        
        Args:
            i (int): index
        
        Returns:
            data saved in the i-th element in vector
        """

        return self._elements[index]

    def __setitem__(self, index, value):
        """
        Overloads item indexing

        Args:
            i (int): index
            value (object): data to be saved in the i-th element in vector
        """

        self._elements[index] = value

    def copy_from(self, iter):
        """
        Copies content from given iterable

        Args:
            iter (iterable): iterable object from which contents are copied and put into vector
        """        
        self._size = 0
        self._capacity = self._default_capacity        
        self._elements = [self._default_element for _ in range(self._capacity)]
        for e in iter:
            self.append(e)

    def compare_with_iterable(self, iter):
        """
        Compares each element in vector with given iterable

        Args:
            iter (iterable): iterable object from which contents are compared with vector

        Returns:
            True if elements saved in vector are the same as those in given iterable
        """  
        comparison = True
        if self._size == len(iter):
            for x, y in zip(self._elements, iter):
                if not x == y:
                    comparison = False
                    break
        else:
            comparison = False

        return comparison

    def append(self, element):
        """
        Appends given element
        """
        # applies more space if necessary
        self.expand()
        self._elements[self._size] = element
        self._size += 1

    def put(self, i, element):
        """
        Updates element of index i

        Args:
            i (int): index
            element (object): the given element to be updated on index i
        """
        if 0 <= i < self._size:
            self._elements[i] = element
        else:
            raise IndexError('index out of range')

    def get(self, i, j=None):
        """
        Gets element of index [i, j)

        Args:
            i, j (int): index
        """
        if j is None:
            if 0 <= i < self._size:
                return self._elements[i]
            else:
                raise IndexError('index out of range')
        else:
            if 0 <= i < j <= self._size:
                return self._elements[i:j]
            else:
                raise IndexError('invalid index range')

    def size(self):
        """
        Returns vector size
        """
        return self._size

    def __len__(self):
        """
        Returns vector size
        """
        return self.size()

    def empty(self):
        """
        Returns if the vector is empty

        Returns:
            True if the vector is empty, else False
        """
        return (self._size == 0)

    def expand(self):
        """
        Doubles the fixed space if necessary
        """
        if self._size == self._capacity:
            self._elements += [self._default_element for _ in self._elements]
            self._capacity *= 2

    def unsorted(self, acending=True):
        """
        Checks if the vector is unsorted

        Args:
            acending (bool): True if checking the vector is sorted acendingly, False if checking the vector is sorted descendingly

        Returns:
            result (int): an index pointing to the first element that's not sorted, -1 if the vector is sorted
        """
        result = -1
        if self._size <= 1:
            return result

        for i in range(1, self._size):
            if acending:
                if self._elements[i - 1] > self._elements[i]:
                    result = i 
                    break
            else:
                if self._elements[i - 1] < self._elements[i]:
                    result = i                    
                    break

        return result

    def find(self, target):
        """
        Finds given target in unsorted vector

        Args:
            target (object): target object to be found in vector

        Returns:
            result (int): least index of the target object found in vector, -1 if not found
        """
        result = -1

        for i in range(self._size):
            if self._elements[i] == target:
                result = i
                break

        return result

    def search(self, target):
        """
        Finds given target in vector

        Args:
            target (object): target object to be found in vector

        Returns:
            result (int): index of target object found in vector, -1 if not found
        """
        result = -1

        if self.unsorted(True) < 0:
            result = self.binary_search_acending(target)
        elif self.unsorted(False) < 0:
            result = self.binary_search_descending(target)
        else:
            result = self.find(target)

        return result

    def binary_search_acending(self, target):
        """
        Finds given target in acending vector

        Args:
            target (object): target object to be found in vector

        Returns:
            result (int): index of target object found in vector, -1 if not found
        """        
        low, high = 0, self._size

        while low < high:
            mid = (low + high) >> 1
            if self._elements[mid] < target:
                low = mid + 1
            elif self._elements[mid] > target:
                high = mid
            else:
                return mid

        return -1

    def binary_search_descending(self, target):
        """
        Finds given target in descending vector

        Args:
            target (object): target object to be found in vector

        Returns:
            result (int): index of target object found in vector, -1 if not found
        """  
        low, high = 0, self._size

        while low < high:
            mid = (low + high) >> 1
            if self._elements[mid] > target:
                low = mid + 1
            elif self._elements[mid] < target:
                high = mid
            else:
                return mid

        return -1

    def insert(self, i, element):
        """
        Inserts element on given index

        Args:
            i (int): index
            element (object): given element to be inserted into vector                
        """
        self._size += 1
        self.expand()        

        if 0 <= i < self._size:
            for j in range(self._size - 1, i, -1):
                self._elements[j] = self._elements[j - 1]
            self._elements[i] = element
        else:
            raise IndexError('index out of range')

    def partial_permute(self, start, end):
        """
        Permutes vector segment [start, end)

        Args:
            start (int): starting index
            end (int): ending index
        """
        for i in range(end - 1, start, -1):
            temp = self._elements[i]
            swap_index = random.randint(start, i - 1)            
            self._elements[i] = self._elements[swap_index]
            self._elements[swap_index] = temp            

    def permute(self):
        """
        Permutes the entire vector
        """
        self.partial_permute(0, self._size)

    def partial_remove(self, start, end):
        """
        Removes vector segment [start, end)

        Args:
            start (int): starting index
            end (int): ending index
        """
        current_size = self._size
        if 0 <= start < end <= current_size:
            self._size = current_size - (end - start)
            for i in range(end, current_size):
                self._elements[start] = self._elements[i]                
                start += 1
        else:
            raise IndexError('starting and ending index out of valid range')

    def remove(self, i):
        """
        Removes element on index i

        Args:
            i (int): index            
        """
        self.partial_remove(i, i + 1)

    def deduplicate(self):
        """
        Deduplicates the vector
        """
        lookup = {}
        slow, fast = 0, 0

        while fast < self._size:
            fast_element = self._elements[fast]
            if not lookup.get(fast_element, False):                            
                self._elements[slow] = fast_element                
                slow += 1
                lookup[fast_element] = True

            fast += 1

        self._size = slow

    def bubblesort(self, start=None, end=None, acending=True):
        """
        Sorts the vector[start, end) through bubblesort

        Args:
            start (int): starting index
            end (int): ending index
            acending (bool): True if sorting acendingly, False if descendingly
        """
        if start is None or end is None:
            start, end = 0, self._size
        
        if 0 <= start < end <= self._size:
            unsorted = True
            while unsorted:
                unsorted = False
                for i in range(start + 1, end):
                    if self._elements[i] < self._elements[i - 1]:
                        unsorted = True
                        temp = self._elements[i]
                        self._elements[i] = self._elements[i - 1]
                        self._elements[i - 1] = temp

            if not acending:
                self._elements[start:end] = self._elements[start:end][::-1]
        else:
            raise IndexError('starting and ending index out of valid range')

    def mergesort(self, low=None, high=None, acending=True):
        """
        Sorts the vector[low, high) through mergesort

        Args:
            low (int): starting index
            high (int): ending index
            acending (bool): True if sorting acendingly, False if descendingly
        """
        if low is None or high is None:
            low, high = 0, self._size

        if high - low < 2:
            return
        
        mid = (low + high) >> 1
        self.mergesort(low, mid)
        self.mergesort(mid, high)
        self.merge(low, mid, high)

        if not acending:
            self._elements[low:high] = self._elements[low:high][::-1]

    def merge(self, low, mid, high):
        """
        Merges the sorted vector[low, mid) and vector[mid, high)

        Args:
            low (int): starting index
            high (int): ending index
            mid (int): floor((low + high) / 2)
        """
        left, right = low, mid
        temp_container = []        
        while left < mid or right < high:
            left_element = self._elements[left] if left < mid else None
            right_element = self._elements[right] if right < high else None

            if left_element is not None and right_element is not None:                
                if left_element < right_element:
                    temp_container.append(left_element)
                    left += 1
                else:
                    temp_container.append(right_element)
                    right += 1
                continue
            
            if left_element is not None:
                temp_container.append(left_element)
                left += 1
                continue

            if right_element is not None:
                temp_container.append(right_element)
                right += 1
                continue

        self._elements[low:high] = temp_container
            



    

