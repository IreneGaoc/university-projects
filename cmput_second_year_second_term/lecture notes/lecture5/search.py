
from graph import Graph
from queue import deque

def basic_search(g, v):
    '''Return a dictionary whose keys
    are all nodes reachable from v.
    The dictionary is the search tree.

    Assumption: g.is_vertex(v) -> True

    Running time: O(n^3)
    '''

    reached = {v:v}

    #O(n^2) time
    def find_new_node():
        #O(n) iterations
        for u in reached:
            #O(n) iterations
            for w in g.neighbours(u):
                if w not in reached:
                    return (u,w)
        return (None, None)

    # number of iterations <= n
    # n == number of vertices of G
    while True:
        old_size = len(reached)

        (prev, found) = find_new_node()

        if found is None and prev is None:
             return reached
        else:
            reached[found] = prev


def breadth_first_search(g, v):
    '''Return a dictionary whose keys
    are all nodes reachable from v.
    The dictionary is the search tree.

    Assumption: g.is_vertex(v) -> True

    Running time: O(m)
    m = # edges
    '''

    reached = {v:v}
    todo = deque([v])

    #O(m) times:
    # number of nodes that go through the
    # todo list is at most (# edges + 1)
    while todo:
        curr = todo.popleft()

        # num iterations = len(g.neighbours)
        # and each vertex is in the todo list at most
        # once so, total number of iterations over the
        # ENTIRE algorithm is at most the total number
        # of neighbours of all nodes
        # i.e. m (number of edges)
        for succ in g.neighbours(curr):
            if succ not in reached:
                reached[succ] = curr
                todo.append(succ)

    return reached

def basic_search_test(g, v, expected):
    reached = basic_search(g, v)
    if set(reached.keys()) != expected:
        print("basic_search_test failure")
        print(" Expected: " + str(expected))
        print(" Got:      " + str(set(reached.keys())))

def breadth_first_search_test(g, v, expected):
    reached = breadth_first_search(g, v)
    if set(reached.keys()) != expected:
        print("breadth_first_search_test failure")
        print(" Expected: " + str(expected))
        print(" Got:      " + str(set(reached.keys())))

# will only run if invoked from the command line
# i.e. python3 search.py
if __name__ == "__main__":

    graph1 = Graph()
    for v in range(5):
        graph1.add_vertex(v)
    edges = [ (0, 1), (0, 3), (3, 4), (1, 4), (2, 1) ]
    for e in edges:
        graph1.add_edge(e[0], e[1])

    print(basic_search(graph1, 0))

    breadth_first_search_test(graph1, 0, {0, 1, 3, 4})
    breadth_first_search_test(graph1, 1, {1, 4})
    breadth_first_search_test(graph1, 2, {2, 1, 4})
    breadth_first_search_test(graph1, 3, {3, 4})
    breadth_first_search_test(graph1, 4, {4})

    path_len = 1000000
    path = Graph()
    for v in range(path_len):
        path.add_vertex(v)
    for i in range(path_len-1):
        path.add_edge(i, i+1)

    print("Starting search...")
    breadth_first_search_test(path, 0, set(range(path_len)))
    print("Done search!")
