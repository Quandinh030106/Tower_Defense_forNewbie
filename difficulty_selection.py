import pygame
from typing import Optional
from constants import *
from maps import DIFFICULTY_SETTINGS

class DifficultySelection:
    def __init__(self, screen, selected_map: str):
        self.screen = screen
        self.selected_map = selected_map
        self.button_height = int(SCREEN_HEIGHT * 0.08)  # Dynamic button height
        self.button_width = int(SCREEN_WIDTH * 0.3)  # Dynamic button width
        self.button_margin = int(SCREEN_HEIGHT * 0.02)  # Dynamic margin
        self.buttons = {}
        self.selected_difficulty = "Medium"
        self.create_buttons()

        self.click_sound = pygame.mixer.Sound("assets/sounds/Menu Selection Click.wav")
        self.click_sound.set_volume(0.3)
        
    def create_buttons(self):
        # Title position
        self.title_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            int(SCREEN_HEIGHT * 0.1),
            self.button_width,
            int(SCREEN_HEIGHT * 0.15)
        )
        
        # Difficulty selection buttons
        y = int(SCREEN_HEIGHT * 0.3)
        for difficulty in DIFFICULTY_SETTINGS.keys():
            self.buttons[f"diff_{difficulty}"] = pygame.Rect(
                SCREEN_WIDTH // 2 - self.button_width // 2,
                y,
                self.button_width,
                self.button_height
            )
            y += self.button_height + self.button_margin
            
        # Start game button
        y += self.button_margin * 2
        self.buttons["start"] = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            y,
            self.button_width,
            self.button_height
        )
        
        # Back button
        y += self.button_height + self.button_margin
        self.buttons["back"] = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            y,
            self.button_width,
            self.button_height
        )
    
    def draw(self):
        # Draw background
        self.screen.fill(DARK_GREEN)
        
        # Draw title
        title_text = TITLE_FONT.render("Select Difficulty", True, WHITE)
        title_rect = title_text.get_rect(center=self.title_rect.center)
        self.screen.blit(title_text, title_rect)
        
        # Draw difficulty selection buttons
        for difficulty in DIFFICULTY_SETTINGS.keys():
            is_selected = difficulty == self.selected_difficulty
            self.draw_button(
                f"Difficulty: {difficulty}",
                f"diff_{difficulty}",
                True,
                is_selected
            )
        
        # Draw start game button
        self.draw_button("Start Game", "start", True, False)
        
        # Draw back button
        self.draw_button("Back", "back", True, False)
        
        # Draw difficulty description
        settings = DIFFICULTY_SETTINGS[self.selected_difficulty]
        desc = f"Starting Gold: {settings['starting_gold']} | Lives: {settings['starting_lives']}"
        desc_text = GAME_FONT.render(desc, True, WHITE)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(desc_text, desc_rect)
    
    def draw_button(self, text, button_id, enabled, is_selected):
        button = self.buttons[button_id]
        color = (150, 150, 150) if is_selected else (100, 100, 100) if enabled else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button)
        pygame.draw.rect(self.screen, WHITE if is_selected else BLACK, button, 2)
        
        text_surface = GAME_FONT.render(text, True, WHITE if enabled else (100, 100, 100))
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos) -> tuple[Optional[str], Optional[str], Optional[str]]:
        for button_id, button in self.buttons.items():
            if button.collidepoint(pos):
                if button_id.startswith("diff_"):
                    self.selected_difficulty = button_id[5:]
                    self.click_sound.play()
                    return None, None, None
                elif button_id == "start":
                    self.click_sound.play()
                    return "start", self.selected_map, self.selected_difficulty
                elif button_id == "back":
                    self.click_sound.play()
                    return "back", None, None
        return None, None, None 
