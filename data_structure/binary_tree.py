from data_structure import TreeNode, Queue, Stack


class BinaryTree(object):
    
    def __init__(self, root=None):
        """
        Constructor

        Args:
            root (TreeNode): root node
        """
        self._root = root

        self._depth, self._size = 0, 0

        if root is not None:
            # if non-trival root node is given
            # maintain tree depth and size
            self._depth = root.height()
            self._size = root.size()

    def size(self):
        """
        Returns size
        """
        return self._size

    def depth(self):
        """
        Returns depth
        """
        return self._depth

    def deserialize(self, iterable):
        
        iterable_size = len(iterable)
        if iterable_size <= 0:
            self._root = None
            self._depth, self._size = 0, 0
            return self
        
        self._root = TreeNode(iterable[0], 0)
        queue = Queue()
        queue.enqueue(self._root)        
        i = 1
        while not queue.empty():
            node = queue.dequeue()
            if i < iterable_size:
                if iterable[i] is not None:
                    left_child = TreeNode(iterable[i], 1)
                    node.insert_left_child(left_child)
                    queue.enqueue(left_child)
                i += 1
                if i < iterable_size and iterable[i] is not None:
                    right_child = TreeNode(iterable[i], -1)
                    node.insert_right_child(right_child)
                    queue.enqueue(right_child)
                i += 1

        self._depth = self._root.height()
        self._size = self._root.size()

        return self

    def serialize(self):

        queue = Queue()
        queue.enqueue(self._root)
        iterable = []

        while not queue.empty():
            queue_size = queue.size()
            for _ in range(queue_size):
                node = queue.dequeue()
                if node is not None:
                    iterable.append(node.data())
                    queue.enqueue(node.left_child())
                    queue.enqueue(node.right_child())
                else:
                    iterable.append(None)

        while iterable and iterable[-1] is None:
            iterable.pop()
        
        return iterable

    def copy_from_iterable(self, iterable):
        """
        Copies data from iterable, which are put into the binary tree in level order

        Args:
            iterable (iterable): iterable object from which contents are copied and put into binary tree

        Returns:
            root node of the binary tree
        """

        # initialize root node
        self._root = TreeNode(iterable[0], 0)
        iterable_size = len(iterable)

        # create a list of tree nodes with each saving data from iterable
        # but topoligical relation has not been established yet
        # note that nodes saved in iterable are mapped to binary tree node in level order
        node_queue = [self._root]
        for i, data in enumerate(iterable[1:]):
            inserting_right = i & 1
            node_queue.append(TreeNode(data, -1 if inserting_right else 1) if data else None)

        i = 1
        while i < iterable_size:
            
            current_node = node_queue[i]
            
            if current_node is not None:
                # inserting_left == 1 when inserting a left child node
                # inserting_left == 0 when inserting a right child node
                inserting_left = i & 1
                # if a tree node has an indice i (0-indexed) in list, the parent node indice will be (i + 1) // 2 - 1 (0-indexed)
                current_parent_node = node_queue[(i + 1) // 2 - 1]        
                if inserting_left:
                    current_parent_node.insert_left_child(current_node)                    
                else:
                    current_parent_node.insert_right_child(current_node)
                
            i += 1

        self._depth = self._root.height()
        self._size = self._root.size()

        return self._root

    def is_full_binary_tree(self):
        """
        Returns if the binary tree is a full binary tree
        """
        return self._size == 2 ** (self._depth + 1) - 1

    def root(self):
        """
        Returns root node of the binary tree
        """
        return self._root

    def empty(self):
        """
        Returns if the binary tree is empty
        """
        return self._size == 0

    def insert_root(self, new_root):
        """
        Inserts a new root node to the binary tree

        Args:
            new_root (TreeNode): new root node to be inserted
        """

        # check if the given new root node is valid
        if new_root.is_root():
            # if given new root node already has left(right) child,
            # insert the binary tree as right(left) child
            if not new_root.has_left_child():
                new_root.insert_left_child(self.root())
            elif not new_root.has_right_child():
                new_root.insert_right_child(self.root())
            else:
                raise ValueError('the given root node has child node')
            
        # update root, size and depth
        self._root = new_root
        self._size = new_root.size()
        self._depth = new_root.height()
        
    def insert_left_subtree(self, left_subtree_root, left_subtree):
        """
        Inserts given binary tree (including it's root) to given tree node as left child

        Args:
            left_subtree_root (TreeNode): insert given binary tree to this tree node
            left_subtree (BinaryTree): insert this binary tree to given tree node as left child
        """

        left_subtree_root.insert_left_child(left_subtree.root())

        self._size = self._root.size()
        self._depth = self._root.height()

    def insert_right_subtree(self, right_subtree_root, right_subtree):
        """
        Inserts given binary tree (including it's root) to given tree node as right child

        Args:
            right_subtree_root (TreeNode): insert given binary tree to this tree node
            right_subtree (BinaryTree): insert this binary tree to given tree node as right child
        """

        right_subtree_root.insert_right_child(right_subtree.root())

        self._size = self._root.size()
        self._depth = self._root.height()

    def get_lowest_leaf(self, starting_node=None):
        """
        Gets lowest leaf node below given starting node

        If starting node is given, it's equivalent to fetch the lowest leaf in subtree rooted at starting node. 

        Args:
            starting_node (TreeNode): the tree node below which the lowest leaf is retrieved
        """

        # default to root node
        if starting_node is None:
            starting_node = self._root

        lowest_leaf = starting_node
        stack = [starting_node]

        while len(stack):
            node = stack.pop()

            # if a lower node is found, update the lowest leaf
            if node.height() < lowest_leaf.height():
                lowest_leaf = node

            if node.has_left_child():
                stack.append(node.left_child())
            if node.has_right_child():
                stack.append(node.right_child())
        
        return lowest_leaf

    def remove_subtree(self, subtree_root):
        """
        Removes subtree from current binary tree

        Args:
            subtree_root (TreeNode): root node of subtree to be removed
        """

        # remove all descendant nodes below the subtree root node
        subtree_root.clear_descendant()
        # get the parent node of subtree root in original binary tree
        subtree_root_parent = subtree_root.parent()

        if subtree_root_parent is None:
            self.__init__(root=None)
            return

        # reset the child node of the parent node of subtree root
        if subtree_root.is_left_child():
            subtree_root_parent._left_child = None
        else:
            subtree_root_parent._right_child = None
        # release memory
        del subtree_root

        # since the structure changes for the subtree rooted at subtree_root_parent, 
        # update height/size of each node in this specific subtree
        lowest_leaf = self.get_lowest_leaf(subtree_root_parent)
        lowest_leaf.update_height_from_child()
        lowest_leaf.update_ancestor_height()

        subtree_root_parent.update_size()
        subtree_root_parent.update_ancestor_size()
        
        self._size = self._root.size()
        self._depth = self._root.height()

    def split_subtree(self, subtree_root):
        """
        Splits the subtree rooted at given node from the binary tree

        Args:
            subtree_root (TreeNode): root node of subtree to be splitted
        """

        # remove all descendant nodes below the subtree root node
        new_leaf_node = subtree_root.parent()
        # make subtree_root a root node
        subtree_root._parent = None

        # reset the child node of the parent node of subtree root
        if subtree_root.is_left_child():
            new_leaf_node._left_child = None
        else:
            new_leaf_node._right_child = None
        
        new_leaf_node.update_size()
        new_leaf_node.update_ancestor_size()

        # update the tree left after the split
        lowest_leaf = self.get_lowest_leaf(new_leaf_node)
        lowest_leaf.update_height_from_child()
        lowest_leaf.update_ancestor_height()

        self._size = self._root.size()
        self._depth = self._root.height()
        
        # update depth/height of each node in splitted subtree
        subtree_root._node_type = 0
        subtree_root.update_depth()
        subtree_root.update_descendant_depth()

        lowest_leaf = self.get_lowest_leaf(subtree_root)
        lowest_leaf.update_height_from_child()
        lowest_leaf.update_ancestor_height()

        return subtree_root

    def preorder_traversal(self, starting_node=None):
        """
        Traverse the binary tree in pre-order: parent node -> left child -> right child

        Args:
            starting_node (TreeNode): traverse the subtree rooted at given starting node

        Returns:
            data_array (list): list of data saved in binary tree
        """
        data_array = []

        if starting_node is None:
            starting_node = self._root

        stack = Stack()
        current_node = starting_node

        while True:

            while current_node is not None:
                data_array.append(current_node.data())
                # push right child node into stack if it exists                
                stack.push(current_node.right_child())
                # always go along left child
                current_node = current_node.left_child()
            
            if stack.empty():
                break

            current_node = stack.pop()

        return data_array

    def inorder_traversal(self, starting_node=None):
        """
        Traverse the binary tree in in-order: left child -> parent node -> right child

        Args:
            starting_node (TreeNode): traverse the subtree rooted at given starting node

        Returns:
            data_array (list): list of data saved in binary tree
        """
        data_array = []

        if starting_node is None:
            starting_node = self._root

        stack = Stack()
        current_node = starting_node

        while True:

            while current_node is not None:                
                stack.push(current_node)
                # always go along left child
                current_node = current_node.left_child()
            
            if stack.empty():
                break
            
            current_node = stack.pop()
            data_array.append(current_node.data())
            current_node = current_node.right_child()

        return data_array

    def _to_highest_leftmost_leaf(self, node_stack):
        """
        Goes to the highest leftmost leaf node visible from left while adding node on path to given stack

        Args:
            node_stack (Stack): containing nodes traveled when going to the highest leftmost leaf node visible from left
        """
        top_node = node_stack.top()

        while top_node is not None:
            # in order to get leftmost leaf, always check left subtree first
            if top_node.has_left_child():
                if top_node.has_right_child():
                    node_stack.push(top_node.right_child())
                node_stack.push(top_node.left_child())
            else:
                # only if no left subtree available
                node_stack.push(top_node.right_child())
            top_node = node_stack.top()

        node_stack.pop()

    def postorder_traversal(self, starting_node=None):
        """
        Traverses the binary tree in post-order: left child -> right child -> parent node

        Args:
            starting_node (TreeNode): traverse the subtree rooted at given starting node

        Returns:
            data_array (list): list of data saved in binary tree
        """
        data_array = []

        if self._root is None:
            return data_array

        if starting_node is None:
            starting_node = self._root

        stack = Stack()        
        current_node = starting_node
        stack.push(current_node)

        while not stack.empty():
            top_node = stack.top()
            if top_node != current_node.parent():
                self._to_highest_leftmost_leaf(stack)
            current_node = stack.pop()
            data_array.append(current_node.data())

        return data_array

    def _level_order_traversal(self, starting_node=None):

        data_array = []

        # returns empty list if the binary tree is empty
        if self._root is None:
            return data_array

        # traverse from root if starting node is not given
        if starting_node is None:
            starting_node = self._root

        queue = Queue()
        queue.enqueue(starting_node)
        
        while not queue.empty():
            queue_size = queue.size()
            data_same_level = []
            for _ in range(queue_size):
                node = queue.dequeue()
                data_same_level.append((node.data(), node.height(), node.depth()))
                if node.has_left_child():
                    queue.enqueue(node.left_child())
                if node.has_right_child():
                    queue.enqueue(node.right_child())
            data_array.append(data_same_level)

        return data_array

    # def _level_order_traversal(self, starting_node=None, include_none=True):
    #     """
    #     Traverses the binary tree from top level to bottom and saves data/height/depth for testing purpose

    #     Args:
    #         starting_node (TreeNode): traverse the subtree rooted at given starting node
    #         include_none (bool): True if including None node in binary tree

    #     Returns:
    #         data_array ([3-tuple]): [(data saved in node, height, depth)]
    #     """
    #     data_array = []

    #     # returns empty list if the binary tree is empty
    #     if self._root is None:
    #         return data_array

    #     # traverse from root if starting node is not given
    #     if starting_node is None:
    #         starting_node = self._root

    #     queue = Queue()
    #     # (data, height, depth, left child, right child)
    #     queue.enqueue(
    #         (starting_node.data(), 
    #          starting_node.height(),
    #          starting_node.depth(),
    #          starting_node.left_child(), 
    #          starting_node.right_child()))

    #     while not queue.empty():
    #         top_node = queue.dequeue()
            
    #         if top_node[0] is not None:
    #             # if it's a non-trival node, append data/height/depth
    #             data_array.append((top_node[0], top_node[1], top_node[2]))                        
    #         else:
    #             data_array.append(None)

    #         # if the node is not on the deepest level, left and right child can be added into queue and visited soon
    #         if top_node[2] < self.depth():
    #                 top_node_left_child, top_node_right_child = top_node[3], top_node[4]
                    
    #                 entry = [None, top_node[1] - 1, top_node[2] + 1, None, None]
    #                 if top_node_left_child is not None:
    #                     entry[0] = top_node_left_child.data()
    #                     entry[3] = top_node_left_child.left_child()
    #                     entry[4] = top_node_left_child.right_child()
    #                 queue.enqueue(tuple(entry))
                    
    #                 entry = [None, top_node[1] - 1, top_node[2] + 1, None, None]
    #                 if top_node_right_child is not None:
    #                     entry[0] = top_node_right_child.data()
    #                     entry[3] = top_node_right_child.left_child()
    #                     entry[4] = top_node_right_child.right_child()
    #                 queue.enqueue(tuple(entry))

    #     # if include_none == False, filter out the None element
    #     if not include_none:
    #         data_array = list(filter(lambda x: x is not None, data_array))

    #     # remove all None at the end of list since they are trival and not informative
    #     while data_array[-1] is None:
    #         data_array.pop()

    #     return data_array

    def level_order_traversal(self, starting_node=None, flatten=False):
        """
        Traverses the binary tree from top level to bottom

        Args:
            starting_node (TreeNode): traverse the subtree rooted at given starting node
            include_none (bool): True if including None node in binary tree

        Returns:
            data_array ([object]): [data saved in node]
        """

        data_array = self._level_order_traversal(starting_node)
        if flatten:
            data_array = [data[0] for array in data_array for data in array]

        return data_array




                
            

        



    


    
