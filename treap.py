#!/usr/bin/env python3
"""treap - Randomized treap (tree + heap) data structure."""
import sys, random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left = None
        self.right = None
        self.size = 1

def _size(node):
    return node.size if node else 0

def _update(node):
    if node:
        node.size = 1 + _size(node.left) + _size(node.right)

def _rotate_right(node):
    left = node.left
    node.left = left.right
    left.right = node
    _update(node)
    _update(left)
    return left

def _rotate_left(node):
    right = node.right
    node.right = right.left
    right.left = node
    _update(node)
    _update(right)
    return right

def insert(root, key):
    if not root:
        return TreapNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.priority > root.priority:
            root = _rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key)
        if root.right.priority > root.priority:
            root = _rotate_left(root)
    _update(root)
    return root

def search(root, key):
    if not root:
        return False
    if key == root.key:
        return True
    if key < root.key:
        return search(root.left, key)
    return search(root.right, key)

def delete(root, key):
    if not root:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        if root.left.priority > root.right.priority:
            root = _rotate_right(root)
            root.right = delete(root.right, key)
        else:
            root = _rotate_left(root)
            root.left = delete(root.left, key)
    _update(root)
    return root

def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.key] + inorder(root.right)

def test():
    random.seed(42)
    root = None
    for x in [5, 3, 7, 1, 9, 2, 8, 4, 6]:
        root = insert(root, x)
    assert _size(root) == 9
    assert inorder(root) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert search(root, 5) and not search(root, 99)
    root = delete(root, 5)
    assert not search(root, 5)
    assert _size(root) == 8
    assert inorder(root) == [1, 2, 3, 4, 6, 7, 8, 9]
    print("OK: treap")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: treap.py test")
