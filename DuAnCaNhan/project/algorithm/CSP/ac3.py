from collections import deque

from .backtracking import HCM_ADJACENCY, HCM_REGIONS, MAP_COLORS


def ac3_map_coloring(region_order=None, color_count=4):

    if not 1 <= color_count <= len(MAP_COLORS):
        raise ValueError("color_count must be between 1 and 4")

    order = list(region_order or HCM_REGIONS)
    if len(order) != len(HCM_REGIONS) or set(order) != set(HCM_REGIONS):
        raise ValueError("region_order must contain every HCM region exactly once")

    domains = {}
    for region in order:
        domains[region] = set()
        for color in range(color_count):
            domains[region].add(color)
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
            has_valid_color = False
            for y in domains[xj]:
                if x != y:
                    has_valid_color = True
                    break
            if not has_valid_color:
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

            removed_names_list = []
            for c in sorted(removed):
                removed_names_list.append(MAP_COLORS[c][0])
            removed_names = ", ".join(removed_names_list)
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
        unassigned = []
        for r in order:
            if r not in assignments:
                unassigned.append(r)

        region = unassigned[0]
        for r in unassigned:
            if len(domains[r]) < len(domains[region]):
                region = r

        for color in sorted(domains[region]):
            snapshot = {}
            for r, values in domains.items():
                snapshot[r] = set(values)
            assignments[region] = color
            domains[region] = {color}
            yield {
                "action": "assign", "assignments": dict(assignments),
                "region": region, "color": color, "done": False,
                "success": False,
                "log": f"Gán {region} = {MAP_COLORS[color][0]}, đưa các cung liên quan vào hàng đợi.",
            }

            arcs = []
            for neighbor in HCM_ADJACENCY[region]:
                arcs.append((neighbor, region))
            consistent = yield from enforce_ac3(arcs)
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
