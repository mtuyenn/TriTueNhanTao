import heapq
from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def Greedy_Search(start, dirties, cols, rows):
    dirties = normalize_dirties(dirties)
    # nếu máy hút bụi bắt đầu ở chỗ có rác
    dirties = tuple(d for d in dirties if d != start)
    
    start_state = (start, dirties)
    start_node = Node(start_state)
    
    frontier = []
    explored = set()

    counter = 0
    heapq.heappush(frontier, (h(start, dirties), counter, start_node))

    while frontier:
        heuristic, _, node = heapq.heappop(frontier)
        current_state = node.state

        if current_state in explored:
            continue

        # nếu rác bằng 0 => sàn đã sạch
        if len(node.state[1]) == 0:
            yield {
                "current": node,
                "frontier": [n for h_val, i, n in frontier],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(node),
                "log": f"SÀN NHÀ ĐÃ SẠCH!"
            }
            return

        explored.add(node.state)

        # sinh node tiếp theo 
        for next_state in get_neighbors(current_state, cols, rows):

            heuristic_cost = h(next_state[0], next_state[1]) if next_state[1] else 0

            child = Node(next_state, node, cost = 0)
            counter += 1
            heapq.heappush(frontier, (heuristic_cost, counter, child))

            yield {
                "current": node,
                "frontier": [n for c, i, n in frontier],
                "explored": explored,
                "log": f"Sinh node {next_state[0]}, heuristic={heuristic_cost}, rác còn: {len(next_state[1])}"
            }

    yield {
        "current": None,
        "frontier": [],
        "explored": explored,
        "done": True,
        "path": [],
        "log": "Không tìm thấy đường đi"
    }
