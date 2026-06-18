from .backtracking import (
    HCM_ADJACENCY,
    HCM_REGIONS,
    MAP_COLORS,
    REGION_SEEDS,
    backtracking_map_coloring,
)
from .forward_checking import forward_checking_map_coloring

__all__ = [
    "HCM_ADJACENCY",
    "HCM_REGIONS",
    "MAP_COLORS",
    "REGION_SEEDS",
    "backtracking_map_coloring",
    "forward_checking_map_coloring",
]
