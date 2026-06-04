from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def Simple_Hill_Climbing(start, dirties, cols, rows):
    dirties = normalize_dirties(dirties)

    # Nếu robot bắt đầu ở ô có rác thì dọn luôn
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    current_node = Node(start_state, cost=0)

    explored = set()

    yield {
        "current": current_node,
        "frontier": [],
        "explored": explored,
        "log": f"Simple Hill Climbing khởi tạo tại {start}, rác còn: {len(dirties)}"
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

        found_better = False

        for next_state in get_neighbors(current_state, cols, rows):
            if next_state in explored:
                continue

            next_h = h(next_state[0], next_state[1])
            child = Node(next_state, current_node, cost=current_node.cost + 1)

            yield {
                "current": current_node,
                "frontier": [child],
                "explored": explored,
                "log": f"Xét node {next_state[0]}, h={next_h}, current h={current_h}"
            }

            # h nhỏ hơn nghĩa là trạng thái tốt hơn
            if next_h < current_h:
                current_node = child
                found_better = True

                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "log": f"Chọn node tốt hơn {next_state[0]}, h giảm từ {current_h} xuống {next_h}"
                }

                break

        if not found_better:
            yield {
                "current": current_node,
                "frontier": [],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(current_node),
                "log": "Dừng vì không có trạng thái lân cận nào có h nhỏ hơn. Có thể bị kẹt tại cực tiểu cục bộ."
            }
            return
