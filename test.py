from collections import deque


class Node:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self) -> None:
        self.m = {}
        self.head = None
        self.tail = None

    def add_head(self, data):
        new = Node(data)
        if self.head is None:
            self.head = new
            self.tail = new
        else:
            new.pos = self.head.pos - 1
            new.next = self.head
            self.head.prev = new
            self.head = new

        if data in self.m:
            self.m[data].appendleft(new)
        else:
            self.m[data] = deque()
            self.m[data].append(new)

    def add_tail(self, data):
        if self.head is None:
            self.add_head(data)
            return
        
        new = Node(data)
        new.pos = self.tail.pos + 1
        new.prev = self.tail
        self.tail.next = new
        self.tail = new

        if data in self.m:
            self.m[data].append(new)
        else:
            self.m[data] = deque()
            self.m[data].append(new)

    def insert_after(self, a, b):
        if a not in self.m:
            self.add_head(b)
            return
        
        if a == self.tail.data:
            self.add_tail(b)
            return
        
        new = Node(b)
        curr = self.m[a][0]
        new.prev = curr
        new.next = curr.next
        new.pos = (curr.pos + new.next.pos) / 2
        self.m[a][0].next = new
        if b not in self.m:
            self.m[b] = deque()
            self.m[b].append(new)
        else:
            i = 0
            while i < len(self.m[b]) and new.pos > self.m[b][i].pos:
                i += 1

            self.m[b].insert(i, new)

    def remove(self, data):
        if self.head is None: 
            return
        
        if data not in self.m:
            return
        
        if data == self.head.data:
            self.remove_head()
            return
        
        if data == self.tail.data and len(self.m[data]) == 1:
            self.remove_tail()
            return

        it = self.m[data].popleft()
        it.prev.next = it.next
    
    def remove_head(self):
        if self.head is None:
            return
        
        data = self.head.data
        it = self.m[data].popleft()
        it.prev = None
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = it.next

    def remove_tail(self):
        if self.head is None:
            return
        
        data = self.tail.data
        it = self.m[data].pop()
        it.prev.next = None
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = it.prev

    def print_list(self):
        it = self.head
        while it is not None:
            print(it.data, end=' ')
            it = it.next


def bisect_left(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid].pos < x: lo = mid+1
        else: hi = mid
    return lo

linked_list = LinkedList()

import sys

while True:
    line = sys.stdin.readline().strip()
    if line == '6':
        break
    if line == '5':
        linked_list.remove_head()
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
