import random
from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def random_restart_hill_climbing(start, dirties, cols, rows, max_restarts=100):
    dirties = normalize_dirties(dirties)
    initial_dirties = tuple(d for d in dirties if d != start)

    best_stuck_node = None

    for i in range(max_restarts):
        if i == 0:
            current_start = start
            current_dirties = initial_dirties
        else:
            current_start = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            current_dirties = tuple(d for d in dirties if d != current_start)

        start_state = (current_start, current_dirties)
        current_node = Node(start_state, cost=0)
        explored = set()

        yield {
            "current": current_node,
            "frontier": [],
            "explored": explored,
            "log": f"Restart {i}: Khởi tạo tại {current_start}"
        }

        while True:
            current_state = current_node.state
            explored.add(current_state)

            current_h = h(current_state[0], current_state[1])

            if len(current_state[1]) == 0:
                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "done": True,
                    "path": reconstruct_path(current_node),
                    "log": "SÀN NHÀ ĐÃ SẠCH!"
                }
                return

            children = []
            for next_state in get_neighbors(current_state, cols, rows):
                if next_state in explored:
                    continue
                child = Node(next_state, current_node, cost=current_node.cost + 1)
                child_h = h(next_state[0], next_state[1])
                children.append((child, child_h))

            if not children:
                # Bị kẹt hoàn toàn, lưu lại node nếu là lần cuối, sau đó restart
                best_stuck_node = current_node
                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "log": "Bị kẹt không có đường đi, chuẩn bị restart..."
                }
                break

            best_child, best_h = min(children, key=lambda x: x[1])
            if best_h < current_h:
                current_node = best_child
            else:
                # Gặp cực tiểu cục bộ
                best_stuck_node = current_node
                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "log": "Gặp cực tiểu cục bộ, chuẩn bị restart..."
                }
                break

    # Nếu thử hết max_restarts lần mà vẫn không tìm được goal
    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "done": True,
        "path": reconstruct_path(best_stuck_node) if best_stuck_node else [],
        "log": f"Thất bại sau {max_restarts} lần restart."
    }
