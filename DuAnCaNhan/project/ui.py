# pyrefly: ignore [missing-import]
import pygame

# Bảng màu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
DARK_GRAY = (50, 50, 50)

class ComboBox:
    def __init__(self, x, y, w, h, options, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = font
        self.active = False
        self.selected_index = 0

    def draw(self, surface):
        # Vẽ nút chính
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = self.font.render(self.options[self.selected_index], True, BLACK)
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

        # Vẽ danh sách thả xuống nếu active
        if self.active:
            for i, option in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.h, self.rect.w, self.rect.h)
                pygame.draw.rect(surface, GRAY, opt_rect)
                pygame.draw.rect(surface, BLACK, opt_rect, 1)
                opt_surf = self.font.render(option, True, BLACK)
                surface.blit(opt_surf, (opt_rect.x + 5, opt_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                return True
            elif self.active:
                for i in range(len(self.options)):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.h, self.rect.w, self.rect.h)
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.active = False
                        return True
                self.active = False
        return False

    def get_selected(self):
        return self.options[self.selected_index]

class InputBox:
    def __init__(self, x, y, w, h, text='', font=None, label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (180, 180, 180)
        self.color_active = (50, 150, 255)
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        if self.label:
            lbl_surface = self.font.render(self.label, True, BLACK)
            screen.blit(lbl_surface, (self.rect.x, self.rect.y - 25))
        # Nền trắng cho dễ nhìn
        pygame.draw.rect(screen, WHITE, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)