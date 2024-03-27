from collections import deque, defaultdict


class Node:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.m = defaultdict(deque)
        self.size = 0

    def add_head(self, data):
        new = Node(data)
        if self._is_empty():
            self.head = new
            self.tail = new
        else:
            new.pos = self.head.pos - 1
            new.next = self.head
            self.head.prev = new
            self.head = new

        self.m[data].appendleft(new)
        self.size += 1

    def add_tail(self, data):
        new = Node(data)
        if self.head is None or self.tail is None:
            self.head = new
            self.tail = new
        else:
            new.pos = self.tail.pos + 1
            new.prev = self.tail
            self.tail.next = new
            self.tail = new

        self.m[data].append(new)
        self.size += 1

    def _contains(self, data):
        return len(self.m[data]) > 0
    
    def _is_empty(self):
        return self.size == 0
    
    def _is_single(self):
        return self.size == 1
    
    def _is_head(self, node):
        return node.prev is None
    
    def _is_tail(self, node):
        return node.next is None
    
    def clear(self):
        self.head = None
        self.tail = None
        self.m = defaultdict(deque)
        self.size = 0

    def insert_after(self, a, b):
        if not self._contains(a):
            self.add_head(b)
            return
        
        curr = self.m[a][0]

        if self._is_tail(curr):
            self.add_tail(b)
            return

        new = Node(b)
        new.prev = curr
        new.next = curr.next

        curr.next = new
        new.next.prev = new
        new.pos = (curr.pos + new.next.pos) / 2
        
        i = 0
        while i < len(self.m[b]) and new.pos > self.m[b][i].pos:
            i += 1

        self.m[b].insert(i, new)
        self.size += 1


    def remove(self, data):
        pass
        if self._is_empty() or not self._contains(data):
            return

        if self._is_single():
            self.clear()
            return
        
        tar = self.m[data].popleft()

        if self._is_head(tar):
            if tar.next is not None:
                tar.next.prev = None

            self.head = tar.next
            tar.next = None
            return
        
        if self._is_tail(tar):
            if tar.prev is not None:
                tar.prev.next = None

            self.tail = tar.prev
            tar.prev = None
            return
        
        if tar.prev is not None:
            tar.prev.next = tar.next
        if tar.next is not None:
            tar.next.prev = tar.prev
    

    def print_list(self):
        it = self.head
        while it is not None:
            print(it.data, end=' ')
            it = it.next

linked_list = LinkedList()

import sys

while True:
    line = sys.stdin.readline().strip()
    if line == '6':
        break
    if line == '5':
        if linked_list.head:
            linked_list.remove(linked_list.head.data)
        continue

    operation, *args = line.split()
    if operation == '0':
        linked_list.add_head(*args)
    elif operation == '1':
        linked_list.add_tail(*args)
    elif operation == '2':
        linked_list.insert_after(*args)
    elif operation == '3':
        linked_list.remove(*args)

linked_list.print_list()