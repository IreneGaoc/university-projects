def is_walk (graph, walk):
    '''Given a graph, checks if all the elements of 'walk' are vertices
    and there are edges between consecutive elements.'''
    if walk and not graph.is_vertex(walk[0]):
        return False
    for i in range(1, len(walk)):
        if not graph.is_edge(walk[i-1], walk[i]):
            return False
    return True


def is_path (graph, walk):
    '''Given a graph, check if the list 'walk' is actually a path,
    i.e. that it is a walk and has no repeated vertices.'''
    return is_walk(graph, walk) and len(set(walk)) == len(walk)
