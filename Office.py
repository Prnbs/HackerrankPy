__author__ = 'prnbs'

import sys
import Queue as Q


class Node:
    def __init__(self, _i_name):
        self.i_name      = _i_name
        self.l_adjacents = []
        self.b_visited   = False
        self.node_parent = self


class Edge:
    def __init__(self, _i_left, _i_right, _i_cost):
        self.i_left   = _i_left
        self.i_right  = _i_right
        self.i_cost   = _i_cost
        self.b_broken = False

    def __cmp__(self, edge_other):
        return cmp(self.cost, edge_other.cost)


class Office:
    def __init__(self):
        self.l_graph = []
        self.b_visited = []

    def get_the_other_node(self, edge, other_node):
        if edge.i_right == other_node:
            return edge.i_left
        else:
            return edge.i_right

    def reset_visited(self):
        for node in self.b_visited:
            node.b_visited = False

    def run_shortest_path(self, i_start, i_stop):
        i_graph_size = len(self.l_graph)
        l_distances  = []

        for i in range(i_graph_size):
            l_distances.append(sys.maxint)

        l_distances[i_start] = 0
        i_currNode = i_start
        q_next_to_process = Q.PriorityQueue()

        while not self.l_graph[i_currNode].b_visited:
            self.l_graph[i_currNode].b_visited = True

            for edge_next in self.l_graph[i_currNode].l_adjacents:
                if not edge_next.b_broken:
                    # get the next Node
                    i_node_next = self.get_the_other_node(edge_next, i_currNode)

                    # print type(edge)
                    if l_distances[i_node_next] > l_distances[i_currNode] + edge_next.i_cost:
                        l_distances[i_node_next] = l_distances[i_currNode] + edge_next.i_cost
                        self.l_graph[i_node_next].node_parent = self.l_graph[i_currNode]
                        q_next_to_process.put(self.l_graph[i_node_next])

            while not q_next_to_process.empty():
                i_node_next = q_next_to_process.get()
                if not i_node_next.b_visited:
                    i_currNode = i_node_next.i_name
                    break

        return l_distances

if __name__ == '__main__':
    djikstra = Office()
    graphInit = raw_input().split()
    N = int(graphInit[0])
    M = int(graphInit[1])
    for i in range(N):
        djikstra.l_graph.append(Node(i))

    for i in range(M):
        nodes  = raw_input().split()
        left   = int(nodes[0])
        right  = int(nodes[1])
        weight = int(nodes[2])
        edge   = Edge(left, right, weight)
        djikstra.l_graph[left].l_adjacents.append(edge)
        djikstra.l_graph[right].l_adjacents.append(edge)

    print "Finished creating graph"

    start_stop = raw_input().split()
    start      = int(start_stop[0])
    stop       = int(start_stop[1])

    distances = djikstra.run_shortest_path(start, stop)

    print distances[stop]