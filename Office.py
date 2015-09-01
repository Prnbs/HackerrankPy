__author__ = 'prnbs'

import sys
import time
import Queue as Q
import numpy as np
import fileinput

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
        self.b_in_shortest_path = False


class Edge:
    def __init__(self, _i_left, _i_right, _i_cost):
        self.i_left          = _i_left
        self.i_right         = _i_right
        self.i_cost          = _i_cost
        self.b_broken        = False
        self.b_shortest_edge = False

    def __cmp__(self, edge_other):
        return cmp(self.cost, edge_other.cost)

    def __eq__(self, other):
        return self.i_right == other.i_right and self.i_left == other.i_left

    def __ne__(self, other):
        return not self.__eq__(other)


class Office:
    def __init__(self):
        self.l_graph = []
        self.l_visited = []
        self.d_edge_dict = {}
        self.l_shortest_path = []

    def get_the_other_node(self, edge_known, i_other_node):
        if edge_known.i_right == i_other_node:
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
            # add shortest edge to list
            self.l_shortest_path.append(edge_current)
            # update next node
            i_last_node = self.l_graph[i_last_node].node_parent.i_name

        # update for starting node
        edge_current = self.d_edge_dict[(i_start, i_last_node)]
        edge_current.b_shortest_edge = True
        # add start edge to dictionary
        self.l_shortest_path.append(edge_current)
        self.l_shortest_path.reverse()

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
                    if self.l_graph[i_node_next].b_visited:
                        continue
                    # update the costs
                    i_next_cost = l_distances[i_curr_node] + edge_next.i_cost
                    if l_distances[i_node_next] > i_next_cost:
                        l_distances[i_node_next] = i_next_cost
                        # set the parent node
                        self.l_graph[i_node_next].node_parent = self.l_graph[i_curr_node]
                        # put this node in the priority queue
                        q_next_to_process.put((i_next_cost, i_node_next))

            #  now find the lowest costing unvisited node to process next
            while not q_next_to_process.empty():
                (i_cost, i_next_node) = q_next_to_process.get()
                if not self.l_graph[i_next_node].b_visited:
                    i_curr_node = i_next_node
                    break
            # if next node is goal node then our job is done
            if i_curr_node == i_stop:
                break

        return l_distances

    def compute_next_shortest_cost(self, edge_broken, l_known_shortest, i_start, i_stop):
        l_new_shortest = np.full(len(self.l_graph), sys.maxint)
        l_new_shortest[i_start] = 0
        i_curr_node = i_start
        q_next_nodes = Q.PriorityQueue()
        d_seen_nodes = {}
        q_next_nodes.put((0,i_curr_node))
        i_while_count = 0
        while not q_next_nodes.empty():
            i_while_count +=1
            (x, i_curr_node) = q_next_nodes.get()
            if i_curr_node not in d_seen_nodes:
                if i_curr_node == i_stop:
                    break
                for edge_adjacent in self.l_graph[i_curr_node].l_adjacents:
                    if not edge_adjacent.b_broken:
                        i_other_node = self.get_the_other_node(edge_adjacent, i_curr_node)
                        if i_other_node not in d_seen_nodes:
                            if l_new_shortest[i_other_node] > l_new_shortest[i_curr_node] + edge_adjacent.i_cost:
                                l_new_shortest[i_other_node] = l_new_shortest[i_curr_node] + edge_adjacent.i_cost
                                # if new cost equals shortest path cost i_other_node's cost will never be updated again
                                # if l_new_shortest[i_other_node] == l_known_shortest[i_other_node]:
                                #     q_next_nodes.put(i_other_node)
                                #     break
                            if i_other_node not in d_seen_nodes:
                                q_next_nodes.put((l_new_shortest[i_other_node],i_other_node))

                d_seen_nodes[i_curr_node] = True
        print "While ran for " + str(i_while_count)
        return l_new_shortest

if __name__ == '__main__':
    global_start = time.time()
    djikstra = Office()
    std_input = fileinput.input()
    [N, M] = map(int, std_input.readline().split())

    for i in range(N):
        djikstra.l_graph.append(Node(i))

    for i in range(M):
        [left, right, weight] = map(int, std_input.readline().split())
        edge   = Edge(left, right, weight)
        djikstra.l_graph[left].l_adjacents.append(edge)
        djikstra.l_graph[right].l_adjacents.append(edge)
        djikstra.d_edge_dict[(left, right)] = edge
        djikstra.d_edge_dict[(right, left)] = edge

    [start, stop] = map(int, std_input.readline().split())

    # perform djikstra on full graph
    l_shortest_distances  = djikstra.run_shortest_path(start, stop)
    # print "Shortest Path = " + str(l_shortest_distances[stop])
    # colour the edges which lead to shortest path
    djikstra.mark_shortest_edge(start, stop)
    i_queries = int(std_input.readline())
    query_start = time.time()
    for i in range(i_queries):
        [i_broken_edge_start, i_broken_edge_end] = map(int, std_input.readline().split())

        edge_broken = djikstra.d_edge_dict[(i_broken_edge_start, i_broken_edge_end)]
        if edge_broken.b_shortest_edge:
            edge_broken.b_broken = True
            l_new_short = djikstra.compute_next_shortest_cost(edge_broken, l_shortest_distances, start, stop)
            edge_broken.b_broken = False
            if l_new_short[stop] == sys.maxint:
                print "Infinity"
            else:
                print int(l_new_short[stop])
        else:
            print l_shortest_distances[stop]

    query_stop = time.time()
    print "Total query time = " + str(query_stop - query_start)

    global_stop = time.time()
    print "Total time = " + str(global_stop - global_start)