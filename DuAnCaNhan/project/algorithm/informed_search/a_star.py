import heapq
from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def A_star(start, dirties, cols, rows):
    dirties = normalize_dirties(dirties)
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    start_node = Node(start_state, cost=0)

    frontier = []
    explored = set()
    best_cost = {start_state: 0}

    counter = 0
    start_h = h(start, dirties)
    heapq.heappush(frontier, (start_h, 0, counter, start_node))
    # frontier lưu: (f, g, counter, node)

    while frontier:
        f_cost, g_cost, _, node = heapq.heappop(frontier)
        current_state = node.state

        if current_state in explored:
            continue

        if len(node.state[1]) == 0:
            yield {           
                "current": node,
                "frontier": [n for f, g, c, n in frontier],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(node),
                "log": f"SÀN NHÀ ĐÃ SẠCH! Tổng cost = {f_cost}"
            }
            return

        explored.add(current_state)

        for next_state in get_neighbors(current_state, cols, rows):
            if next_state in explored:
                continue

            new_g_cost = g_cost + 1
            new_h_cost = h(next_state[0], next_state[1])
            new_f_cost = new_g_cost + new_h_cost

            if next_state not in best_cost or new_g_cost < best_cost[next_state]:
                best_cost[next_state] = new_g_cost

                child = Node(next_state, node, cost=new_g_cost)
                counter += 1
                heapq.heappush(frontier, (new_f_cost, new_g_cost, counter, child))

                yield {
                    "current": node,
                    "frontier": [n for f, g, c, n in frontier],
                    "explored": explored,
                    "log": f"Sinh node {next_state[0]}, g={new_g_cost}, h={new_h_cost}, f={new_f_cost}, rác còn: {len(next_state[1])}"
                }

    yield {
        "current": None,
        "frontier": [],
        "explored": explored,
        "done": True,
        "path": [],
        "log": "Không tìm thấy đường đi"
    }
