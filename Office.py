__author__ = 'prnbs'

import sys
import Queue as Q
import time

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
        self.i_left   = _i_left
        self.i_right  = _i_right
        self.i_cost   = _i_cost
        self.b_broken = False

    def __cmp__(self, edge_other):
        return cmp(self.cost, edge_other.cost)


class Office:
    def __init__(self):
        self.l_graph = []
        self.l_visited = []
        self.d_edge_dict = {}

    def get_the_other_node(self, edge_known, other_node):
        if edge_known.i_right == other_node:
            return edge_known.i_left
        else:
            return edge_known.i_right

    def reset_visited(self):
        for node in self.l_visited:
            node.b_visited = False
        self.l_visited = []

    def run_shortest_path(self, i_start, i_stop):
        i_graph_size = len(self.l_graph)
        l_distances  = []

        for i in range(i_graph_size):
            l_distances.append(sys.maxint)

        l_distances[i_start] = 0
        i_curr_node = i_start
        q_next_to_process = Q.PriorityQueue()

        while not self.l_graph[i_curr_node].b_visited:
            self.l_graph[i_curr_node].b_visited = True
            self.l_visited.append(self.l_graph[i_curr_node])

            for edge_next in self.l_graph[i_curr_node].l_adjacents:
                if not edge_next.b_broken:
                    # get the next Node
                    i_node_next = self.get_the_other_node(edge_next, i_curr_node)

                    # update the costs
                    if l_distances[i_node_next] > l_distances[i_curr_node] + edge_next.i_cost:
                        l_distances[i_node_next] = l_distances[i_curr_node] + edge_next.i_cost
                        # set the parent node
                        self.l_graph[i_node_next].node_parent = self.l_graph[i_curr_node]
                        # put this node in the priority queue
                        q_next_to_process.put(self.l_graph[i_node_next])

            #  now find the lowest costing node to process next
            if not q_next_to_process.empty():
                node_next = q_next_to_process.get()
                i_curr_node = node_next.i_name

            # if next node is goal node then our job is done
            if i_curr_node == i_stop:
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
        djikstra.d_edge_dict[(left, right)] = edge
        djikstra.d_edge_dict[(right, left)] = edge

    print "Finished creating graph"

    start_stop = raw_input().split()
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

    print distances[stop]
    count_seen = 0
    for num in distances:
        if num == sys.maxint:
            count_seen += 1
    print str(count_seen) + " nodes were not set"
    print str(len(djikstra.l_visited)) + " nodes were visited"
    print "Time = " + str(stopped_at - started_at)