import pygame
from typing import Tuple, Optional
from constants import *
from maps import MAPS, DIFFICULTY_SETTINGS

class Menu:
    def __init__(self):
        self.button_height = 40
        self.button_width = 120
        self.button_margin = 10
        self.buttons = {}
        self.selected_button: Optional[str] = None
        self.create_buttons()
        self.selected_tower = None
        self.sound_enabled = True
        self.music_enabled = True
        self.click_sound = pygame.mixer.Sound("assets/sounds/Menu Selection Click.wav")
        self.click_sound.set_volume(0.3)
        self.auto_wave = False

    def create_buttons(self):
        # Tower buttons
        y = 140
        self.buttons["basic_tower"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 70 , y, self.button_width - 30, self.button_height)
        self.buttons["slow_tower"] = pygame.Rect(SCREEN_WIDTH - self.button_width + 25, y, self.button_width- 30, self.button_height)

        y += self.button_height + self.button_margin
        self.buttons["rapid_tower"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 70 , y, self.button_width -30 , self.button_height)
        y += self.button_height + self.button_margin
        self.buttons["sniper_tower"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 70 , y, self.button_width -30, self.button_height)
        y += self.button_height + self.button_margin
        self.buttons["laser_tower"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 70, y, self.button_width -30 ,self.button_height)
        y += self.button_height + self.button_margin
        self.buttons["soldier"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 70 , y, self.button_width- 30, self.button_height)

        #dragging button
        y += self.button_height + self.button_margin
        self.buttons["toggle_drag"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30 , y, self.button_width,self.button_height)

        #sell button
        y += self.button_height + self.button_margin
        self.buttons["sell"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30 , y, self.button_width,self.button_height)

        #Upgrade buttion
        y += self.button_height + self.button_margin
        self.buttons["upgrade"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30 , y, self.button_width,self.button_height)

        # Game control buttons
        bottom_y = SCREEN_HEIGHT - (self.button_height + self.button_margin) * 5
        self.buttons["start_wave"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30 , bottom_y, self.button_width,self.button_height)
        self.buttons["quit"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30 ,bottom_y + self.button_height + self.button_margin, self.button_width,self.button_height)
        self.buttons["toggle_sound"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30,bottom_y + 2*self.button_height + 2*self.button_margin, self.button_width,self.button_height)
        self.buttons["toggle_music"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30, bottom_y + 3*self.button_height + 3*self.button_margin, self.button_width,self.button_height)
        self.buttons["auto_wave"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 30,bottom_y + 4 * self.button_height + 4 * self.button_margin,self.button_width, self.button_height)
        # Map selection buttons
        y += self.button_height + self.button_margin * 2
        for map_name in MAPS.keys():
            self.buttons[f"map_{map_name}"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 10, y, self.button_width, self.button_height)
            y += self.button_height + self.button_margin
            
        # Difficulty selection buttons
        y += self.button_margin
        for difficulty in DIFFICULTY_SETTINGS.keys():
            self.buttons[f"diff_{difficulty}"] = pygame.Rect(SCREEN_WIDTH - self.button_width - 10, y, self.button_width, self.button_height)
            y += self.button_height + self.button_margin
    
    def draw(self, screen, gold, wave, lives, dragging_enabled, can_sell=False):
        # Draw background
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH - 200, 0, 200, SCREEN_HEIGHT))
        
        # Draw game info
        gold_text = GAME_FONT.render(f"Gold: {gold}", True, WHITE)
        wave_text = GAME_FONT.render(f"Wave: {wave}", True, WHITE)
        lives_text = GAME_FONT.render(f"Lives: {lives}", True, WHITE)
        
        screen.blit(gold_text, (SCREEN_WIDTH - 190, 10))
        screen.blit(wave_text, (SCREEN_WIDTH - 190, 35))
        screen.blit(lives_text, (SCREEN_WIDTH - 190, 60))
        
        # Draw tower buttons
        self.draw_button(screen, "Basic (50g)", "basic_tower", gold >= 50)
        self.draw_button(screen, "Rapid (75g)", "rapid_tower", gold >= 75)
        self.draw_button(screen, "Sniper (100g)", "sniper_tower", gold >= 100)
        self.draw_button(screen, "Laser (120g)", "laser_tower", gold >= 120)
        self.draw_button(screen, "Slow (90g)", "slow_tower", gold >= 90)

        self.draw_button(screen, "Soldier (75g)", "soldier", gold >= 75)
        #draw dragging button
        self.draw_button(screen, "Drag: " + ("ON" if dragging_enabled else "OFF"), "toggle_drag", True)
        #draw sell button
        self.draw_button(screen,"Sell Tower","sell",can_sell)
        #draw upgrade button
        self.draw_button(screen, "Upgrade", "upgrade", can_sell)
        #draw music control buttion
        self.draw_button(screen, "Sound: " + ("ON" if self.sound_enabled else "OFF"), "toggle_sound", True)
        self.draw_button(screen, "Music: " + ("ON" if self.music_enabled else "OFF"), "toggle_music", True)

        self.draw_button(screen, "Auto Wave: " + ("ON" if self.auto_wave else "OFF"), "auto_wave", True)

        if can_sell:
            tower = self.selected_tower  # gán để dễ viết
            stats = [
                f"Lv {tower.level}",
                f"DMG: {tower.damage}",
                f"RNG: {tower.range}",
                f"RLD: {tower.fire_rate}"
            ]
            start_y = self.buttons["upgrade"].bottom + 10
            for i, line in enumerate(stats):
                stat_text = INFO_FONT.render(line, True, WHITE)
                screen.blit(stat_text, (SCREEN_WIDTH - self.button_width, start_y + i * 20))

        # Draw game control buttons
        self.draw_button(screen, "Start Wave", "start_wave", True)
        self.draw_button(screen, "Quit", "quit", True)
        
    
    def draw_button(self, screen, text, button_id, enabled):
        button = self.buttons[button_id]
        is_selected = (self.selected_button == button_id)
        color = (150, 150, 150) if is_selected else (100, 100, 100) if enabled else (50, 50, 50)
        pygame.draw.rect(screen, color, button)
        pygame.draw.rect(screen, BLACK, button, 2)
        
        text_surface = INFO_FONT.render(text, True, WHITE if enabled else (100, 100, 100))
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos, gold):
        for button_id, button in self.buttons.items():
            if button.collidepoint(pos):
                if button_id == "basic_tower" and gold >= 50:
                    self.selected_button = "basic_tower"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "basic_tower", 50
                elif button_id == "rapid_tower" and gold >= 75:
                    self.selected_button = "rapid_tower"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "rapid_tower", 75
                elif button_id == "sniper_tower" and gold >= 100:
                    self.selected_button = "sniper_tower"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "sniper_tower", 100
                elif button_id == "soldier" and gold >= 75:
                    self.selected_button = "soldier"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "soldier", 75
                elif button_id == "laser_tower" and gold >= 120:
                    self.selected_button = "laser_tower"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "laser_tower", 120
                elif button_id == "slow_tower" and gold >= 90:
                    self.selected_button = "slow_tower"
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "slow_tower", 90
                elif button_id == "auto_wave":
                    self.auto_wave = not self.auto_wave
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "toggle_auto_wave", 0


                elif button_id == "toggle_drag":
                    self.selected_button = None
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "toggle_drag", 0
                elif button_id == "sell":
                    self.selected_button = None
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "sell", 0
                elif button_id == "upgrade":
                    self.selected_button = None
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "upgrade", 0
                elif button_id == "toggle_sound":
                    self.sound_enabled = not self.sound_enabled
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "toggle_sound", 0
                elif button_id == "toggle_music":
                    if self.sound_enabled:
                        self.click_sound.play()
                    self.music_enabled = not self.music_enabled
                    if self.music_enabled:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                    return "toggle_music", 0

                elif button_id == "start_wave":
                    self.selected_button = None
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "start_wave", 0
                elif button_id == "quit":
                    self.selected_button = None
                    if self.sound_enabled:
                        self.click_sound.play()
                    return "quit", 0
                elif button_id.startswith("map_"):
                    if self.sound_enabled:
                        self.click_sound.play()
                    return f"select_map_{button_id[4:]}", 0
                elif button_id.startswith("diff_"):
                    if self.sound_enabled:
                        self.click_sound.play()
                    return f"select_difficulty_{button_id[5:]}", 0
        return None, 0 
