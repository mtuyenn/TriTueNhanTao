import random
from ..informed_search.a_star import A_star

def partialobservation_search(cases, cols, rows):
    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "log": f"Biết trước vị trí của partialobservation: {[c['start_state'] for c in cases]}"
    }

    initial_bs = set()
    for case in cases:
        pos = case["start_state"]
        guess_dirties = tuple(sorted(case["current_dirties"]))
        initial_bs.add((pos, guess_dirties))

    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "log": f"Tập trạng thái ban đầu có {len(initial_bs)} vị trí có thể, các vị trí đã biết đều không có rác."
    }

    all_paths = []

    for state in initial_bs:
        start_guess, current_dirties = state
        
        yield {
            "current": None,
            "frontier": [],
            "explored": set(),
            "log": f"--- Chạy A* giả định robot xuất phát tại {start_guess} ---"
        }
        
        # Thực hiện thuật toán A*
        a_star_gen = A_star(start_guess, current_dirties, cols, rows)
        
        path_for_this_state = []
        for step in a_star_gen:
            if "log" in step:
                step["log"] = f"[Giả định {start_guess}] " + step["log"]
                
            if step.get("done"):
                path_for_this_state = step.get("path", [])
                
                yield {
                    "current": step.get("current"),
                    "frontier": step.get("frontier", []),
                    "explored": step.get("explored", set()),
                    "log": f"[Giả định {start_guess}] Tìm thấy đường đi: {len(path_for_this_state)-1} bước!"
                }
            else:
                yield step
                
        all_paths.append((start_guess, path_for_this_state))

    final_path = all_paths[0][1] if all_paths else []

    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "done": True,
        "path": final_path,
        "all_paths": all_paths,
        "log": f"Hoàn tất duyệt {len(initial_bs)} giả định tưởng tượng! Bắt đầu mô phỏng robot..."
    }
