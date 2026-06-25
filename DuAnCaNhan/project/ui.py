# pyrefly: ignore [missing-import]
import pygame

WHITE = (248, 250, 252)
BLACK = (15, 23, 42)
GRAY = (226, 232, 240)
BLUE = (59, 130, 246)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
YELLOW = (250, 204, 21)
DARK_GRAY = (30, 41, 59)
MUTED = (100, 116, 139)
PANEL = (255, 255, 255)
BORDER = (203, 213, 225)
HOVER = (239, 246, 255)


def fit_text(font, text, max_width):
    text = str(text)
    if font.size(text)[0] <= max_width:
        return text
    ellipsis = "..."
    available = max(0, max_width - font.size(ellipsis)[0])
    clipped = ""
    for char in text:
        if font.size(clipped + char)[0] > available:
            break
        clipped += char
    return clipped + ellipsis


class ComboBox:
    def __init__(self, x, y, w, h, options, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = font
        self.active = False
        self.selected_index = 0
        self.scroll_offset = 0
        self.visible_items = 9

    def _menu_rect(self):
        rows = min(self.visible_items, len(self.options))
        return pygame.Rect(self.rect.x, self.rect.bottom + 8, self.rect.w, rows * (self.rect.h + 2) + 8)

    def _option_rect(self, index):
        row = index - self.scroll_offset
        return pygame.Rect(self.rect.x + 4, self.rect.bottom + 12 + row * (self.rect.h + 2), self.rect.w - 8, self.rect.h)

    def draw(self, surface):
        pygame.draw.rect(surface, PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surface, BORDER, self.rect, 1, border_radius=8)
        text = fit_text(self.font, self.options[self.selected_index], self.rect.w - 42)
        surface.blit(self.font.render(text, True, BLACK), (self.rect.x + 14, self.rect.y + 7))
        arrow_x = self.rect.right - 22
        arrow_y = self.rect.centery
        pygame.draw.polygon(surface, MUTED, [(arrow_x - 6, arrow_y - 3), (arrow_x + 6, arrow_y - 3), (arrow_x, arrow_y + 5)])

        if not self.active:
            return

        menu_rect = self._menu_rect()
        pygame.draw.rect(surface, PANEL, menu_rect, border_radius=8)
        pygame.draw.rect(surface, BORDER, menu_rect, 1, border_radius=8)
        end = min(len(self.options), self.scroll_offset + self.visible_items)
        for i in range(self.scroll_offset, end):
            opt_rect = self._option_rect(i)
            bg = HOVER if i == self.selected_index else PANEL
            pygame.draw.rect(surface, bg, opt_rect, border_radius=6)
            text = fit_text(self.font, self.options[i], opt_rect.w - 18)
            surface.blit(self.font.render(text, True, BLACK), (opt_rect.x + 10, opt_rect.y + 7))

        if len(self.options) > self.visible_items:
            track = pygame.Rect(menu_rect.right - 10, menu_rect.y + 8, 4, menu_rect.h - 16)
            pygame.draw.rect(surface, GRAY, track, border_radius=2)
            thumb_h = max(24, int(track.h * self.visible_items / len(self.options)))
            max_offset = len(self.options) - self.visible_items
            thumb_y = track.y + int((track.h - thumb_h) * self.scroll_offset / max_offset)
            pygame.draw.rect(surface, MUTED, (track.x, thumb_y, track.w, thumb_h), border_radius=2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.active:
                    self.scroll_offset = min(self.selected_index, max(0, len(self.options) - self.visible_items))
                return True

            if self.active:
                end = min(len(self.options), self.scroll_offset + self.visible_items)
                for i in range(self.scroll_offset, end):
                    if self._option_rect(i).collidepoint(event.pos):
                        self.selected_index = i
                        self.active = False
                        return True
                self.active = False

        if event.type == pygame.MOUSEWHEEL and self.active:
            max_offset = max(0, len(self.options) - self.visible_items)
            self.scroll_offset = max(0, min(max_offset, self.scroll_offset - event.y))
            return True

        return False

    def get_selected(self):
        return self.options[self.selected_index]


class InputBox:
    def __init__(self, x, y, w, h, text="", font=None, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = BORDER
        self.color_active = BLUE
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        if self.label:
            screen.blit(self.font.render(self.label, True, MUTED), (self.rect.x, self.rect.y - 23))
        pygame.draw.rect(screen, PANEL, self.rect, border_radius=8)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 7))
        pygame.draw.rect(screen, self.color, self.rect, 1, border_radius=8)
