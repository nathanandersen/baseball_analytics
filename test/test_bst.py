# tests binary search tree

from util import BinarySearchTree

def key_fun(item):
	return item

b = BinarySearchTree(key_fun)

for i in range(10):
	b.insert(i)

for i in b.in_order():
	print i