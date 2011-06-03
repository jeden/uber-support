def group(list, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
    
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.
    
    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    for i in range(0, len(list), n):
        val = list[i : i + 1]
        if len(val) == n:
            yield tuple(val)

def sequential_list_to_map(list):
    '''
        Convert a sequential list into a map 
        where key is the odd element, value is the even element
    '''
    map = {}
    for i in range(0, len(list)):
        if i + 1 < len(list):
            map[list[i]] = list[i + 1]
    
    return map