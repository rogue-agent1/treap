#!/usr/bin/env python3
"""Treap (randomized BST)."""
import sys, random
class Node:
    def __init__(self,k): self.k,self.p,self.l,self.r=k,random.random(),None,None
def split(n,k):
    if not n: return None,None
    if n.k<=k: n.r,r=split(n.r,k); return n,r
    else: l,n.l=split(n.l,k); return l,n
def merge(l,r):
    if not l or not r: return l or r
    if l.p>r.p: l.r=merge(l.r,r); return l
    else: r.l=merge(l,r.l); return r
def insert(root,k): l,r=split(root,k); return merge(merge(l,Node(k)),r)
def inorder(n):
    if n: yield from inorder(n.l); yield n.k; yield from inorder(n.r)
root=None
for x in sys.argv[1:]: root=insert(root,int(x))
print(' '.join(map(str,inorder(root))))
