from ..base import Node, normalize_dirties, get_neighbors, reconstruct_path

def depth_limited_search(start, dirties, cols, rows, limit):
    dirties = normalize_dirties(dirties)

    # nếu có rác ở vị trí đang đứng => dọn sạch
    dirties = tuple(d for d in dirties if d != start)
    
    # khởi tạo trạng thái ban đầu (vị trí (x,y), rác còn lại)
    start_state = (start, dirties)
    # khởi tạo node ban đầu 
    start_node = Node(start_state)
    
    stack = [(start_node, 0)] # tạo stack chứa các node
    visited = set() # các trạng thái đã thăm 
    
    while stack:
        # lấy node trong stack để duyệt
        node, depth = stack.pop()
        visited.add(node.state)
        
        yield {
            "current" : node,
            "frontier" : [n for n, d in stack],
            "explored" : visited,
            "log": f"IDS depth={depth}/{limit}, robot ở {node.state[0]}, rác còn: {len(node.state[1])}"
        }
        
        # kiểm tra các node con có = GOAL không
        if len(node.state[1]) == 0: # nếu hết rác
            yield {
                "current" : node,
                "frontier" : [n for n, d in stack],
                "explored": visited,
                "done" : True,
                "path" : reconstruct_path(node),
                "log" : "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!"
            }
            return
        
        # nếu rác vẫn còn thì sinh con 
        if depth < limit:
            for neighbor_state in reversed(get_neighbors(node.state, cols, rows)):
                if neighbor_state not in visited and neighbor_state not in [n.state for n, d in stack]:
                    child = Node(neighbor_state, node)
                    stack.append((child, depth + 1))
                
                    yield {
                        "current": node,
                        "frontier": [n for n, d in stack],
                        "explored": visited,
                        "log": f"Sinh node {neighbor_state[0]}, depth={depth + 1}, rác còn: {len(neighbor_state[1])}"
                    }
        
    
def ids(start, dirties, cols, rows, max_depth):

    # duyệt từng level của cây
    for limit in range(max_depth + 1):

        yield{
            "current" : None,
            "frontier" : [],
            "explored" : set(),
            "log" : f"IDS bắt đầu với độ sâu = {limit}"
        }

        for step in depth_limited_search(start, dirties, cols, rows, limit):
            yield step

            if step.get("done"):
                return

    # nếu không tìm thấy đường đi
    yield {
        "current" : None,
        "frontier" : [],
        "explored" : set(),
        "done" : True,
        "path" : [],
        "log" : f"Không tìm thấy đường đi trong depth = {max_depth}"
    }


def ids_normal(start, dirties, cols, rows):
    return ids(start, dirties, cols, rows, max_depth=rows * cols * len(dirties))


# thuật toán tối ưu IDS -> sinh con ra duyệt rồi mới cho vào stack

def depth_limited_search_v2(start, dirties, cols, rows, limit):
    dirties = normalize_dirties(dirties)

    # nếu có rác ở vị trí đang đứng => dọn sạch
    dirties = tuple(d for d in dirties if d != start)
    
    # khởi tạo trạng thái ban đầu (vị trí (x,y), rác còn lại)
    start_state = (start, dirties)
    # khởi tạo node ban đầu 
    start_node = Node(start_state)

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
    
    stack = [(start_node, 0)] # tạo stack chứa các node
    visited = set() # các trạng thái đã thăm 

    while stack:
        node, depth = stack.pop()
        visited.add(node.state)

        yield {
            "current": node,
            "frontier": [n for n, d in stack],
            "explored": visited,
            "log": f"IDS depth={depth}/{limit}, robot ở {node.state[0]}, rác còn: {len(node.state[1])}"
        }

        if depth < limit:
            for neighbor_state in reversed(get_neighbors(node.state, cols, rows)):
                if neighbor_state in visited or neighbor_state in [n.state for n, d in stack]:
                    continue

                child = Node(neighbor_state, node) # sinh node con

                yield {
                    "current": node,
                    "frontier": [n for n, d in stack],
                    "explored": visited,
                    "log": f"Sinh node {neighbor_state[0]}, depth={depth + 1}, rác còn: {len(neighbor_state[1])}"
                }

                # kiểm tra goal trước khi cho vào stack
                if len(child.state[1]) == 0:
                    yield {
                        "current": child,
                        "frontier": [n for n, d in stack],
                        "explored": visited,
                        "done": True,
                        "path": reconstruct_path(child),
                        "log": "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!"
                    }
                    return

                # nếu chưa phải goal thì mới cho vào stack
                stack.append((child, depth + 1))

                yield {
                    "current": node,
                    "frontier": [n for n, d in stack],
                    "explored": visited,
                    "log": f"Đưa node {neighbor_state[0]} vào Stack"
                }

def ids2(start, dirties, cols, rows, max_depth):

    # duyệt từng level của cây
    for limit in range(max_depth + 1):

        yield{
            "current" : None,
            "frontier" : [],
            "explored" : set(),
            "log" : f"IDS bắt đầu với độ sâu = {limit}"
        }

        for step in depth_limited_search_v2(start, dirties, cols, rows, limit):
            yield step

            if step.get("done"):
                return

    # nếu không tìm thấy đường đi
    yield {
        "current" : None,
        "frontier" : [],
        "explored" : set(),
        "done" : True,
        "path" : [],
        "log" : f"Không tìm thấy đường đi trong depth = {max_depth}"
    }


def ids2_optimize(start, dirties, cols, rows):
    return ids2(start, dirties, cols, rows, max_depth = rows * cols * len(dirties))
