#!/usr/bin/env python3
"""Treap — randomized BST with heap property."""
import sys, random

class TreapNode:
    __slots__ = ('key','priority','left','right','size')
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = self.right = None
        self.size = 1

def _size(n): return n.size if n else 0
def _update(n):
    if n: n.size = 1 + _size(n.left) + _size(n.right)

def split(node, key):
    if not node: return None, None
    if node.key <= key:
        node.right, right = split(node.right, key)
        _update(node)
        return node, right
    else:
        left, node.left = split(node.left, key)
        _update(node)
        return left, node

def merge(left, right):
    if not left: return right
    if not right: return left
    if left.priority > right.priority:
        left.right = merge(left.right, right)
        _update(left)
        return left
    else:
        right.left = merge(left, right.left)
        _update(right)
        return right

class Treap:
    def __init__(self):
        self.root = None
    def insert(self, key):
        l, r = split(self.root, key - 0.5)
        self.root = merge(merge(l, TreapNode(key)), r)
    def delete(self, key):
        l, mr = split(self.root, key - 0.5)
        _, r = split(mr, key)
        self.root = merge(l, r)
    def __contains__(self, key):
        n = self.root
        while n:
            if key == n.key: return True
            n = n.left if key < n.key else n.right
        return False
    def __len__(self):
        return _size(self.root)
    def inorder(self):
        result = []
        def _io(n):
            if not n: return
            _io(n.left); result.append(n.key); _io(n.right)
        _io(self.root)
        return result

def test():
    t = Treap()
    for x in [5,3,7,1,4,6,8,2]:
        t.insert(x)
    assert len(t) == 8
    assert 5 in t
    assert 9 not in t
    assert t.inorder() == [1,2,3,4,5,6,7,8]
    t.delete(3)
    assert 3 not in t
    assert len(t) == 7
    print("  treap: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Treap — randomized BST")
