from heap import MinHeap
from graph import WeightedGraph
import sys
import time
import math
import textserial
import argparse

def parse_args():
    """
    Parses arguments for this program.

    Returns:
    An object with the following attributes:
     serialport (str): what is after -s or --serial on the command line
    """
    # try to automatically find the port
    port = textserial.get_port()
    if port==None:
        port = "0"

    parser = argparse.ArgumentParser(
          description='Serial port communication testing program.'
        , epilog = 'If the port is 0, stdin/stdout are used.\n'
        )
    parser.add_argument('-s', '--serial',
                        help='path to serial port '
                             '(default value: "%s")' % port,
                        dest='serialport',
                        default=port)

    return parser.parse_args()


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
    start = vertices[u]
    end = vertices[v]
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
    nearest = min(vertices.items(), key=lambda x: compute_distance(coo, x[1]))

    return nearest[0]



def read_city_graph(filename):
    f = open(filename)
    g = WeightedGraph()
    global vertices
    vertices = {}
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
            vertices[v] = (int(lat * 100000), int(lon * 100000) )
        elif fields[0] == "E":
            e = (int(fields[1]), int(fields[2]))
            g.add_edge(int(fields[1]),int(fields[2]))
            edges[e] = {"street": fields[3]}
        line = f.readline()

    return g

def read_output():
	filename = "edmonton-roads-2.0.1.txt"
	rgraph = read_city_graph(filename)
	
	'''
	wait for pathlen request
	get request
	get pathlen
	send pathlen to client
	
	wait for waypoints request
	send waypoints
	send 'end' acknowledgement
	'''
	
	# wait for pathlen request
	while 1:
		msg = 'sending'
		print("srv: ", msg)
		print(msg, file=srv)
		
		# get request
		check_cli = srv.readline().strip()
		print("srv: ", check_cli)
		if check_cli == "pathlen request":
			print("check msg: ", check_cli)
			#print("srv: request received from arduino")
			break
	
	print("server ready", file=srv)
	check_clireq = srv.readline().strip()
	check_clireq = check_clireq.split(" ")
	print("s: ", check_clireq)
	if check_clireq[0] == "R":
		print("srv: got request!")
		start_ = nearest_vertex(int(check_clireq[1]), int(check_clireq[2]))
		dest = nearest_vertex(int(check_clireq[3]), int(check_clireq[4]))

	else:
		read_output()

	path = least_cost_path(rgraph, start_, dest, cost_distance)
	print("pathlen: ")
	
	# send pathlen to client
	print(path)
	
	timeout = time.time() + 1
	while 1:
		print(len(path), file=srv)
		check_client = srv.readline().strip()
		if check_client == "request timeout" or time.time() > timeout or len(path) == 0 or len(path) > 200:
			read_output()
		else:
			print("N ", check_client)
			break
	
	# wait for waypoints request
	while 1:
		msg = 'sending..'
		print("srvr: ", msg)
		checkcli = srv.readline().strip()
		print("srv got: ", checkcli)
		if checkcli == "request waypoints":
			break
		
	# after waiting, get the request
	for i,node in enumerate(path):
		print("server ready", file=srv)
		
		print('W', vertices[node][0], vertices[node][1], '\r\n')
		print('W', vertices[node][0], vertices[node][1], '\r\n', file=srv)
		
		
		timeout = time.time() + 1
		while 1:
			if time.time() > timeout:
				read_output()
				
			check_ack = srv.readline().strip()
			if check_ack == 'A':
				print("check ack: ", check_ack)
				#check_ack = srv.readline().strip()
				#print("next waypoint..")
				break
				
			if time.time() > timeout or check_ack == "request timeout" or len(path) == 0 or len(path) > 200:
				#timeout
				read_output()
							
	print("server ready", file=srv)
	print('E\r\n')
	print('E\r\n', file=srv)
	print("waypoints exchange finished")
	
	while 1:
		client = srv.readline().strip()
		if client == "Done with communication":
			print("srv: " , client)
			break
	
if __name__ == "__main__":
    args = parse_args()

    if args.serialport!="0":
        print("Opening serial port: %s" % args.serialport)
        baudrate = 9600 # [bit/seconds] 115200 also works
        with textserial.TextSerial(args.serialport,baudrate,newline=None) as srv:
            while 1:
                read_output()
    else:
        print("No serial port")
        read_output()
