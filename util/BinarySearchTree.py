# BINARY SEARCH TREE - 
# Python BST implementation

import game_model

__all__ = ["BinarySearchTree","identity_key","date_key"]

# SOME BASIC KEY FUNCTIONS
def identity_key(item):
	return item

def date_key(item):
	return item.date

# BINARY SEARCH TREE IMPLEMENTATION
class BinarySearchTree(object):
	def __init__(self,key_function = identity_key):
		self.key_function = key_function
		self.root = None

	#returns either the item or None
	def lookup(self,item):
		found = _find(self.key_function(item),self.root)
		if found is not None:
			found = found.item
		return found
	
	#recursively traverses the BST
	def _find(key,node):
		if node == None or node.key == key:
			return node
		elif key < node.key:
			_find(key,node.left_child)
		else:
			_find(key,node.right_child)

	def insert(self,item):
		#handle empty tree case:
		if self.root is None:
			self.root = BSTNode(self.key_function(item),item)
		#otherwise
		else:
			self._insert(self.key_function(item),self.root,item)

	def _insert(self,key,current_node,item):
		if key < current_node.key:
			if current_node.left_child is None:
				current_node.left_child = BSTNode(key,item)
			else:
				self._insert(key,current_node.left_child,item)
		else:
			if current_node.right_child is None:
				current_node.right_child = BSTNode(key,item)
			else:
				self._insert(key,current_node.right_child,item)

	#iterators, by default it will follow an in order traversal
	def in_order(self):
		if self.root is None:
			return
		for node in self._in_order(self.root):
			yield node.item

	def _in_order(self,current_node):
		if current_node is None:
			return
		for node in self._in_order(current_node.left_child):
			yield node
		yield current_node
		for node in self._in_order(current_node.right_child):
			yield node

	@property
	def empty(self):
		return self.root is None

class BSTNode(object):

	def __init__(self,key,item):
		self.item = item
		self.key = key
		self.left_child = None
		self.right_child = None