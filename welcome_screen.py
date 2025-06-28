import pygame
from typing import Tuple, Optional
from constants import *

class WelcomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.button_height = int(SCREEN_HEIGHT * 0.08)  # Dynamic button height
        self.button_width = int(SCREEN_WIDTH * 0.3)  # Dynamic button width
        self.button_margin = int(SCREEN_HEIGHT * 0.02)  # Dynamic margin
        self.buttons = {}
        self.create_buttons()

        self.click_sound = pygame.mixer.Sound("assets/sounds/Menu Selection Click.wav")
        self.click_sound.set_volume(0.3)
        
    def create_buttons(self):
        # Title position
        self.title_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            int(SCREEN_HEIGHT * 0.2),
            self.button_width,
            int(SCREEN_HEIGHT * 0.15)
        )
        
        # Play button
        y = int(SCREEN_HEIGHT * 0.5)
        self.buttons["play"] = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            y,
            self.button_width,
            self.button_height
        )
        
        # Quit button
        y += self.button_height + self.button_margin
        self.buttons["quit"] = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            y,
            self.button_width,
            self.button_height
        )
    
    def draw(self):
        # Draw background
        self.screen.fill(DARK_GREEN)
        
        # Draw title
        title_text = TITLE_FONT.render("Tower Defense 8-bit", True, WHITE)
        title_rect = title_text.get_rect(center=self.title_rect.center)
        self.screen.blit(title_text, title_rect)
        
        # Draw play button
        self.draw_button("Play Game", "play", True, False)
        
        # Draw quit button
        self.draw_button("Quit Game", "quit", True, False)
    
    def draw_button(self, text, button_id, enabled, is_selected):
        button = self.buttons[button_id]
        color = (150, 150, 150) if is_selected else (100, 100, 100) if enabled else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button)
        pygame.draw.rect(self.screen, WHITE if is_selected else BLACK, button, 2)
        
        text_surface = GAME_FONT.render(text, True, WHITE if enabled else (100, 100, 100))
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos) -> Optional[str]:
        for button_id, button in self.buttons.items():
            if button.collidepoint(pos):
                self.click_sound.play()
                return button_id
        return None 
