#!/usr/bin/env python3
"""treap - Randomized binary search tree (treap)."""
import sys,random
class Node:
    def __init__(s,key,pri=None):s.key=key;s.pri=pri or random.random();s.left=s.right=None;s.size=1
def size(n):return n.size if n else 0
def update(n):
    if n:n.size=1+size(n.left)+size(n.right)
def split(n,key):
    if not n:return None,None
    if n.key<=key:l,n.right=n,split(n.right,key);update(l);return l,n.right
    else:n.left,r=split(n.left,key);update(n);return n.left,n
def merge(l,r):
    if not l or not r:return l or r
    if l.pri>r.pri:l.right=merge(l.right,r);update(l);return l
    else:r.left=merge(l,r.left);update(r);return r
def insert(root,key):l,r=split(root,key-0.5);return merge(merge(l,Node(key)),r)
def delete(root,key):
    l,r=split(root,key-0.5);_,r=split(r,key);return merge(l,r)
def inorder(n):
    if not n:return[]
    return inorder(n.left)+[n.key]+inorder(n.right)
def kth(n,k):
    ls=size(n.left)
    if k<=ls:return kth(n.left,k)
    if k==ls+1:return n.key
    return kth(n.right,k-ls-1)
if __name__=="__main__":
    root=None;data=[5,3,8,1,4,7,9,2,6]
    for d in data:root=insert(root,d)
    print(f"Inserted: {data}");print(f"Inorder: {inorder(root)}")
    print(f"Size: {size(root)}");print(f"3rd smallest: {kth(root,3)}")
    root=delete(root,5);print(f"After delete 5: {inorder(root)}")
