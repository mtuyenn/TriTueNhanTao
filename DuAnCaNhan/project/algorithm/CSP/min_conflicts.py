import random

from .backtracking import HCM_ADJACENCY, HCM_REGIONS, MAP_COLORS


def min_conflicts_map_coloring(region_order=None, color_count=4, max_steps=2000, seed=None):
    if not 1 <= color_count <= len(MAP_COLORS):
        raise ValueError("color_count must be between 1 and 4")
    if max_steps < 1:
        raise ValueError("max_steps must be positive")

    order = list(region_order or HCM_REGIONS)
    if len(order) != len(HCM_REGIONS) or set(order) != set(HCM_REGIONS):
        raise ValueError("region_order must contain every HCM region exactly once")

    rng = random.Random(seed)
    assignments = {}
    for region in order:
        assignments[region] = rng.randrange(color_count)

    def conflicts(region, color):
        count = 0
        for neighbor in HCM_ADJACENCY[region]:
            if assignments[neighbor] == color:
                count += 1
        return count

    yield {
        "action": "start", "assignments": dict(assignments),
        "region": None, "color": None, "done": False, "success": False,
        "log": "Min-Conflicts tạo một phép gán đầy đủ ngẫu nhiên.",
    }

    for step_number in range(1, max_steps + 1):
        conflicted = []
        for r in order:
            if conflicts(r, assignments[r]) > 0:
                conflicted.append(r)
        if not conflicted:
            yield {
                "action": "done", "assignments": dict(assignments),
                "region": None, "color": None, "done": True, "success": True,
                "log": f"Min-Conflicts tô màu hoàn tất sau {step_number - 1} bước sửa.",
            }
            return

        region = rng.choice(conflicted)
        scores = {}
        for color in range(color_count):
            scores[color] = conflicts(region, color)

        best_score = None
        for color in scores:
            if best_score is None or scores[color] < best_score:
                best_score = scores[color]

        best_colors = []
        for color in scores:
            if scores[color] == best_score:
                best_colors.append(color)
        color = rng.choice(best_colors)
        old_color = assignments[region]
        assignments[region] = color

        yield {
            "action": "repair", "assignments": dict(assignments),
            "region": region, "color": color, "done": False, "success": False,
            "log": (
                f"Bước {step_number}: {region} xung đột, đổi "
                f"{MAP_COLORS[old_color][0]} → {MAP_COLORS[color][0]} "
                f"(còn {best_score} xung đột tại vùng này)."
            ),
        }

    yield {
        "action": "done", "assignments": dict(assignments),
        "region": None, "color": None, "done": True, "success": False,
        "log": f"Min-Conflicts dừng sau {max_steps} bước mà chưa có nghiệm.",
    }
