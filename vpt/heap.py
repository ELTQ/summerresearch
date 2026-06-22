# code from CP307

import copy
import random 

class BinaryTree():
    
    def __init__(self):
        self.root = None
    
    def add(self, k, v):
        if self.root is None:
            self.root = BinaryTreeNode(k,v)
        else:
            self.root.add(k,v)
    
    def search(self, k):
        if self.root is None:
            return None
        return self.root.search(k)
    
    def depth(self):
        if self.root is None:
            return 0
        else:
            return self.root.depth()
    
    def print(self):
        if self.root is None:
            print("Empty")
        else:
            self.root.print()
    
class BinaryTreeNode():
    
    def __init__(self, k, v):
        
        self.k = k
        self.v = v
        self.p = None
        self.lc = None
        self.rc = None
        
    def add(self, k, v):
        
        if self.lc is None:
            self.lc = BinaryTreeNode(k,v)
            self.lc.p = self
        elif self.rc is None:
            self.rc = BinaryTreeNode(k,v)
            self.rc.p = self
        else:
            if random.random() < .5:
                self.rc.add(k,v)
            else:
                self.lc.add(k,v)
                
    def search(self, k):
        if self.k == k:
            return self.v
        if self.lc:
            lc_result = self.lc.search(k)
            if lc_result is not None:
                return lc_result
        if self.rc:
            rc_result = self.rc.search(k)
            if rc_result is not None:
                return rc_result
        return None
    
    def depth(self):
        if self.lc is None:
            lc_depth = 0
        else:
            lc_depth = self.lc.depth()
            
        if self.rc is None:
            rc_depth = 0
        else:
            rc_depth = self.rc.depth()
        
        if self.rc is None and self.lc is None:
            return 0
        else:
            return max(lc_depth, rc_depth) + 1
        
    def print(self, gen=0):
        print("\t" * gen, self.k, self.v)
        if self.lc:
            self.lc.print(gen=gen+1)
        if self.rc:
            self.rc.print(gen=gen+1)

class MaxHeap(BinaryTree):
    def add(self, k, v):
        if self.root is None:
            self.root = MaxHeapNode(k,v)
        else:
            self.root.add(k,v)
            if self.root.checkHeapProperty() != True:
                self.sortHeap()
    def checkHeapProperty(self):
        if self.root == None:
            return 0
        return self.root.checkHeapProperty()
    def checkSize(self):
        if self.root == None:
            return 0
        return self.root.nodeSize()

    def sortHeap(self):
        if self.root == None:
            print("empty tree") 
        else:
            root = self.root.sortHeap()
            self.root = root
        return 1
            
    def pop(self): # remove root from tree
        rootNode = copy.deepcopy(self.root) # truly a python moment that cost me hours of debugging. thanks, deepcopy!
        for i in range(self.root.k): # get smaller object and put up top
            if self.search(i) != None:
                self.root.swap(i, None, None)
                break
        while not(self.checkHeapProperty()):
            self.sortHeap()
        return rootNode
class MaxHeapNode(BinaryTreeNode):
    def insert(self, k, v):
        pass
    def checkHeapProperty(self):
        status = True
        if self.lc != None and self.lc.k != None:
            if self.lc.checkHeapProperty() != True:
                status = False
            if self.lc.k > self.k: # subnodes can't be bigger than parent node
                status = False
        if self.rc != None and self.rc.k != None:
            if self.rc.checkHeapProperty() != True:
                status = False
            if self.rc.k > self.k:
                status = False
        return status
        
    def nodeSize(self):
        size = 0
        if self.lc != None:
            size += self.lc.nodeSize()
        if self.rc != None:
            size += self.rc.nodeSize()
        return size + 1 
        
    def sortHeap(self):
        if self.lc != None:
            self.lc.sortHeap()
        if self.rc != None:
            self.rc.sortHeap()

        if self.lc != None:
            
            if self.lc.k > self.k:
                tempk = self.lc.k
                tempv = self.lc.v
                self.lc.k = self.k
                self.lc.v = self.v
                '''
                self.lc.p = self.p
                self.p = self.lc
                '''
                self.k = tempk
                self.v = tempv
        if self.rc != None:
            
            if self.rc.k > self.k:
                tempk = self.rc.k
                tempv = self.rc.v
                self.rc.k = self.k
                self.rc.v = self.v
                '''
                self.rc.p = self.p
                self.p = self.rc
                '''
                self.k = tempk
                self.v = tempv
    
        # if self changed, the return value also changed (ie new root)
        # lowkey isn't this address already root
        return self
    def add(self, k, v):
        
        if self.lc is None:
            self.lc = MaxHeapNode(k,v)
            self.lc.p = self
        elif self.rc is None:
            self.rc = MaxHeapNode(k,v)
            self.rc.p = self
        else:
            if random.random() < .5:
                self.rc.add(k,v)
                #self.rc.p = self
            else:
                self.lc.add(k,v)
                #self.lc.p = self

    def swap(self, k, replace_k, replace_v, d=0):
        
        old_val = None
        if self.k == k:
            old_val = self.v
            '''
            print("old_val is", old_val)
            print("key is", self.k)
            '''
            if replace_k == None and replace_v == None: # chief's dead!
                if (self == self.p.lc):
                    self.p.lc = None
                else:
                    self.p.rc = None
            else:
                self.k = replace_k
                self.v = replace_v
            return old_val
            
        if self.lc:
            lc_result = self.lc.swap(k, replace_k, replace_v, d=d+1)
            if lc_result is not None:
                if d != 0:
                    return lc_result
                else:
                    old_val = lc_result
            else:
                old_val = None
                
        if self.rc and old_val == None:
            rc_result = self.rc.swap(k, replace_k, replace_v, d=d+1)
            if rc_result is not None:
                if d != 0:
                    return rc_result
                else:
                    old_val = rc_result
            else:
                old_val = None
        # detect if we are in base case
        # if we are, update self.k and be done
        if d == 0 and old_val != None: # break into this case if we followed a path to a dead end
            self.v = old_val
            #print(self.k, "will be updated with", k)
            self.k = k
        return None


class PQueue(MaxHeap):
    def enqueue(self, k, v):
        self.add(k, v)
    def dequeue(self):
        return self.pop().v
    def update(self, searched_key, new_key, v):
        if self.search(searched_key):
            if searched_key < new_key:
                self.root.swap(searched_key, new_key, v)
                self.sortHeap()

def heapSort(myList):
    sortedList = [0] * len(myList)
    myQueue = PQueue()

    for i in range(len(myList)):
        myQueue.enqueue(myList[i], '') # value is not useful here
    for i in range(len(myList)):
        sortedList[i] = myQueue.pop().k
    return sortedList