import pygame

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames = []
        self.current_frame = 0
        self.frame_delay = 3  # số frame chờ giữa các hình
        self.timer = 0
        self.finished = False

        # Load sprite sheet
        sheet = pygame.image.load("assets/effect/sniper_bullet.png").convert_alpha()
        frame_width = 48
        frame_height = 48
        num_frames = 8

        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            # Scale lên nếu cần (ví dụ 2x):
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_delay:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            frame = self.frames[self.current_frame]
            rect = frame.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(frame, rect.topleft)
