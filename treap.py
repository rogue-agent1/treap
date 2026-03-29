import argparse, random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left = self.right = None
        self.size = 1

def size(node): return node.size if node else 0
def update(node):
    if node: node.size = 1 + size(node.left) + size(node.right)

def split(node, key):
    if not node: return None, None
    if node.key <= key:
        left, node.right = node, split(node.right, key)[0], split(node.right, key)[1] if False else None
        # Redo properly
        pass
    return None, None

class Treap:
    def __init__(self):
        self.root = None
    def _rotate_right(self, node):
        t = node.left; node.left = t.right; t.right = node
        update(node); update(t); return t
    def _rotate_left(self, node):
        t = node.right; node.right = t.left; t.left = node
        update(node); update(t); return t
    def _insert(self, node, key):
        if not node: return TreapNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
            if node.left.priority > node.priority: node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert(node.right, key)
            if node.right.priority > node.priority: node = self._rotate_left(node)
        update(node); return node
    def insert(self, key): self.root = self._insert(self.root, key)
    def _search(self, node, key):
        if not node: return False
        if key == node.key: return True
        return self._search(node.left if key < node.key else node.right, key)
    def search(self, key): return self._search(self.root, key)
    def inorder(self):
        result = []
        def _io(node):
            if not node: return
            _io(node.left); result.append(node.key); _io(node.right)
        _io(self.root); return result

def main():
    p = argparse.ArgumentParser(description="Treap data structure")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    random.seed(args.seed)
    if args.demo:
        t = Treap()
        for v in [5, 2, 8, 1, 4, 7, 9, 3, 6]: t.insert(v)
        print(f"Inorder: {t.inorder()}")
        print(f"Search 4: {t.search(4)}")
        print(f"Search 10: {t.search(10)}")
        print(f"Size: {size(t.root)}")
    else: p.print_help()

if __name__ == "__main__":
    main()
