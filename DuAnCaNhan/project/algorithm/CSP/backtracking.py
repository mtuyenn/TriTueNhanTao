MAP_COLORS = (
    ("Đỏ", (239, 105, 105)),
    ("Xanh lá", (111, 207, 151)),
    ("Xanh dương", (105, 160, 235)),
    ("Vàng", (245, 211, 100)),
)

# A white pixel safely inside each district on assets/hcm_city_map.png.
REGION_SEEDS = {
    "Củ Chi": (296, 271),
    "Quận 12": (550, 527),
    "Hóc Môn": (434, 483),
    "Gò Vấp": (559, 597),
    "TP Thủ Đức": (823, 616),
    "Bình Thạnh": (651, 655),
    "Tân Bình": (499, 662),
    "Phú Nhuận": (566, 684),
    "Tân Phú": (430, 723),
    "Quận 1": (576, 757),
    "Quận 10": (521, 750),
    "Quận 3": (630, 742),
    "Quận 4": (648, 795),
    "Bình Tân": (330, 727),
    "Quận 11": (469, 805),
    "Quận 5": (548, 807),
    "Quận 7": (728, 854),
    "Quận 8": (569, 872),
    "Bình Chánh": (380, 962),
    "Quận 6": (481, 894),
    "Nhà Bè": (669, 988),
    "Cần Giờ": (893, 1174),
}

HCM_REGIONS = tuple(REGION_SEEDS)

# Adjacency graph for the simplified district map used by the project.
HCM_ADJACENCY = {
    "Củ Chi": {"Hóc Môn"},
    "Hóc Môn": {"Củ Chi", "Quận 12", "Tân Phú", "Bình Tân"},
    "Quận 12": {"Hóc Môn", "Gò Vấp", "Bình Thạnh", "TP Thủ Đức", "Tân Bình", "Tân Phú"},
    "Gò Vấp": {"Quận 12", "Tân Bình", "Phú Nhuận", "Bình Thạnh"},
    "Tân Bình": {"Gò Vấp", "Phú Nhuận", "Tân Phú", "Quận 10", "Quận 11", "Quận 12"},
    "Tân Phú": {"Hóc Môn", "Tân Bình", "Bình Tân", "Quận 10", "Quận 11", "Quận 12"},
    "Bình Tân": {"Hóc Môn", "Tân Phú", "Quận 11", "Quận 6", "Bình Chánh"},
    "Phú Nhuận": {"Gò Vấp", "Tân Bình", "Bình Thạnh", "Quận 3", "Quận 1", "Quận 10"},
    "Bình Thạnh": {"Quận 12", "Gò Vấp", "Phú Nhuận", "Quận 3", "Quận 4", "TP Thủ Đức"},
    "Quận 10": {"Tân Bình", "Tân Phú", "Quận 11", "Quận 1", "Quận 5", "Phú Nhuận"},
    "Quận 11": {"Bình Tân","Tân Bình", "Tân Phú", "Quận 10", "Quận 6", "Quận 5"},
    "Quận 3": {"Phú Nhuận", "Bình Thạnh", "Quận 1", "Quận 4", "TP Thủ Đức"},
    "Quận 1": {"Phú Nhuận", "Quận 3", "Quận 4", "Quận 10", "Quận 5"},
    "Quận 4": {"Quận 1", "TP Thủ Đức", "Quận 7", "Quận 8", "Quận 3", "Quận 5", "Bình Thạnh"},
    "Quận 5": {"Quận 10", "Quận 11", "Quận 1", "Quận 4", "Quận 6", "Quận 8"},
    "Quận 6": {"Bình Tân", "Quận 5", "Quận 8", "Bình Chánh", "Quận 11"},
    "Quận 8": {"Quận 4", "Quận 5", "Quận 6", "Quận 7", "Bình Chánh", "Nhà Bè"},
    "Quận 7": {"TP Thủ Đức", "Quận 4", "Quận 8", "Nhà Bè", "Cần Giờ"},
    "TP Thủ Đức": {"Quận 12", "Bình Thạnh", "Quận 3", "Quận 4", "Quận 7"},
    "Bình Chánh": {"Bình Tân", "Quận 6", "Quận 8", "Nhà Bè"},
    "Nhà Bè": {"Quận 7", "Quận 8", "Bình Chánh", "Cần Giờ"},
    "Cần Giờ": {"Quận 7", "Nhà Bè"},
}


def backtracking_map_coloring(region_order=None, color_count=4):
    if not 1 <= color_count <= len(MAP_COLORS):
        raise ValueError("color_count must be between 1 and 4")

    order = list(region_order or HCM_REGIONS)
    if len(order) != len(HCM_REGIONS) or set(order) != set(HCM_REGIONS):
        raise ValueError("region_order must contain every HCM region exactly once")

    assignments = {}
    yield {
        "action": "start",
        "assignments": {},
        "region": None,
        "color": None,
        "done": False,
        "success": False,
        "log": f"Bắt đầu backtracking với {len(order)} vùng và {color_count} màu.",
    }

    def solve(index):
        if index == len(order):
            return True

        region = order[index]
        for color_index in range(color_count):
            conflicts = []
            for neighbor in HCM_ADJACENCY[region]:
                if assignments.get(neighbor) == color_index:
                    conflicts.append(neighbor)
            color_name = MAP_COLORS[color_index][0]

            if conflicts:
                yield {
                    "action": "reject",
                    "assignments": dict(assignments),
                    "region": region,
                    "color": color_index,
                    "done": False,
                    "success": False,
                    "log": f"Từ chối {region} = {color_name}: trùng màu với {conflicts[0]}.",
                }
                continue

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

            if (yield from solve(index + 1)):
                return True

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
