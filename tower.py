import math
import pygame
from typing import List, Optional, Tuple
from constants import *
from projectile import Projectile, SlowProjectile


class Tower:
    def __init__(self, grid_x: int, grid_y: int, damage: int, range_radius: int, fire_rate: float, cost: int):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        self.damage = damage
        self.range = range_radius
        self.fire_rate = fire_rate
        self.cost = cost
        self.cooldown = 0
        self.is_selected = False
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.level = 1
        self.game = None

        self.shoot_sound = pygame.mixer.Sound("assets/sounds/cannon_fire.ogg")
        self.shoot_sound.set_volume(0.2)

    def upgrade(self):
        self.level += 1
        self.damage = int(self.damage * 1.2)
        self.range += 10
        self.fire_rate = max(5, self.fire_rate - 3)

    def can_fire(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.fire_rate

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def find_target(self, enemies: List['Enemy']) -> Optional['Enemy']:
        # Find the closest enemy within range
        target = None
        min_distance = float('inf')
    
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and distance < min_distance:
                target = enemy
                min_distance = distance
    
        return target

    def fire(self, target: 'Enemy') -> Projectile:
        # Create a new projectile targeting the enemy
        return Projectile(self.x, self.y, target, self.damage, 5, YELLOW)

    def start_drag(self, mouse_x: int, mouse_y: int):
        self.is_dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def update_drag(self, mouse_x: int, mouse_y: int):
        if self.is_dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y

    def end_drag(self, grid_x: int, grid_y: int):
        self.is_dragging = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        # Draw selection indicator
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW,(self.grid_x * GRID_SIZE - 2, self.grid_y * GRID_SIZE - 2,GRID_SIZE + 4, GRID_SIZE + 4), 2)

        # Draw range circle if selected
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)

        # Draw tower body
        if self.is_dragging:
            # Draw semi-transparent tower while dragging
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE//2, self.y - GRID_SIZE//2))
        else:
            pygame.draw.rect(screen, GRAY, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)



class BasicTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=15, range_radius=120, fire_rate=30, cost=50)
        self.animation_timer = 0
        self.is_animating = False
        # Load sprite sheet mới
        self.sprite_sheet = pygame.image.load("assets/tower/basic_tower.png").convert_alpha()
        self.frame_width = 128  # Chiều rộng mỗi frame
        self.frame_height = 128  # Chiều cao mỗi frame
        self.frames = []
        self.current_frame = 0
        # Cắt sprite sheet thành 8 frame và scale về GRID_SIZE
        scale_factor = 1.8  # Hoặc 1.5 nếu muốn lớn hơn 1 ô
        for i in range(8):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(pygame.transform.scale(frame, (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor))))
        self.angle = 0
        scale_factor = 1.8
        self.cannon_length = 28 * scale_factor  # Điều chỉnh dựa trên khoảng cách thực tế đến đầu nòng
        self.cannon_offset_x = 0  # Nòng súng ở giữa theo trục x
        self.cannon_offset_y = -32 * scale_factor  +64

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW,(self.grid_x * GRID_SIZE - 2,self.grid_y * GRID_SIZE - 2,GRID_SIZE + 4, GRID_SIZE + 4), 2)
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        if self.is_dragging:
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE // 2, self.y - GRID_SIZE // 2))
        else:
            if self.frames:
                frame_to_draw = self.current_frame if self.is_animating else 0
                original_frame = self.frames[frame_to_draw]
                rotated_frame = pygame.transform.rotate(original_frame, -(self.angle+90))
                new_rect = rotated_frame.get_rect(center=(self.x, self.y))

                screen.blit(rotated_frame, new_rect.topleft)

    def update_angle(self, target: 'Enemy'):
        if target:
            cannon_x = self.x + self.cannon_offset_x
            cannon_y = self.y + self.cannon_offset_y
            dx = target.x - cannon_x
            dy = target.y - cannon_y
            self.angle = math.degrees(math.atan2(dy, dx))

    def fire(self, target: 'Enemy') -> Projectile:
        if self.game and self.game.menu.sound_enabled:
            self.shoot_sound.play()

        self.is_animating = True
        self.animation_timer = len(self.frames) * 5
        self.current_frame = 0

        dx = target.x - self.x
        dy = target.y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))


        angle_rad = math.radians(self.angle)
        cannon_x = self.x + self.cannon_offset_x + math.cos(angle_rad) * self.cannon_length
        cannon_y = self.y + self.cannon_offset_y + math.sin(angle_rad) * self.cannon_length

        return Projectile(cannon_x, cannon_y, target, self.damage, 5, YELLOW)

    def update_cooldown(self,enemies):

        if self.cooldown > 0:
            self.cooldown -= 1

        target = self.find_target(enemies)
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))

        if self.is_animating:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.is_animating = False
            else:
                self.current_frame = (len(self.frames) - 1) - (self.animation_timer // 5)

class RapidTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=10, range_radius=120, fire_rate=15, cost=75)
        self.animation_timer = 0
        self.is_animating = False
        # Load sprite sheet mới
        self.sprite_sheet = pygame.image.load("assets/tower/rapid_tower.png").convert_alpha()
        self.frame_width = 128
        self.frame_height = 128
        self.frames = []
        self.current_frame = 0
        scale_factor = 1.8
        for i in range(8):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(pygame.transform.scale(frame, (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor))))
        self.angle = 0
        self.cannon_length = 15 * scale_factor
        self.cannon_offset_x = 0
        self.cannon_offset_y = -int(GRID_SIZE * scale_factor * 0.5) + 64

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        if self.is_dragging:
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE // 2, self.y - GRID_SIZE // 2))
        else:
            if self.frames:
                frame_to_draw = self.current_frame if self.is_animating else 0
                original_frame = self.frames[frame_to_draw]
                rotated_frame = pygame.transform.rotate(original_frame, -(self.angle+90))
                new_rect = rotated_frame.get_rect(center=(self.x, self.y))
                screen.blit(rotated_frame, new_rect.topleft)
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW,
                            (self.grid_x * GRID_SIZE - 2,
                             self.grid_y * GRID_SIZE - 2,
                             GRID_SIZE + 4, GRID_SIZE + 4), 2)

    def update_angle(self, target: 'Enemy'):
        if target:
            cannon_x = self.x + self.cannon_offset_x
            cannon_y = self.y + self.cannon_offset_y
            dx = target.x - cannon_x
            dy = target.y - cannon_y
            self.angle = math.degrees(math.atan2(dy, dx))

    def fire(self, target: 'Enemy') -> List[Projectile]:
        if self.game and self.game.menu.sound_enabled:
            self.shoot_sound.play()

        self.is_animating = True
        self.animation_timer = len(self.frames) * 5
        self.current_frame = 0

        dx = target.x - self.x
        dy = target.y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))


        cannon_x = self.x + self.cannon_offset_x + math.cos(math.radians(self.angle)) * self.cannon_length
        cannon_y = self.y + self.cannon_offset_y + math.sin(math.radians(self.angle)) * self.cannon_length


        angle_rad = math.radians(self.angle)

        offset_side = 10


        perp_dx = -math.sin(angle_rad)
        perp_dy = math.cos(angle_rad)


        base_x = self.x + self.cannon_offset_x + math.cos(angle_rad) * self.cannon_length
        base_y = self.y + self.cannon_offset_y + math.sin(angle_rad) * self.cannon_length


        left_cannon_x = base_x + perp_dx * offset_side
        left_cannon_y = base_y + perp_dy * offset_side
        right_cannon_x = base_x - perp_dx * offset_side
        right_cannon_y = base_y - perp_dy * offset_side


        proj1 = Projectile(left_cannon_x, left_cannon_y, target, self.damage, 5, YELLOW)
        proj2 = Projectile(right_cannon_x, right_cannon_y, target, self.damage, 5, YELLOW)

        return [proj1, proj2]

    def update_cooldown(self,enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        target = self.find_target(enemies)
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))
        if self.is_animating:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.is_animating = False
            else:
                self.current_frame = (len(self.frames) - 1) - (self.animation_timer // 5)

class SniperTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=15, range_radius=200, fire_rate=60, cost=100)
        self.animation_timer = 0
        self.is_animating = False
        # Load sprite sheet mới
        self.sprite_sheet = pygame.image.load("assets/tower/sniper_tower.png").convert_alpha()
        self.frame_width = 128
        self.frame_height = 128
        self.frames = []
        self.current_frame = 0
        scale_factor = 1.8
        for i in range(8):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(pygame.transform.scale(frame, (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor))))
        self.angle = 0
        self.cannon_length = 24 * scale_factor
        self.cannon_offset_x = 0
        self.cannon_offset_y = -int(GRID_SIZE * scale_factor * 0.5) + 64

        self.game = None

        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.explosion_sound.set_volume(0.05)

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        if self.is_dragging:
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE // 2, self.y - GRID_SIZE // 2))
        else:
            if self.frames:
                frame_to_draw = self.current_frame if self.is_animating else 0
                original_frame = self.frames[frame_to_draw]
                rotated_frame = pygame.transform.rotate(original_frame, -(self.angle+90))
                new_rect = rotated_frame.get_rect(center=(self.x, self.y)
)
                screen.blit(rotated_frame, new_rect.topleft)
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW,
                            (self.grid_x * GRID_SIZE - 2,
                             self.grid_y * GRID_SIZE - 2,
                             GRID_SIZE + 4, GRID_SIZE + 4), 2)

    def update_angle(self, target: 'Enemy'):
        if target:
            cannon_x = self.x + self.cannon_offset_x
            cannon_y = self.y + self.cannon_offset_y
            dx = target.x - cannon_x
            dy = target.y - cannon_y
            self.angle = math.degrees(math.atan2(dy, dx))

    def fire(self, target: 'Enemy') -> Projectile:
        if self.game and self.game.menu.sound_enabled:
            self.shoot_sound.play()


        self.is_animating = True
        self.animation_timer = len(self.frames) * 5
        self.current_frame = 0

        dx = target.x - self.x
        dy = target.y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))


        cannon_x = self.x + self.cannon_offset_x + math.cos(math.radians(self.angle)) * self.cannon_length
        cannon_y = self.y + self.cannon_offset_y + math.sin(math.radians(self.angle)) * self.cannon_length

        proj = Projectile(cannon_x, cannon_y, target, self.damage, 5, YELLOW,game=self.game)
        proj.game = self.game  # Gắn game để truy cập danh sách enemy
        proj.aoe_radius = 50  # Bán kính nổ
        return proj

    def update_cooldown(self,enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        target = self.find_target(enemies)
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))
        if self.is_animating:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.is_animating = False
            else:
                self.current_frame = (len(self.frames) - 1) - (self.animation_timer // 5)

class LaserTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=3, range_radius=150, fire_rate=1, cost=120)

        # Load sprite
        self.sprite_sheet = pygame.image.load("assets/tower/laser_tower.png").convert_alpha()
        self.frame_width = 128
        self.frame_height = 128

        # Scale ảnh cho phù hợp GRID_SIZE
        scale_factor = 0.6
        self.image = pygame.transform.scale(
            self.sprite_sheet,
            (int(self.frame_width * scale_factor), int(self.frame_height * scale_factor))
        )

        self.cannon_length = 24 * scale_factor
        self.cannon_offset_x = 0
        self.cannon_offset_y = -int(GRID_SIZE * scale_factor * 0.5) + 64

        self.laser_color = (0, 255, 255)
        self.beam_width = 4
        self.target = None
        self.tick = 0
        self.laser_flash_timer = 0
        self.laser_sound = pygame.mixer.Sound("assets/sounds/laserpew.ogg")
        self.laser_sound.set_volume(0.2)

    def update_cooldown(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1

        self.target = self.find_target(enemies)
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))

            self.tick += 1
            if self.tick >= 5:
                self.tick = 0
                self.laser_flash_timer = 3  # Hiện laser trong 3 frame
                self.deal_laser_damage()  # Gây sát thương
        else:
            self.tick = 0
            self.laser_flash_timer = 0

    def fire(self, target):
        return []  # không tạo đạn

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)

        if self.is_dragging:
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE // 2, self.y - GRID_SIZE // 2))
        else:
            rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, rect.topleft)

        if self.is_selected:
            pygame.draw.rect(screen, YELLOW,
                             (self.grid_x * GRID_SIZE - 2, self.grid_y * GRID_SIZE - 2, GRID_SIZE + 4, GRID_SIZE + 4),
                             2)

        # Laser flash effect (hiện trong 3 frame)
        if self.laser_flash_timer > 0 and self.target and not self.target.is_dead():
            self.laser_flash_timer -= 1

            angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
            num_beams = 1 + (self.level - 1) * 2
            spread_angle = 10

            for i in range(num_beams):
                offset = (i - (num_beams - 1) / 2) * math.radians(spread_angle)
                beam_angle = angle + offset

                # Tính điểm xa nhất
                end_x = self.x + math.cos(beam_angle) * self.range
                end_y = self.y + math.sin(beam_angle) * self.range

                pygame.draw.line(
                    screen,
                    self.laser_color,
                    (int(self.x), int(self.y)),
                    (int(end_x), int(end_y)),
                    self.beam_width
                )

    def deal_laser_damage(self):
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)

        num_beams = 1 + (self.level - 1) * 2  # Level 1: 1 tia, Level 2: 3 tia, ...
        spread_angle = 10  # độ lệch mỗi tia

        if self.game and self.game.menu.sound_enabled:
            self.laser_sound.play()

        for i in range(num_beams):
            offset = (i - (num_beams - 1) / 2) * math.radians(spread_angle)
            beam_angle = angle + offset

            for enemy in self.game.enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                dist = math.hypot(dx, dy)
                if dist <= self.range:
                    angle_to_enemy = math.atan2(dy, dx)
                    if abs(angle_to_enemy - beam_angle) < 0.15:
                        enemy.take_damage(self.damage)

    def upgrade(self):
        self.level += 1
        self.damage += 1
        self.range += 10
        self.fire_rate = max(1, self.fire_rate - 2)


class SlowTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=10, range_radius=140, fire_rate=40, cost=90)

        self.slow_amount = 0.5      # Giảm 50% tốc độ
        self.slow_duration = 90     # Trong 90 frame (1.5s)

        self.sprite_sheet = pygame.image.load("assets/tower/slow_tower.png").convert_alpha()
        self.frame_width = 128
        self.frame_height = 128
        self.frames = []
        scale_factor = 1.8
        for i in range(11):  # 11 frame animation
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(pygame.transform.scale(frame, (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor))))

        self.current_frame = 0
        self.animation_timer = 0
        self.is_animating = False

        # Xoay nòng
        self.angle = 0
        self.cannon_length = 25
        self.cannon_offset_x = 0
        self.cannon_offset_y = -int(GRID_SIZE * scale_factor * 0.5) + 64

    def update_cooldown(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1

        # Xoay theo target
        target = self.find_target(enemies)
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))

        # Cập nhật animation
        if self.is_animating:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.is_animating = False
            else:
                self.current_frame = (len(self.frames) - 1) - (self.animation_timer // 5)

    def fire(self, target: 'Enemy'):
        if self.game and self.game.menu.sound_enabled:
            self.shoot_sound.play()
        self.is_animating = True
        self.animation_timer = len(self.frames) * 5
        self.current_frame = 0

        # Tính hướng bắn
        dx = target.x - self.x
        dy = target.y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
        angle_rad = math.radians(self.angle)

        cannon_x = self.x + self.cannon_offset_x + math.cos(angle_rad) * self.cannon_length
        cannon_y = self.y + self.cannon_offset_y + math.sin(angle_rad) * self.cannon_length

        proj = SlowProjectile(
            cannon_x, cannon_y,
            target,
            damage=self.damage,
            speed=5,
            color=(100, 200, 255),
            slow_factor=self.slow_amount,
            slow_duration=self.slow_duration,
            game=self.game
        )
        return proj

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (100, 200, 255, 80), (int(self.x), int(self.y)), self.range, 1)

        if self.is_dragging:
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 255, 128))
            screen.blit(s, (self.x - GRID_SIZE // 2, self.y - GRID_SIZE // 2))
        else:
            if self.frames:
                frame_to_draw = self.current_frame if self.is_animating else 0
                original_frame = self.frames[frame_to_draw]
                rotated_frame = pygame.transform.rotate(original_frame, -(self.angle + 90))
                rect = rotated_frame.get_rect(center=(self.x, self.y))
                screen.blit(rotated_frame, rect.topleft)

        if self.is_selected:
            pygame.draw.rect(screen, BLUE, (
                self.grid_x * GRID_SIZE - 2,
                self.grid_y * GRID_SIZE - 2,
                GRID_SIZE + 4, GRID_SIZE + 4
            ), 2)






