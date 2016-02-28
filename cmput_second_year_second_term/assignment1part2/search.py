from graph import Graph # the graph.py module from Lecture 4
from queue import deque

def breadth_first_search(g, v):
    '''Return a dictionary whose keys
    are all nodes reachable from v.

    The dictionary is the search tree
    obtained through a breadth-first search,
    so the paths are shortest paths.

    Assumption: g.is_vertex(v) -> True

    Running time: O(m) where m = num edges
    '''
    
    reached = {v:v}
    todo = deque([v])

    # O(min(n,m)) iterations
    # Each iteration processes one node in the todo list,
    # but can only process nodes that are reachable from v.
    while todo:
        curr = todo.popleft()

        # Number of iterations over the ENTIRE algorithm
        # is at most m: each node has its neighbours
        # expanded at most once.
        for succ in g.neighbours(curr):
            if succ not in reached:
                reached[succ] = curr
                todo.append(succ)

    return reached

def depth_first_search(g, v):
    '''Return a dictionary whose keys
    are all nodes reachable from v.

    The dictionary is the search tree
    obtained through a depth-first search.

    Assumption: g.is_vertex(v) -> True

    Running time: O(m), m = # edges
    '''

    reached = {}
    
    def do_dfs(curr, prev):
        if curr in reached:
            return
        reached[curr] = prev
        for succ in g.neighbours(curr):
            do_dfs(succ, curr)

    do_dfs(v, v)

    return reached


def dijkstra(g, v, cost):
    '''
    Find and return the search tree
    obtained by performing Dijkstra's search
    on a graph with edge costs.
    
    Assumption: g.is_vertex(v) -> True
    cost(u,w) returns the cost of an edge
    (u,w) in the graph.

    WARNING: We did not have time to test this code
    in class.

    Running time: O(m^2)
    '''
    
    reached = {}

    # just a bandage for now, we will use
    # a better data structure later to get
    # better running time
    runners = {(0, v, v)}

    # num iterations <= num edges + 1
    # i.e. O(m)
    while runners:
        # O(m) time per extraction
        # WARNING: if there are multiple "runners"
        # with the same minimum time, then this
        # will compare the second elements of the tuple.
        # Our final, more efficient implementation
        # will avoid this.
        (time, goal, start) = min(runners)
        runners.remove((time, goal, start))

        if goal in reached:
            continue

        reached[goal] = (start, time)

        # O(1) time per insertion, at most m insertions
        # throughout the entire algorithm
        for succ in g.neighbours(goal):
            set.add((time + cost(goal, succ), succ, goal))

    return reached
