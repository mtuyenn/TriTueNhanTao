from ..informed_search.a_star import A_star


def partialobservation_search(cases, cols, rows):
    observed_positions = cases[0].get("known_positions", []) if cases else []
    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "log": f"Biết trước 2 ô quan sát: {observed_positions}",
    }

    initial_bs = []
    for case_index, case in enumerate(cases):
        start = case["start_state"]
        dirties = tuple(sorted(case["current_dirties"]))
        initial_bs.append((case_index, start, dirties))

    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "log": f"Tập BS có {len(initial_bs)} giả định; 2 ô quan sát giống nhau trong mọi giả định.",
    }

    all_paths = []
    for case_index, start, dirties in initial_bs:
        yield {
            "current": None,
            "frontier": [],
            "explored": set(),
            "log": f"--- Chạy A* cho giả định {case_index + 1}, robot xuất phát tại {start} ---",
        }

        path_for_case = []
        for step in A_star(start, dirties, cols, rows):
            if "log" in step:
                step["log"] = f"[Giả định {case_index + 1}] {step['log']}"

            if step.get("done"):
                path_for_case = step.get("path", [])
                yield {
                    "current": step.get("current"),
                    "frontier": step.get("frontier", []),
                    "explored": step.get("explored", set()),
                    "log": f"[Giả định {case_index + 1}] Tìm thấy đường đi: {len(path_for_case) - 1} bước!",
                }
            else:
                yield step

        all_paths.append({"case_index": case_index, "start": start, "path": path_for_case})

    final_path = all_paths[0]["path"] if all_paths else []
    yield {
        "current": None,
        "frontier": [],
        "explored": set(),
        "done": True,
        "path": final_path,
        "all_paths": all_paths,
        "log": f"Hoàn tất lập kế hoạch cho {len(initial_bs)} trạng thái trong BS. Bắt đầu mô phỏng...",
    }
