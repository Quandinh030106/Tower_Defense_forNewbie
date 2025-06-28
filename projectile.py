import math
import pygame

class Projectile:
    def __init__(self, x: int, y: int, target, damage: int, speed: int, color: tuple,game=None):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        self.color = color
        self.radius = 5
        self.hit = False
        self.game = game

    def move(self) -> bool:
        if self.target.health <= 0:
            return True  # Target is dead, remove projectile
        
        # Calculate direction to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.radius + self.target.radius:
            # Nếu đạn có aoe_radius và game thì gây sát thương lan
            if hasattr(self, "aoe_radius") and hasattr(self, "game"):
                for enemy in self.game.enemies:
                    dx = enemy.x - self.target.x
                    dy = enemy.y - self.target.y
                    if math.sqrt(dx ** 2 + dy ** 2) <= self.aoe_radius:
                        enemy.take_damage(self.damage)

                if hasattr(self, "game"):
                    for tower in self.game.towers:
                        if type(tower).__name__ == "SniperTower":
                            tower.explosion_sound.play()
                            break
            else:
                self.target.take_damage(self.damage)
            if self.game:
                self.game.add_explosion(self.x, self.y)
                
            return True

        # Normalize and move
        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed
        
        return False  # Keep moving
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 