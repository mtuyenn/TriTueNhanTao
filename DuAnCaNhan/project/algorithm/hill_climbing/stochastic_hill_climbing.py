import random
from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def stochastic_hill_climbing(start, dirties, cols, rows):
    dirties = normalize_dirties(dirties)
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    current_node = Node(start_state, cost=0)

    explored = set()

    yield {
        "current": current_node,
        "frontier": [],
        "explored": explored,
        "log": f"Stochastic Hill Climbing khởi tạo tại {start}, rác còn: {len(dirties)}"
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
        good_children = []

        for next_state in get_neighbors(current_state, cols, rows):
            if next_state in explored:
                continue

            child = Node(next_state, current_node, cost=current_node.cost + 1)
            child_h = h(next_state[0], next_state[1])

            children.append((child, child_h))

            if child_h < current_h:
                good_children.append((child, child_h))

            yield {
                "current": current_node,
                "frontier": [c for c, _ in children],
                "explored": explored,
                "log": f"Sinh node {next_state[0]}, h={child_h}, current h={current_h}"
            }

        if not good_children:
            yield {
                "current": current_node,
                "frontier": [c for c, _ in children],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(current_node),
                "log": "Dừng vì không có node con nào tốt hơn để random. Bị kẹt tại cực tiểu cục bộ."
            }
            return

        next_node, next_h = random.choice(good_children)
        current_node = next_node

        yield {
            "current": current_node,
            "frontier": [c for c, _ in good_children],
            "explored": explored,
            "log": f"Random chọn node tốt {current_node.state[0]}, h giảm từ {current_h} xuống {next_h}"
        }
