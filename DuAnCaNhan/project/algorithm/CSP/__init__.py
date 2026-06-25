from .backtracking import (
    HCM_ADJACENCY,
    HCM_REGIONS,
    MAP_COLORS,
    REGION_SEEDS,
    backtracking_map_coloring,
)
from .forward_checking import forward_checking_map_coloring
from .ac3 import ac3_map_coloring
from .min_conflicts import min_conflicts_map_coloring

__all__ = [
    "HCM_ADJACENCY",
    "HCM_REGIONS",
    "MAP_COLORS",
    "REGION_SEEDS",
    "backtracking_map_coloring",
    "forward_checking_map_coloring",
    "ac3_map_coloring",
    "min_conflicts_map_coloring",
]
