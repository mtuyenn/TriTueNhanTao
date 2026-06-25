from collections import deque

from .backtracking import HCM_ADJACENCY, HCM_REGIONS, MAP_COLORS


def ac3_map_coloring(region_order=None, color_count=4):

    if not 1 <= color_count <= len(MAP_COLORS):
        raise ValueError("color_count must be between 1 and 4")

    order = list(region_order or HCM_REGIONS)
    if len(order) != len(HCM_REGIONS) or set(order) != set(HCM_REGIONS):
        raise ValueError("region_order must contain every HCM region exactly once")

    domains = {region: set(range(color_count)) for region in order}
    assignments = {}

    yield {
        "action": "start", "assignments": {}, "region": None, "color": None,
        "done": False, "success": False,
        "log": f"Bắt đầu AC-3 (MAC) với {len(order)} vùng và {color_count} màu.",
    }

    def revise(xi, xj):
        removed = set()
        for x in tuple(domains[xi]):
            # Constraint for adjacent regions: x != y.
            if not any(x != y for y in domains[xj]):
                domains[xi].remove(x)
                removed.add(x)
        return removed

    def enforce_ac3(initial_arcs):
        queue = deque(initial_arcs)
        while queue:
            xi, xj = queue.popleft()
            removed = revise(xi, xj)
            if not removed:
                continue

            removed_names = ", ".join(MAP_COLORS[c][0] for c in sorted(removed))
            yield {
                "action": "revise", "assignments": dict(assignments),
                "region": xi, "color": next(iter(removed)), "done": False,
                "success": False,
                "log": f"AC-3 xét ({xi}, {xj}): loại {removed_names} khỏi miền {xi}.",
            }
            if not domains[xi]:
                return False
            for xk in HCM_ADJACENCY[xi] - {xj}:
                queue.append((xk, xi))
        return True

    def solve():
        if len(assignments) == len(order):
            return True

        # MRV, with the selected order as a stable tie-breaker.
        unassigned = [r for r in order if r not in assignments]
        region = min(unassigned, key=lambda r: len(domains[r]))

        for color in sorted(domains[region]):
            snapshot = {r: set(values) for r, values in domains.items()}
            assignments[region] = color
            domains[region] = {color}
            yield {
                "action": "assign", "assignments": dict(assignments),
                "region": region, "color": color, "done": False,
                "success": False,
                "log": f"Gán {region} = {MAP_COLORS[color][0]}, đưa các cung liên quan vào hàng đợi.",
            }

            consistent = yield from enforce_ac3(
                (neighbor, region) for neighbor in HCM_ADJACENCY[region]
            )
            if consistent and (yield from solve()):
                return True

            assignments.pop(region, None)
            for r, values in snapshot.items():
                domains[r] = values
            yield {
                "action": "backtrack", "assignments": dict(assignments),
                "region": region, "color": color, "done": False,
                "success": False,
                "log": f"Miền rỗng: quay lui tại {region}, khôi phục các miền.",
            }
        return False

    success = yield from solve()
    yield {
        "action": "done", "assignments": dict(assignments),
        "region": None, "color": None, "done": True, "success": success,
        "log": "AC-3 tô màu hoàn tất!" if success else "AC-3 không tìm được cách tô màu.",
    }
