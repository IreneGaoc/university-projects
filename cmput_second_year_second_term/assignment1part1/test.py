from server import *
from graph import UndirectedGraph # assumes we use the graph module from class
#test10(29577354,29577354)

rgraph = read_city_graph("edmonton-roads-2.0.1.txt" )  # read data
cost_distance(29577354,29577354)
graph = UndirectedGraph({1,2,3,4,5,6}, [(1,2), (1,3), (1,6), (2,1),
            (2,3), (2,4), (3,1), (3,2), (3,4), (3,6), (4,2), (4,3),
            (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)])
weights = {(1,2): 7, (1,3):9, (1,6):14, (2,1):7, (2,3):10,
            (2,4):15, (3,1):9, (3,2):10, (3,4):11, (3,6):2,
            (4,2):15, (4,3):11, (4,5):6, (5,4):6, (5,6):9, (6,1):14,
            (6,3):2, (6,5):9}
cost = lambda u,v : weights.get((u,v), float("inf"))

print(least_cost_path(graph, 1,5, cost))
