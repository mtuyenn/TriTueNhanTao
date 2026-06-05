from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h

def local_beam_search(start, dirties, cols, rows, k=3):
    dirties = normalize_dirties(dirties)
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    start_node = Node(start_state, cost=0)

    if len(start_state[1]) == 0:
        yield {
            "current": start_node,
            "frontier": [],
            "explored": set(),
            "done": True,
            "path": reconstruct_path(start_node),
            "log": "Sàn nhà đã sạch từ đầu!"
        }
        return  

    # Beam bắt đầu với k phần tử là start_node (ở bước đầu tiên chỉ có 1 node)
    beam = [start_node]
    explored = set()

    yield {
        "current": start_node,
        "frontier": beam,
        "explored": explored,
        "log": f"Local Beam Search khởi tạo tại {start}, rác còn: {len(dirties)}, k={k}"
    }

    while True:
        next_beam_candidates = []
        
        # Kiểm tra xem có state nào trong beam đã đến đích chưa
        for node in beam:
            if len(node.state[1]) == 0:
                yield {
                    "current": node,
                    "frontier": beam,
                    "explored": explored,
                    "done": True,
                    "path": reconstruct_path(node),
                    "log": "SÀN NHÀ ĐÃ SẠCH!"
                }
                return
            explored.add(node.state)

        for node in beam:
            for next_state in get_neighbors(node.state, cols, rows):
                if next_state not in explored:
                    child = Node(next_state, node, cost=node.cost + 1)
                    child_h = h(next_state[0], next_state[1])
                    next_beam_candidates.append((child, child_h))

        if not next_beam_candidates:
            yield {
                "current": beam[0] if beam else None,
                "frontier": [],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(beam[0]) if beam else [],
                "log": "Dừng vì không có trạng thái lân cận nào để tiếp tục. Bị kẹt tại cực tiểu cục bộ."
            }
            return

        # Sắp xếp các candidates theo heuristic (thấp đến cao) và chọn k phần tử tốt nhất
        next_beam_candidates.sort(key=lambda x: x[1])
        
        # Chọn k phần tử tốt nhất
        beam = [child for child, child_h in next_beam_candidates[:k]]

        best_h = next_beam_candidates[0][1]

        yield {
            "current": beam[0], # Hiển thị đại diện node tốt nhất trong beam
            "frontier": beam,
            "explored": explored,
            "log": f"Giữ lại {len(beam)} node tốt nhất trong Beam, heuristic tốt nhất = {best_h}"
        }
