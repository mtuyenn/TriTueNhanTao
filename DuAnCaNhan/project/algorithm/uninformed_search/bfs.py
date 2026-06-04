from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, is_in_frontier

# ================= BFS / DFS kiểm tra goal sau khi POP =================
def search_v1(start_pos, dirties, cols, rows, use_queue=True):
    dirties = normalize_dirties(dirties)
    
    # Nếu vị trí bắt đầu có rác thì dọn luôn
    dirties = tuple(d for d in dirties if d != start_pos)

    start_state = (start_pos, dirties)
    start_node = Node(start_state)

    frontier = [start_node]
    explored = set()

    yield {
        "current": None,
        "frontier": frontier,
        "explored": explored,
        "log": f"Khởi tạo robot tại {start_pos}, còn {len(dirties)} rác"
    }

    while frontier:
        node = frontier.pop(0) if use_queue else frontier.pop()

        yield {
            "current": node,
            "frontier": frontier,
            "explored": explored,
            "log": f"Lấy {node.state[0]} ra khỏi {'Queue' if use_queue else 'Stack'}, rác còn: {len(node.state[1])}"
        }

        if len(node.state[1]) == 0:
            yield {
                "current": node,
                "frontier": frontier,
                "explored": explored,
                "log": "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!",
                "done": True,
                "path": reconstruct_path(node)
            }
            return

        explored.add(node.state)

        for neighbor_state in get_neighbors(node.state, cols, rows):
            if neighbor_state in explored or is_in_frontier(neighbor_state, frontier):
                continue

            child = Node(neighbor_state, node)
            frontier.append(child)

            yield {
                "current": node,
                "frontier": frontier,
                "explored": explored,
                "log": f"Sinh node {neighbor_state[0]}, rác còn: {len(neighbor_state[1])}"
            }

    yield {
        "current": None,
        "frontier": frontier,
        "explored": explored,
        "done": True,
        "path": [],
        "log": "Không tìm thấy đường đi"
    }


# ================= BFS / DFS kiểm tra goal trước khi PUSH =================
def search_v2(start_pos, dirties, cols, rows, use_queue=True):
    dirties = normalize_dirties(dirties)

    # Nếu vị trí bắt đầu có rác thì dọn luôn
    dirties = tuple(d for d in dirties if d != start_pos)

    start_state = (start_pos, dirties)
    start_node = Node(start_state)

    if len(dirties) == 0:
        yield {
            "current": start_node,
            "frontier": [],
            "explored": set(),
            "done": True,
            "path": reconstruct_path(start_node),
            "log": "Sàn nhà đã sạch từ đầu!"
        }
        return

    frontier = [start_node]
    explored = set()
    reached = {start_state}

    yield {
        "current": None,
        "frontier": frontier,
        "explored": explored,
        "log": f"Khởi tạo robot tại {start_pos}, còn {len(dirties)} rác"
    }

    while frontier:
        node = frontier.pop(0) if use_queue else frontier.pop()
        explored.add(node.state)

        yield {
            "current": node,
            "frontier": frontier,
            "explored": explored,
            "log": f"Lấy {node.state[0]} ra khỏi {'Queue' if use_queue else 'Stack'}, rác còn: {len(node.state[1])}"
        }

        for neighbor_state in get_neighbors(node.state, cols, rows):
            if neighbor_state in reached:
                continue

            child = Node(neighbor_state, node)

            yield {
                "current": node,
                "frontier": frontier,
                "explored": explored,
                "log": f"Sinh node {neighbor_state[0]}, rác còn: {len(neighbor_state[1])}"
            }

            if len(neighbor_state[1]) == 0:
                yield {
                    "current": child,
                    "frontier": frontier,
                    "explored": explored,
                    "done": True,
                    "path": reconstruct_path(child),
                    "log": "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!"
                }
                return

            reached.add(neighbor_state)
            frontier.append(child)

    yield {
        "current": None,
        "frontier": frontier,
        "explored": explored,
        "done": True,
        "path": [],
        "log": "Không tìm thấy đường đi"
    }


def bfs1(start, dirties, cols, rows):
    return search_v1(start, dirties, cols, rows, use_queue=True)


def bfs2(start, dirties, cols, rows):
    return search_v2(start, dirties, cols, rows, use_queue=True)
