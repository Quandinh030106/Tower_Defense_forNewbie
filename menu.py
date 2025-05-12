import pygame
from typing import Tuple, Optional
from constants import *

class Menu:
    def __init__(self):
        self.buttons = [
            {"text": "Basic Tower (50)", "cost": 50, "type": "basic_tower"},
            {"text": "Sniper Tower (100)", "cost": 100, "type": "sniper_tower"},
            {"text": "Rapid Tower (75)", "cost": 75, "type": "rapid_tower"},
            {"text": "Soldier (30)", "cost": 30, "type": "soldier"},
            {"text": "Start Wave", "type": "start_wave"},
            {"text": "Quit Game", "type": "quit"}
        ]
        self.button_height = 40
        self.button_width = 180
        self.button_margin = 10
        self.menu_x = SCREEN_WIDTH - self.button_width - 20
        self.menu_y = 20
        
    def draw(self, screen: pygame.Surface, gold: int, wave: int, lives: int):
        # Draw menu background
        pygame.draw.rect(screen, (50, 50, 50), (self.menu_x - 10, 0, self.button_width + 30, SCREEN_HEIGHT))
        
        # Draw game info
        gold_text = GAME_FONT.render(f"Gold: {gold}", True, YELLOW)
        wave_text = GAME_FONT.render(f"Wave: {wave}", True, WHITE)
        lives_text = GAME_FONT.render(f"Lives: {lives}", True, RED)
        
        screen.blit(gold_text, (self.menu_x, 20))
        screen.blit(wave_text, (self.menu_x, 50))
        screen.blit(lives_text, (self.menu_x, 80))
        
        # Draw buttons
        for i, button in enumerate(self.buttons):
            button_y = self.menu_y + (self.button_height + self.button_margin) * (i + 3)
            
            # Check if player can afford the tower
            can_afford = True
            if "cost" in button and button["cost"] > gold:
                can_afford = False
                
            color = (100, 100, 100) if can_afford else (50, 50, 50)
            pygame.draw.rect(screen, color, (self.menu_x, button_y, self.button_width, self.button_height))
            pygame.draw.rect(screen, BLACK, (self.menu_x, button_y, self.button_width, self.button_height), 2)
            
            # Button text
            text = GAME_FONT.render(button["text"], True, WHITE if can_afford else GRAY)
            text_rect = text.get_rect(center=(self.menu_x + self.button_width//2, button_y + self.button_height//2))
            screen.blit(text, text_rect)
    
    def handle_click(self, mouse_pos: Tuple[int, int], gold: int) -> Tuple[Optional[str], int]:
        x, y = mouse_pos
        
        for i, button in enumerate(self.buttons):
            button_y = self.menu_y + (self.button_height + self.button_margin) * (i + 3)
            
            if (self.menu_x <= x <= self.menu_x + self.button_width and 
                button_y <= y <= button_y + self.button_height):
                
                # Check if player can afford the tower
                if "cost" in button and button["cost"] > gold:
                    return None, 0  # Can't afford
                    
                return button["type"], button.get("cost", 0)
                
        return None, 0  # No button clicked 