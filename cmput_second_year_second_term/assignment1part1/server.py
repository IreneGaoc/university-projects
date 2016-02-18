from heap import MinHeap
from graph import WeightedGraph
import sys
import math


def compute_distance(u,v):
    '''
    Computes and returns the line distance between u and v.
    Args:
    u, v: The ids for two vertices that are the start and
    end of a valid edge in the graph.
    Returns:
    numeric value: the distance between the two vertices.
    '''

    distance = math.sqrt((u[0]-v[0])**2+(u[1]-v[1])**2)**1/2
    return int(distance)
def cost_distance(u,v):
    '''
    Computes and returns the straight-line distance between the two vertices u and v.
    Args:
    u, v: The ids for two vertices that are the start and
    end of a valid edge in the graph.
    Returns:
    numeric value: the distance between the two vertices.
    '''
    start = vertecies[u]
    end = vertecies[v]
    return compute_distance(start,end)
def least_cost_path(graph,start,dest,cost):
    """Find and return the least cost path in graph from start vertex to dest vertex.
    Efficiency: If E is the number of edges, the run-time is
      O( E log(E) ).
    Args:
      graph (Graph): The digraph defining the edges between the
        vertices.
      start: The vertex where the path starts. It is assumed
        that start is a vertex of graph.
      dest:  The vertex where the path ends. It is assumed
        that start is a vertex of graph.
      cost:  A function, taking the two vertices of an edge as
        parameters and returning the cost of the edge. For its
        interface, see the definition of cost_distance.
    Returns:
      list: A potentially empty list (if no path can be found) of
        the vertices in the graph. If there was a path, the first
        vertex is always start, the last is always dest in the list.
        Any two consecutive vertices correspond to some
        edge in graph.
    >>> graph = Graph({1,2,3,4,5,6}, [(1,2), (1,3), (1,6), (2,1),
            (2,3), (2,4), (3,1), (3,2), (3,4), (3,6), (4,2), (4,3),
            (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)])
    >>> weights = {(1,2): 7, (1,3):9, (1,6):14, (2,1):7, (2,3):10,
            (2,4):15, (3,1):9, (3,2):10, (3,4):11, (3,6):2,
            (4,2):15, (4,3):11, (4,5):6, (5,4):6, (5,6):9, (6,1):14,
            (6,3):2, (6,5):9}
    >>> cost = lambda u, v: weights.get((u, v), float("inf"))
    >>> least_cost_path(graph, 1,5, cost)
    [1, 3, 6, 5]
    """
    reached = {}
    runners = MinHeap()
    distances = {}
    # add the starting vertices to the runners
    runners.add( 0,(start,start))

    while runners and dest not in reached:
        (val,(prev, goal)) = runners.pop_min()
        #print('[',prev,goal,val,']')
        if goal in reached:
            continue

        if goal not in reached:
            reached[goal] = prev
            distances[goal] = val
            # check the neighbours and add to the runners
            for succ in graph.neighbours(goal):
                runners.add( val + cost(goal,succ),(goal, succ))

            if goal == dest:
                break

    # return empty list if dest cannot be reached
    if dest not in reached:
        return []

    path = []
    vertice = dest
    while True:
        path.append(vertice)
        #print(path)
        if path[-1] == start:
            break
        vertice = reached[vertice]

    # reverse list and output it
    path.reverse()
    return path


def nearest_vertex(lat, lon):

    coo = (lat, lon)
    nearest = min(vertecies.items(), key=lambda x: compute_distance(coo, x[1]))

    return nearest[0]



def read_city_graph(filename):
    f = open(filename)
    g = WeightedGraph()
    global vertecies
    vertecies = {}
    global edges
    edges = {}

    line = f.readline()
    while line:
        fields = line.split(",")

        if fields[0] == "V":
            v = int(fields[1])
            lat = float(fields[2])
            lon = float(fields[3])
            g.add_vertex(v)
            vertecies[v] = (int(lat * 100000), int(lon * 100000) )
        elif fields[0] == "E":
            e = (int(fields[1]), int(fields[2]))
            g.add_edge(int(fields[1]),int(fields[2]))
            edges[e] = {"street": fields[3]}
        line = f.readline()

    return g


def read_output(in_put, out_put):

    filename = "edmonton-roads-2.0.1.txt"  # name of file
    rgraph = read_city_graph(filename)  # read data
    while True:

        lines = " "
        while lines[0] != 'R' or len(lines) != 5:
            lines = in_put.readline()
            lines = lines.strip('\r\n').split(' ')

        try:
            start = nearest_vertex(int(lines[1]), int(lines[2]))
            dest = nearest_vertex(int(lines[3]), int(lines[4]))
        except:
            print('input invaild')
            continue
        # least_cost_path from start to end
        path = least_cost_path(rgraph, start , dest, cost_distance)


        if (len(path)!=0):
            #print the number of points in path
            print('N', len(path), '\r\n', file=out_put)
        else:
            #When there is no path from the start to the end vertex nearest to the
            #start and end points sent to the server, the server should return an empty
            #path to the Arduino by sending the error message

            print("N 0")
            continue
        for node in path:

            ans = in_put.readline().rstrip('\r\n')
            while ans != 'A':
                ans = in_put.readline().rstrip('\r\n')
            print('W', vertecies[node][0], vertecies[node][1], '\r\n', file=out_put)
        ans = in_put.readline().rstrip('\r\n')
        while ans != 'A':
            ans = in_put.readline().rstrip('\r\n')
        print('E\r\n', file=out_put)





if __name__ == "__main__":
    read_output(sys.stdin, sys.stdout)
