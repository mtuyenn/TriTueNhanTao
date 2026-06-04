from .bfs import search_v1, search_v2

def dfs1(start, dirties, cols, rows):
    return search_v1(start, dirties, cols, rows, use_queue=False)

def dfs2(start, dirties, cols, rows):
    return search_v2(start, dirties, cols, rows, use_queue=False)
