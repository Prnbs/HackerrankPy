__author__ = 'prnbs'

import sys
import Queue as Q
import time
import mmap
import os

# i_<var name> = integer type
# b_<var name> = boolean type
# l_<var name> = list
# d_<var name> = dictionary
# q_<var name> = queue
# edge_<var name> = an edge object
# node_<var name> = a node object


class Node:
    def __init__(self, _i_name):
        self.i_name      = _i_name
        self.l_adjacents = []
        self.b_visited   = False
        self.node_parent = self


class Edge:
    def __init__(self, _i_left, _i_right, _i_cost):
        self.i_left          = _i_left
        self.i_right         = _i_right
        self.i_cost          = _i_cost
        self.b_broken        = False
        self.b_shortest_edge = False

    def __cmp__(self, edge_other):
        return cmp(self.cost, edge_other.cost)


class Office:
    def __init__(self):
        self.l_graph = []
        self.l_visited = []
        self.d_edge_dict = {}
        self.d_shortest_path = {}

    def get_the_other_node(self, edge_known, other_node):
        if edge_known.i_right == other_node:
            return edge_known.i_left
        else:
            return edge_known.i_right

    def reset_visited(self):
        for node in self.l_visited:
            node.b_visited = False
        self.l_visited = []

    def mark_shortest_edge(self, i_start, i_stop):
        i_last_node = i_stop
        while self.l_graph[i_last_node].node_parent.i_name != i_start:
            # get edge node
            edge_current = self.d_edge_dict[(self.l_graph[i_last_node].node_parent.i_name, i_last_node)]
            # mark it as shortest path
            edge_current.b_shortest_edge = True
            # add shortest edge to dictionary
            self.d_shortest_path[(self.l_graph[i_last_node].node_parent.i_name, i_last_node)] = edge_current
            self.d_shortest_path[(i_last_node, self.l_graph[i_last_node].node_parent.i_name)] = edge_current
            # update next node
            i_last_node = self.l_graph[i_last_node].node_parent.i_name
        # update for starting node
        edge_current = self.d_edge_dict[(i_start, i_last_node)]
        edge_current.b_shortest_edge = True
        # add start edge to dictionary
        self.d_shortest_path[(i_start, i_last_node)] = edge_current
        self.d_shortest_path[(i_last_node, i_start)] = edge_current

    def run_shortest_path(self, i_start, i_stop):
        i_graph_size = len(self.l_graph)
        l_distances  = [] #np.full(i_graph_size, sys.maxint)

        for i in range(i_graph_size):
            l_distances.append(sys.maxint)

        l_distances[i_start] = 0
        i_curr_node = i_start
        q_next_to_process = Q.PriorityQueue()

        i_time_start = time.time()
        while not self.l_graph[i_curr_node].b_visited:
            self.l_graph[i_curr_node].b_visited = True
            self.l_visited.append(self.l_graph[i_curr_node])

            for edge_next in self.l_graph[i_curr_node].l_adjacents:
                if not edge_next.b_broken:
                    # get the next Node
                    i_node_next = self.get_the_other_node(edge_next, i_curr_node)
                    if self.l_graph[i_node_next].b_visited:
                        continue
                    # update the costs
                    i_next_cost = l_distances[i_curr_node] + edge_next.i_cost
                    if l_distances[i_node_next] > i_next_cost:
                        l_distances[i_node_next] = i_next_cost
                        # set the parent node
                        self.l_graph[i_node_next].node_parent = self.l_graph[i_curr_node]
                        # put this node in the priority queue
                        q_next_to_process.put(self.l_graph[i_node_next])

            #  now find the lowest costing unvisited node to process next
            while not q_next_to_process.empty():
                node_next = q_next_to_process.get()
                if not node_next.b_visited:
                    i_curr_node = node_next.i_name
                    break
            # if next node is goal node then our job is done
            if i_curr_node == i_stop:
                break
        i_time_stop = time.time()
        print "Djikstra's main while in " + str(i_time_stop - i_time_start)

        return l_distances

if __name__ == '__main__':
    global_start = time.time()
    djikstra = Office()
    start = 0
    stop  = 0
    with open(sys.argv[1], "r") as f:
        mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        graphInit = mm.readline().split()

        N = int(graphInit[0])
        M = int(graphInit[1])

        for i in range(N):
            djikstra.l_graph.append(Node(i))

        for i in range(M):
            nodes  = mm.readline().split()
            left   = int(nodes[0])
            right  = int(nodes[1])
            weight = int(nodes[2])
            edge   = Edge(left, right, weight)
            djikstra.l_graph[left].l_adjacents.append(edge)
            djikstra.l_graph[right].l_adjacents.append(edge)
            djikstra.d_edge_dict[(left, right)] = edge
            djikstra.d_edge_dict[(right, left)] = edge

        print "Finished creating graph"

        start_stop = mm.readline().split()
        start      = int(start_stop[0])
        stop       = int(start_stop[1])

    # i_queries = int(raw_input())
    #
    # for i in range(i_queries):
    #     l_brokenEdges = raw_input().split()
    #     i_broken_edge_start = int(l_brokenEdges[0])
    #     i_broken_edge_end = int(l_brokenEdges[1])
    #
    #     edge_broken = djikstra.d_edge_dict[(i_broken_edge_start, i_broken_edge_end)]
    #     edge_broken.b_broken = True
    started_at = time.time()
    distances  = djikstra.run_shortest_path(start, stop)
    stopped_at = time.time()
    #     edge_broken.b_broken = False
    #     djikstra.reset_visited()
    # djikstra.mark_shortest_edge(start, stop)

    print distances[stop]

    global_stop = time.time()

    print "Time = " + str(stopped_at - started_at)

    print "Total time = " + str(global_stop - global_start)