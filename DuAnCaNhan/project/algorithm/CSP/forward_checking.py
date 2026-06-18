from algorithm.CSP.backtracking import MAP_COLORS, HCM_REGIONS, HCM_ADJACENCY

def forward_checking_map_coloring(region_order=None, color_count=4):
    """Yield every assignment, rejection and backtrack in the CSP search with Forward Checking."""
    if not 1 <= color_count <= len(MAP_COLORS):
        raise ValueError("color_count must be between 1 and 4")

    order = list(region_order or HCM_REGIONS)
    if len(order) != len(HCM_REGIONS) or set(order) != set(HCM_REGIONS):
        raise ValueError("region_order must contain every HCM region exactly once")

    assignments = {}

    # tạo domain cho từng vùng
    domains = {region: list(range(color_count)) for region in order}

    yield {
        "action": "start",
        "assignments": {},
        "region": None,
        "color": None,
        "done": False,
        "success": False,
        "log": f"Bắt đầu Forward Checking với {len(order)} vùng và {color_count} màu.",
    }

    def forward_check(region, color, unassigned_regions):
        pruned = []
        for neighbor in HCM_ADJACENCY[region]:
            if neighbor in unassigned_regions and color in domains[neighbor]:
                domains[neighbor].remove(color)
                pruned.append((neighbor, color))
                if len(domains[neighbor]) == 0:
                    return False, pruned
        return True, pruned

    def solve(index):
        if index == len(order):
            return True

        region = order[index]
        unassigned_regions = order[index+1:]
        
        available_colors = list(domains[region])
        
        for color_index in available_colors:
            color_name = MAP_COLORS[color_index][0]

            assignments[region] = color_index
            yield {
                "action": "assign",
                "assignments": dict(assignments),
                "region": region,
                "color": color_index,
                "done": False,
                "success": False,
                "log": f"Gán {region} = {color_name}.",
            }

            fc_success, pruned = forward_check(region, color_index, unassigned_regions)
            
            if not fc_success:
                failed_neighbor = [n for n in unassigned_regions if len(domains[n]) == 0][0]
                yield {
                    "action": "reject",
                    "assignments": dict(assignments),
                    "region": region,
                    "color": color_index,
                    "done": False,
                    "success": False,
                    "log": f"Từ chối {region} = {color_name}: FC phát hiện {failed_neighbor} sẽ hết màu!",
                }
                
                for n, c in pruned:
                    domains[n].append(c)
                del assignments[region]
                continue

            if (yield from solve(index + 1)):
                return True

            for n, c in pruned:
                domains[n].append(c)
            del assignments[region]
            
            yield {
                "action": "backtrack",
                "assignments": dict(assignments),
                "region": region,
                "color": color_index,
                "done": False,
                "success": False,
                "log": f"Quay lui tại {region}, bỏ màu {color_name}.",
            }

        return False

    success = yield from solve(0)
    yield {
        "action": "done",
        "assignments": dict(assignments),
        "region": None,
        "color": None,
        "done": True,
        "success": success,
        "log": "Tô màu hoàn tất!" if success else "Không tìm được cách tô với số màu đã chọn.",
    }
