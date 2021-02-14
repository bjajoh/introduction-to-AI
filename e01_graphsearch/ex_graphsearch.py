"""
For all exercise you need a graph structure. We use a very simple
representation for that: A dictionary.
Assume you have a graph with four node connect as depicted in the next lines:

   B
 /  \
A---C
 \
  D

The python representation would look like this:

weighted_graph = {'A': {'B': 20, 'C': 30, 'D': 25},
                  'B': {'A': 20, 'C': 20},
                  'C': {'A': 30, 'B': 20},
                  'D': {'A': 25}
                  }

With this implementation you can iterate over all nodes of the graph like
this:

for node in graph:
    print("{} is a node.".format(node))

Or over neighbors of a given node like this:

for neighbor in graph['B']:
    print("{} is neighbor of B".format(neighbor))

You can get the distance with:

for neighbor in graph['A']:
    print("{} is {} miles away from A.".format(neighbor, graph['A'][neighbor]))

As nodes use the Node datastructure below.

As a fringe use python's Queue, LifoQueue and the NodePriorityQueue we supplied
below. Note that you have to fill in the calculation of the priority.
"""

from data import graph, sbahn, coordinates
from Queue import Queue, LifoQueue, PriorityQueue
import ex_graphsearch as ex



class FailureException(Exception):
    """
    A exception that is raised when a failure occurs
    """
    pass


class CutoffException(Exception):
    """
    An exception, that is raised when a cutoff appears
    """
    pass


class Node(object):
    """
    A very simple node data structure as in the slides. Use this structure to
    implement the tree search.
    """
    def __init__(self, state, parent, path_cost, depth):
        self.state = state

        self.parent = parent
        self.children = []
        self.path_cost = path_cost
        self.depth = depth

        if self.parent is not None:
            self.parent.children.append(self)

    def __str__(self):
        string = "'" + self.state + "'"
        if self.parent is not None:
            string = string + ", " + str(self.parent)
        return string


class NodePriorityQueue(object):
    """
    A PriorityQueue that uses the path_cost as priority. When a heuristic and
    a goal state is given the heuristic cost from each node to the goal state
    is added to the priority.
    """
    def __init__(self, heuristic=None, goals=[None]):
        self.visited = []
        self.queue = PriorityQueue()
        self.goals = goals

        if heuristic is not None:
            self.heuristic = heuristic
        else:
            # if no heuristic is given use a constant 0 heuristic
            self.heuristic = lambda u, v: 0

    def put(self, node):
        """
        This function should put a node with the correct priority into the
        internal priority queue. You don't have to take care to adjust
        earlier added nodes. Just put the right priority here
        """
        #######################################################################
        #                                                                     #
        #                                                                     #
        #        A D J U S T   T H E   F O L L O W I N G   L I N E !          #
        #           remember that there might be multiple goals               #
        #                                                                     #
        #                                                                     #
        #######################################################################
        priority = node.path_cost
        # this is used just for the A* search, oder?
        # Yes :)
        self.queue.put((priority, node))

    def get(self):
        """
        This function takes care that already visited nodes are not visited
        again.
        """
        _, node = self.queue.get()
        while node.state in self.visited:
            _, node = self.queue.get()

        self.visited.append(node.state)
        return node

    def empty(self):
        """
        empty() returns true if the queue is empty or has only already
        visited nodes in it.
        """
        if self.queue.empty():
            return True
        priority, node = self.queue.get()
        while node.state in self.visited:
            if self.queue.empty():
                return True
            priority, node = self.queue.get()

        self.queue.put((priority, node))
        return False


def expand(node, graph):
    """
    Implement the expand function for a graph problem. Use the Node class
    we provided. Actions are the vertices of the graph, i.e.:

    # for action in graph[current_node]:
        # do something

    would be a useful construct.
    The step_costs are also in the graph and are the vertex weights:

    step_cost = graph[current_node][next_node]

    :param node:
    :param graph: The graph, that defines the problem
    :return: A list of all successors
    """
    successors = []

    for action in graph[node.state]:
        step_cost = graph[node.state][action]
        successors.append(Node(action, node, node.path_cost+step_cost, node.depth+1))

    return successors

    pass


