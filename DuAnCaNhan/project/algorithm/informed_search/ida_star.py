from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h, FOUND, INF

def IDA_start(start, dirties, cols, rows, limit=None):
    dirties = normalize_dirties(dirties)
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    start_node = Node(start_state, cost=0)

    limit = h(start, dirties)

    while True:
        result = yield from IDA_dfs(start_node, 0, limit, cols, rows, set())

        if result == FOUND:
            return

        if result == INF:
            yield {
                "current": None,
                "frontier": [],
                "explored": set(),
                "done": True,
                "path": [],
                "log": "Không tìm thấy đường đi"
            }
            return

        limit = result


def IDA_dfs(node, g_cost, limit, cols, rows, visited):
    f_cost = g_cost + h(node.state[0], node.state[1])

    if f_cost > limit:
        return f_cost

    yield {
        "current": node,
        "frontier": [],
        "explored": visited,
        "limit": limit,
        "log": f"IDA*: robot ở {node.state[0]}, g={g_cost}, h={h(node.state[0], node.state[1])}, f={f_cost}, limit={limit}, rác còn={len(node.state[1])}"
    }

    if len(node.state[1]) == 0:
        yield {
            "current": node,
            "frontier": [],
            "explored": visited,
            "done": True,
            "path": reconstruct_path(node),
            "log": f"SÀN NHÀ ĐÃ SẠCH! Tổng cost = {g_cost}"
        }
        return FOUND

    min_next_limit = float("inf")
    visited.add(node.state)

    for next_state in get_neighbors(node.state, cols, rows):
        if next_state in visited:
            continue

        child = Node(next_state, node, cost=g_cost + 1)
        result = yield from IDA_dfs(child, g_cost + 1, limit, cols, rows, visited)

        if result == FOUND:
            return FOUND

        if result < min_next_limit:
            min_next_limit = result

    visited.remove(node.state)

    return min_next_limit
