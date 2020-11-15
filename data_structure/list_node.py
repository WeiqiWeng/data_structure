class ListNode(object):
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