def breadth_first_search(graph, start, goals):
    """
    Compute a breadth first search on the given graph. Use the Node class
    we provided. It might be useful to implement the generic tree search
    function first and then use different implementations for the fringe.

    :param graph: The graph to run the BFS on
    :param start: The start state
    :param goals: A list of goal states that should be reached (one of them)
    :return: a tuple with a the found node as first entry and the
            fringe as the second entry
    """
    
    fringe = Queue()
    visited = set()
    fringe.put(Node(start, None, 0, 0))
    
    while not fringe.empty():

        current_node = fringe.get()
        if current_node.state in goals:
            return (current_node, fringe)

        else:
            visited.add(current_node)
            for next_node in expand(current_node, graph):
                if next_node not in visited:
                    fringe.put(next_node)



def uniform_cost_search(graph, start, goals):
    """
    Compute a uniform cost search on the given graph. Use the Node class
    we provided. It might be useful to implement the generic tree search
    function first and then use different implementations for the fringe.

    :param graph: The graph to run the uniform-cost search on
    :param start: The start state
    :param goals: A list of goal states that should be reached (one of them)
    :return: a tuple with a the found node as first entry and the
            fringe as the second entry
    """
    fringe = NodePriorityQueue()
    visited = set()
    fringe.put(Node(start, None, 0, 0))

    while not fringe.empty():
        current_node = fringe.get()
        if current_node.state in goals:
            return (current_node, fringe)
        
        else:
            visited.add(current_node)
            for next_node in expand(current_node, graph):
                if next_node not in visited:
                    fringe.put(next_node)


def depth_limited_search(graph, start, goals, limit):
    """
    Compute a depth-limited search on the given graph. Use the Node class
    we provided. Use the recursive DLS variant.
    Raise an CutoffException if a you did not find the goal because of the
    limit.

    :param graph: The graph to run the DLS on
    :param start: The start state
    :param goals: A list of goal states that should be reached (one of them)
    :param limit: The depth limit
    :return: the found node
    """

    visited = set()
    current_node = recursive_dls(graph, Node(start, None, 0,0), goals, limit, visited)
    
    if current_node.state is "cutoff":
        raise CutoffException()
    elif current_node.state in goals:
        return current_node
    else:
        raise FailureException()
        

def recursive_dls(graph, current_node, goals, limit, visited):
    cutoff_occured = False
    if current_node.state in goals:
        return current_node

    elif current_node.depth == limit:
        return Node("cutoff", None, 0,0)

    else:
        visited.add(current_node)
        for successor in expand(current_node, graph):
            if successor not in visited:
                next_node = recursive_dls(graph, successor, goals, limit, visited)
                if next_node.state is "cutoff":
                    cutoff_occured = True
                elif next_node.state is not "failure":
                    return next_node
    if cutoff_occured:
        return Node("cutoff", None, 0, 0)
    else:
        return Node("failure", None, 0, 0)


def iterative_deepening_search(graph, start, goals):
    """
    Compute a iterative deepening search on the given graph. Use the Node
    class we provided.

    :param graph: The graph to run the iterative deepening search on
    :param start: The start state
    :param goals: A list of goal states that should be reached (one of them)
    :return: the found node
    """

    current_depth = 0
    while True:
        try:
            node = depth_limited_search(graph, start, goals, current_depth)
            return node
        except FailureException:
            return
        except CutoffException:
            current_depth +=1
            continue



def a_star_search(graph, start, goals, heuristic):
    """
    We cover A star in the next lecture. You might want to wait to
    implement this.
    Compute a A star search on the given graph. Use the Node class we
    provided. It might be useful to implement the generic tree search
    function first and then use different implementations for the fringe.

    :param graph: The graph to run A star on
    :param start: The start state
    :param goals: A list of goal states that should be reached (one of them)
    :param heuristic: A function that returns a heuristic cost value
                      for two given nodes. E.g. heuristic('A', 'B')
                      returns a float
    :return: a tuple with the found node as first entry and the
            fringe as the second entry
    """
    fringe = NodePriorityQueue()
    fringe.put(Node(start, None, 0,0))
    
    while not fringe.empty():

        current_node = fringe.get()
        if current_node.state in goals:
            return (current_node, fringe)

        else:
            for next_node in expand(current_node, graph):
                h_small = float('inf')

                for goal in goals:
                    h = heuristic(next_node.state, goal)
                    if h_small > h:
                        h_small = h
                next_node.path_cost = h_small + next_node.path_cost
                fringe.put(next_node)


if __name__ == '__main__':
    node, fringe = breadth_first_search(graph, 'D', ['C'])
    print node
