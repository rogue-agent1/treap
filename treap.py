#!/usr/bin/env python3
"""Treap - Randomized BST with heap property for balanced operations."""
import sys, random

class Node:
    def __init__(self, key, priority=None):
        self.key = key; self.priority = priority if priority is not None else random.random()
        self.left = None; self.right = None; self.size = 1
    def update(self):
        self.size = 1 + (self.left.size if self.left else 0) + (self.right.size if self.right else 0)

def split(node, key):
    if not node: return None, None
    if node.key <= key:
        node.right, right = split(node.right, key)
        node.update(); return node, right
    else:
        left, node.left = split(node.left, key)
        node.update(); return left, node

def merge(left, right):
    if not left: return right
    if not right: return left
    if left.priority > right.priority:
        left.right = merge(left.right, right); left.update(); return left
    else:
        right.left = merge(left, right.left); right.update(); return right

class Treap:
    def __init__(self): self.root = None
    def insert(self, key):
        left, right = split(self.root, key)
        self.root = merge(merge(left, Node(key)), right)
    def delete(self, key):
        left, right = split(self.root, key)
        left2, _ = split(left, key - 1)
        self.root = merge(left2, right)
    def find(self, key):
        node = self.root
        while node:
            if key == node.key: return True
            node = node.left if key < node.key else node.right
        return False
    def kth(self, k):
        node = self.root
        while node:
            left_size = node.left.size if node.left else 0
            if k == left_size: return node.key
            elif k < left_size: node = node.left
            else: k -= left_size + 1; node = node.right
        return None
    def inorder(self):
        result = []
        def dfs(n):
            if not n: return
            dfs(n.left); result.append(n.key); dfs(n.right)
        dfs(self.root); return result
    @property
    def size(self): return self.root.size if self.root else 0

def main():
    random.seed(42); t = Treap()
    for x in [5, 2, 8, 1, 4, 7, 9, 3, 6]: t.insert(x)
    print(f"=== Treap ({t.size} nodes) ===\n")
    print(f"Sorted: {t.inorder()}")
    print(f"Find(4): {t.find(4)}, Find(10): {t.find(10)}")
    print(f"3rd element (0-indexed): {t.kth(3)}")
    t.delete(5); print(f"After delete(5): {t.inorder()}")

if __name__ == "__main__":
    main()
