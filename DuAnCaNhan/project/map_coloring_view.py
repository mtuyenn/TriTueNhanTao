"""Pygame renderer that colors regions in the HCM raster map."""

# pyrefly: ignore [missing-import]
import pygame

from algorithm.CSP.backtracking import MAP_COLORS, REGION_SEEDS


class HCMMapRenderer:
    def __init__(self, image_path, max_display_size=(620, 332)):
        self.base_surface = pygame.image.load(image_path).convert()
        source_width, source_height = self.base_surface.get_size()
        max_width, max_height = max_display_size
        scale = min(max_width / source_width, max_height / source_height)
        self.display_size = (
            round(source_width * scale),
            round(source_height * scale),
        )

        white_mask = pygame.mask.from_threshold(
            self.base_surface,
            (255, 255, 255),
            (20, 20, 20, 255),
        )
        self.region_masks = {
            region: white_mask.connected_component(seed)
            for region, seed in REGION_SEEDS.items()
        }
        self._validate_masks()
        self._cache_key = None
        self._cache_surface = None

    def _validate_masks(self):
        seen = []
        for region, mask in self.region_masks.items():
            if mask.count() == 0:
                raise ValueError(f"Không tìm thấy vùng ảnh cho {region}")
            if any(mask.overlap_area(other, (0, 0)) for other in seen):
                raise ValueError(f"Mặt nạ vùng {region} bị trùng với vùng khác")
            seen.append(mask)

    def render(self, assignments):
        key = tuple(sorted(assignments.items()))
        if key != self._cache_key:
            colored = self.base_surface.copy()
            for region, color_index in assignments.items():
                self.region_masks[region].to_surface(
                    surface=colored,
                    setcolor=MAP_COLORS[color_index][1],
                    unsetcolor=None,
                )
            self._cache_surface = pygame.transform.smoothscale(colored, self.display_size)
            self._cache_key = key
        return self._cache_surface
