import heapq
from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path

def ucs(start, dirties, cols, rows):
    dirties = normalize_dirties(dirties)
    
    # kiểm tra vị trí đang đứng có phải ô bẩn hay không
    dirties = tuple(d for d in dirties if d != start)

    # khởi tạo trạng thái ban đầu 
    start_state = (start, dirties)
    start_node = Node(start_state, cost=0)

    frontier = []

    explored = set()
    best_cost = {start_state : 0}

    heapq.heappush(frontier, (0, 0, start_node)) # priority queue lưu (cost, counter, node) 
    # counter để tránh lỗi khi cost bằng nhau
    counter = 0

    yield {
        "current": None,
        "frontier": [start_node],
        "explored": explored,
        "log": f"UCS khởi tạo tại {start}, còn {len(dirties)} rác, cost=0"
    }

    while frontier:
        cost, _, node = heapq.heappop(frontier)

        if node.state in explored:
            continue

        yield {
            "current": node,
            "frontier": [n for c, i, n in frontier],
            "explored": explored,
            "log": f"Lấy {node.state[0]} ra khỏi Priority Queue, cost={cost}, rác còn: {len(node.state[1])}"
        }

        if len(node.state[1]) == 0:
            yield {
                "current": node,
                "frontier": [n for c, i, n in frontier],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(node),
                "log": f"SÀN NHÀ ĐÃ SẠCH! Tổng cost = {cost}"
            }
            return

        explored.add(node.state)

        for neighbor_state in get_neighbors(node.state, cols, rows):
            step_cost = 1
            new_cost = cost + step_cost

            if neighbor_state in explored:
                continue

            if neighbor_state not in best_cost or new_cost < best_cost[neighbor_state]:
                best_cost[neighbor_state] = new_cost
                child = Node(neighbor_state, node, cost=new_cost)

                counter += 1
                heapq.heappush(frontier, (new_cost, counter, child))

                yield {
                    "current": node,
                    "frontier": [n for c, i, n in frontier],
                    "explored": explored,
                    "log": f"Sinh node {neighbor_state[0]}, cost={new_cost}, rác còn: {len(neighbor_state[1])}"
                }

    yield {
        "current": None,
        "frontier": [],
        "explored": explored,
        "done": True,
        "path": [],
        "log": "Không tìm thấy đường đi"
    }
