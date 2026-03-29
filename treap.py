#!/usr/bin/env python3
"""treap - Randomized treap (tree + heap) with split/merge."""
import sys, json, random

class TreapNode:
    def __init__(self, key, value=None, priority=None):
        self.key = key; self.value = value
        self.priority = priority if priority is not None else random.random()
        self.left = None; self.right = None; self.size = 1

def _size(node): return node.size if node else 0

def _update(node):
    if node: node.size = 1 + _size(node.left) + _size(node.right)

def split(node, key):
    if not node: return None, None
    if node.key <= key:
        left, node.right = split(node.right, key)
        _update(node)
        return node, left
    else:
        node.left, right = split(node.left, key)
        _update(node)
        return right, node

def merge(left, right):
    if not left: return right
    if not right: return left
    if left.priority > right.priority:
        left.right = merge(left.right, right)
        _update(left); return left
    else:
        right.left = merge(left, right.left)
        _update(right); return right

class Treap:
    def __init__(self):
        self.root = None
    
    def insert(self, key, value=None):
        left, right = split(self.root, key - 0.5)
        node = TreapNode(key, value)
        self.root = merge(merge(left, node), right)
    
    def delete(self, key):
        left, right = split(self.root, key - 0.5)
        _, right = split(right, key)
        self.root = merge(left, right)
    
    def search(self, key):
        node = self.root
        while node:
            if key == node.key: return node.value
            elif key < node.key: node = node.left
            else: node = node.right
        return None
    
    def kth(self, k):
        node = self.root
        while node:
            ls = _size(node.left)
            if k <= ls: node = node.left
            elif k == ls + 1: return node.key
            else: k -= ls + 1; node = node.right
        return None
    
    def inorder(self):
        result = []
        def traverse(node):
            if not node: return
            traverse(node.left); result.append(node.key); traverse(node.right)
        traverse(self.root)
        return result
    
    @property
    def size(self): return _size(self.root)

def main():
    random.seed(42)
    t = Treap()
    print("Treap demo\n")
    for x in [5,3,8,1,9,2,7,4,6,10]:
        t.insert(x, f"v{x}")
    print(f"  Size: {t.size}")
    print(f"  Sorted: {t.inorder()}")
    print(f"  Search(7): {t.search(7)}")
    print(f"  3rd smallest: {t.kth(3)}")
    t.delete(5); t.delete(8)
    print(f"  After delete 5,8: {t.inorder()}")

if __name__ == "__main__":
    main()
