# This project was created by Max Paulenz for the purpose of the HW0 assignment in CSIE5400-02
# Student ID a12921301

# Preparation
# Islands will be referred to as Nodes and Bridges as Edges inside a graph

# Translation of the rules
# 1 & 2 Each node should not be in the path more than once
# 3 When multiple Nodes are available, always choose the one with the lowest index
# 4 & 5 All Nodes are equal

# Find the longest continous path in the graph

# Expected Time Complexity: O(N)

# Expected Edge Cases:
# 1. A graph with no Edges



import sys

class Solution:
    def __init__(self):
        # The first node is always 1
        self.STARTNODE = 1

        # Input the Nodes and Edges from the command line
        self.input = sys.stdin.read()
        # Split the input into a list of strings
        self.input = self.input.split()
        # Group the input into Tuple pairs of integers
        try:
            self.input = list(zip(self.input[::2], self.input[1::2]))
            self.input = list((int(x), int(y)) for x, y in self.input)
        except ValueError:
            print('Input must be a list of integers')
            sys.exit(1)

        # Read the first Tuple as the number of Nodes and Edges
        self.numNodes = self.input[0][0] #N
        self.numEdges = self.input[0][1] #M
        self.input.pop(0)
        print('Number of Nodes:', self.numNodes, '\nNumber of Edges:', self.numEdges)
        self.get_graph()



    # A graph is represented as a dict of sets, as inspired by https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
    def get_graph(self):
        # Create a dictionary with the Nodes as keys and an empty set as the value
        self.graph = {}
        for i in range(1, self.numNodes+1):
            self.graph[i] = set()

        # Add the Edges to the graph
        try:
            for edge in self.input:
                if edge[0] == edge[1]:
                    print('A Node cannot be connected to itself')
                    sys.exit(1)
                self.graph[edge[0]].add(edge[1])
                self.graph[edge[1]].add(edge[0])
        except KeyError:
            print('Edge does not exist')
            sys.exit(1)

        print('Graph:', self.graph)

        
    def solve(self):
        self.currentNode = self.STARTNODE
        self.longestPath = [self.currentNode]
        # Find the longest path
        while len(self.graph[self.currentNode]):
            # Remove the current Node from the graph
            for node, edges in self.graph.items():
                if self.currentNode in edges:
                    edges.remove(self.currentNode)

            # Find the next Node
            self.currentNode = min(self.graph[self.currentNode])
            self.longestPath.append(self.currentNode)
        
        print('Longest Path:', self.longestPath)
            

    
    # Feel free to define your own member function

if __name__ == '__main__':
    ans = Solution()
    ans.solve()