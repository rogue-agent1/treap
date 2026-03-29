#!/usr/bin/env python3
"""treap - Randomized BST (treap) with split/merge."""
import random, sys

class Node:
    __slots__ = ['key', 'priority', 'left', 'right', 'size']
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = None
        self.right = None
        self.size = 1

def _size(node):
    return node.size if node else 0

def _update(node):
    if node:
        node.size = 1 + _size(node.left) + _size(node.right)

def split(node, key):
    if not node:
        return None, None
    if node.key <= key:
        left, node.right = node, split(node.right, key)[0], None
        node.right, right = split(node.right if hasattr(node, '_tmp') else None, key)
        # Simpler approach
        pass
    # Let me redo with cleaner split
    pass

def _split(node, key):
    if not node:
        return None, None
    if node.key <= key:
        left, right = _split(node.right, key)
        node.right = left
        _update(node)
        return node, right
    else:
        left, right = _split(node.left, key)
        node.left = right
        _update(node)
        return left, node

def _merge(left, right):
    if not left or not right:
        return left or right
    if left.priority > right.priority:
        left.right = _merge(left.right, right)
        _update(left)
        return left
    else:
        right.left = _merge(left, right.left)
        _update(right)
        return right

class Treap:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        left, right = _split(self.root, key - 0.5)
        self.root = _merge(_merge(left, Node(key)), right)
    
    def delete(self, key):
        left, mid_right = _split(self.root, key - 0.5)
        mid, right = _split(mid_right, key)
        if mid:
            mid = _merge(mid.left, mid.right)  # Remove root of mid
        self.root = _merge(_merge(left, mid), right)
    
    def contains(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False
    
    def kth(self, k):
        """Find k-th smallest (0-indexed)."""
        node = self.root
        while node:
            left_size = _size(node.left)
            if k < left_size:
                node = node.left
            elif k == left_size:
                return node.key
            else:
                k -= left_size + 1
                node = node.right
        return None
    
    def rank(self, key):
        """Count elements < key."""
        left, right = _split(self.root, key - 0.5)
        r = _size(left)
        self.root = _merge(left, right)
        return r
    
    def size(self):
        return _size(self.root)
    
    def inorder(self):
        result = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            result.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return result

def test():
    random.seed(42)
    t = Treap()
    
    for x in [5, 3, 7, 1, 4, 6, 8, 2]:
        t.insert(x)
    
    assert t.size() == 8
    assert t.contains(5)
    assert not t.contains(9)
    assert t.inorder() == [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Kth
    assert t.kth(0) == 1
    assert t.kth(3) == 4
    assert t.kth(7) == 8
    
    # Rank
    assert t.rank(5) == 4
    assert t.rank(1) == 0
    
    # Delete
    t.delete(5)
    assert not t.contains(5)
    assert t.size() == 7
    assert t.inorder() == [1, 2, 3, 4, 6, 7, 8]
    
    # Stress
    t2 = Treap()
    for i in range(1000):
        t2.insert(i)
    assert t2.size() == 1000
    assert t2.kth(500) == 500
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: treap.py test")
