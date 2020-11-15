class TreeNode(object):

    def __init__(
        self, 
        data,        
        node_type,
        parent=None,
        left_child=None, 
        right_child=None):
        """
        Constructor

        Args:
            data (object): data object to be saved in node
            node_type (int): 0 -- root node, 1 -- parent node's left child, -1 -- parent node's right child
            parent (TreeNode): parent node
            left_child (TreeNode): left child tree node
            right_child (TreeNode): right child tree node
        """

        self._data = data
        self._parent = parent
        self._left_child = left_child
        self._right_child = right_child

        # update size/height/depth if any child node is given
        # size: number of descendant nodes plus the node itself
        self._size = 1
        self.update_size()

        # height of node counted starting from lowest leaf
        # lowest leaf has height of 0
        self._height = 0
        # depth of node counted starting from the root
        # the root has depth of 0
        self._depth = 0

        self._node_type = node_type
        if self.is_root():
            self._node_type = 0
            self.update_height_from_child()
        else:
            self.update_depth()

    def update_height_from_child(self):
        """
        Updates current node height based on child node height

        Returns:
            new_height (int): updated height of current node
        """
        left_child, right_child = self.left_child(), self.right_child()

        left_child_height = -1
        if left_child is not None:
            left_child_height = left_child.height()            
        
        right_child_height = -1
        if right_child is not None:
            right_child_height = right_child.height()            

        new_height = max(left_child_height, right_child_height) + 1
        self._height = new_height

        return new_height

    def update_height_from_parent(self):
        """
        Updates current node height based on parent node height

        Returns:
            new_height (int): updated height of current node
        """
        new_height = self.parent().height() - 1
        self._height = new_height

        return new_height

    def update_depth(self):
        """
        Updates current node depth based on parent node
        """
        parent = self.parent()

        if parent is not None:
            self._depth = parent.depth() + 1
        else:
            self._depth = 0

    def update_size(self):
        """
        Updates current node size
        """
        left_child, right_child = self.left_child(), self.right_child()

        left_child_size = 0
        if left_child is not None:
            left_child_size = left_child.size()            
        
        right_child_size = 0
        if right_child is not None:
            right_child_size = right_child.size()

        self._size = left_child_size + right_child_size + 1           

    def size(self):
        """
        Returns size
        """
        return self._size

    def data(self):
        """
        Returns data
        """
        return self._data

    def height(self):
        """
        Returns height
        """
        return self._height

    def depth(self):
        """
        Returns depth
        """
        return self._depth

    def left_child(self):
        """
        Returns left child
        """
        return self._left_child

    def right_child(self):
        """
        Returns right child
        """
        return self._right_child

    def parent(self):
        """
        Returns parent node
        """
        return self._parent

    def node_type(self):
        """
        Returns node type
        """
        return self._node_type

    def is_root(self):
        """
        Returns if the node is root
        """
        return self.node_type() == 0

    def is_left_child(self):
        """
        Returns if the node is a left child
        """
        return self.node_type() == 1

    def is_right_child(self):
        """
        Returns if the node is a right child
        """
        return self.node_type() == -1

    def has_left_child(self):
        """
        Returns if the node has a left child
        """
        return self.left_child() is not None

    def has_right_child(self):
        """
        Returns if the node has a right child
        """
        return self.right_child() is not None

    def has_child(self):
        """
        Returns if the node has any child node
        """
        return self.has_left_child() or self.has_right_child()

    def has_both_child(self):
        """
        Returns if the node has both left and right child nodes
        """
        return self.has_left_child() and self.has_right_child()

    def is_leaf(self):
        """
        Returns if the node is a leaf
        """
        return not self.has_child()

    def get_sibling(self):
        """
        Returns sibling of current node

        Returns:
            sibling (TreeNode): sibling node
        """
        sibling = None
        if not self.is_root():
            if self.is_left_child():
                sibling = self.parent().right_child()
            if self.is_right_child():
                sibling = self.parent().left_child()

        return sibling

    def update_descendant_depth(self):
        """
        Updates depth of each desendant node
        """
        stack = []

        # starting from child of the current node
        if self.has_left_child():
            stack.append(self.left_child())
        if self.has_right_child():
            stack.append(self.right_child())

        while len(stack):
            node = stack.pop()
            # update depth of current node
            node.update_depth()

            # update depth of left child node
            child_node = node.left_child()
            if child_node:
                stack.append(child_node)
            
            # update depth of right child node
            child_node = node.right_child()
            if child_node:
                stack.append(child_node)

    def get_root(self, starting_node):
        """
        Returns root node

        Args:
            starting_node (TreeNode): starting node to go up and get root

        Returns:
            root (TreeNode): root node
        """
        root = starting_node
        while root.parent() is not None:
            root = root.parent()
        
        return root

    def update_descendant_height(self):
        """
        Updates height of each descendant node
        """
        queue = []

        # start with child nodes of current node
        if self.has_left_child():
            queue.append(self.left_child())            
        if self.has_right_child():
            queue.append(self.right_child())

        while len(queue):
            node = queue.pop()

            node_current_height = node.height()  
            # self._height is updated in method update_height_from_parent
            new_height = node.update_height_from_parent()

            if new_height != node_current_height:
                # if height needs updating
                # append child nodes and no need to reverse
                if node.has_left_child():
                    queue.append(node.left_child())            
                if node.has_right_child():
                    queue.append(node.right_child())
            else:
                # if height remains
                # no need to update descendant height
                node._height = node_current_height
                break

    def update_ancestor_height(self):
        """
        Updates height of each ancestor node
        """
        queue = []

        sibling = self.get_sibling()
        
        if sibling is not None:
            # update height of the sibling node
            sibling._height = self.height()
            # update descendant node height of the sibling node
            sibling.update_descendant_height()

        if not self.is_root():
            queue.append(self.parent())

        updating_height = True
        while updating_height:
            node = queue.pop()

            node_current_height = node.height()            
            new_height = node.update_height_from_child()

            if new_height != node_current_height:
                # if height needs updating
                sibling = node.get_sibling()
                if sibling is not None:
                    # also update sibling node height
                    sibling._height = new_height
                    # and update descendant node height of the sibling node
                    sibling.update_descendant_height()
                updating_height = False
                # go up one layer
                if not node.is_root():
                    queue.append(node.parent())
                    updating_height = True
            else:
                # if height remains
                # no need to update ancestor height
                node._height = node_current_height
                break

    def update_ancestor_size(self):
        """
        Updates size of each ancestor node
        """
        queue = []

        # start from parent of current node
        if not self.is_root():
            queue.append(self.parent())

        while len(queue):
            node = queue.pop()
            # nodes in queue are all above the current node            
            node.update_size()
        
            if not node.is_root():
                queue.append(node.parent())

    def insert_left_child(self, new_left_child):
        """
        Inserts given node as left child to current node

        Args:
            new_left_child (TreeNode): given tree node to be inserted as left child
        """

        # set node type
        new_left_child._node_type = 1
        
        # clear the left child of current node
        if self.has_left_child():
            self.left_child().clear_descendant()
            del self._left_child
            self._left_child = None
        
        # set left child and update size/depth/height
        self._left_child = new_left_child
        self.update_size()
        self.update_ancestor_size()
        # point to current node as parent node for the new left child
        self._left_child._parent = self
        self._left_child.update_depth()
        self._left_child.update_descendant_depth()
        self._left_child.update_ancestor_height()

    def insert_right_child(self, new_right_child):
        """
        Inserts given node as right child to current node

        Args:
            new_right_child (TreeNode): given tree node to be inserted as right child
        """

        # set node type
        new_right_child._node_type = -1

        # clear the right child of current node
        if self.has_right_child():
            self.right_child().clear_descendant()
            del self._right_child
            self._right_child = None
        
        # set left child and update size/depth/height
        self._right_child = new_right_child
        self.update_size() 
        self.update_ancestor_size()

        self._right_child._parent = self
        self._right_child.update_depth()
        self._right_child.update_descendant_depth()
        self._right_child.update_ancestor_height()

    def clear_descendant(self):
        """
        Removes every descendant node of current node
        """

        # leverage a list to simulate behavior of a stack
        # technically descendants are removed in a depth-first manner
        stack = []

        self._size = 1
        self._height = 0

        # start from child node of current node
        if self.has_left_child():
            stack.append(self.left_child())            
        if self.has_right_child():
            stack.append(self.right_child())

        while len(stack):
            node = stack.pop()            

            if node.has_left_child():
                stack.append(node.left_child())
            if node.has_right_child():
                stack.append(node.right_child())
            # remove the node
            del node

       

      
        

