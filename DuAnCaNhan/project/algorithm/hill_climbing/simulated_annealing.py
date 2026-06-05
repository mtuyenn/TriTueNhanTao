from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path, h
import random
import math

def simulated_annealing(start, dirties, cols, rows, alpha=0.9, T0=100.0, Tmin=0.01):
    dirties = normalize_dirties(dirties)

    # Nếu robot bắt đầu ở ô có rác thì dọn luôn
    dirties = tuple(d for d in dirties if d != start)

    start_state = (start, dirties)
    current_node = Node(start_state, cost=0)

    explored = set()
    T = T0

    yield {
        "current": current_node,
        "frontier": [],
        "explored": explored,
        "log": f"Simulated Annealing khởi tạo tại {start}, rác còn: {len(dirties)}"
    }

    while T > Tmin:
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

        neighbors = get_neighbors(current_state, cols, rows)
        if not neighbors:
            yield {
                "current": current_node,
                "frontier": [],
                "explored": explored,
                "done": True,
                "path": reconstruct_path(current_node),
                "log": "Dừng vì không có trạng thái lân cận nào."
            }
            return
            
        next_state = random.choice(neighbors)
        next_h = h(next_state[0], next_state[1])
        child = Node(next_state, current_node, cost=current_node.cost + 1)
        
        delta = next_h - current_h

        yield {
            "current": current_node,
            "frontier": [child],
            "explored": explored,
            "log": f"T={T:.2f}, Xét random node {next_state[0]}, h={next_h}, delta={delta}"
        }

        if delta < 0:
            current_node = child
            yield {
                "current": current_node,
                "frontier": [],
                "explored": explored,
                "log": f"Chấp nhận node tốt hơn {next_state[0]}"
            }
        else:
            p = math.exp(-delta / T)
            r = random.random()
            if r < p:
                current_node = child
                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "log": f"Chấp nhận node kém hơn {next_state[0]} với xác suất {p:.3f} (random={r:.3f})"
                }
            else:
                yield {
                    "current": current_node,
                    "frontier": [],
                    "explored": explored,
                    "log": f"Từ chối node {next_state[0]} (p={p:.3f}, random={r:.3f})"
                }

        T = alpha * T

    # Nếu vòng lặp kết thúc mà chưa tìm được đích
    yield {
        "current": current_node,
        "frontier": [],
        "explored": explored,
        "done": True,
        "path": reconstruct_path(current_node),
        "log": f"Dừng vì nhiệt độ T={T:.2f} <= Tmin={Tmin}. Chưa dọn xong rác."
    }
