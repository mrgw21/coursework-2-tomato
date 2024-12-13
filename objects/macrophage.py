import os
import sys
import pygame

class Macrophage:
    DEFAULT_OFFSET = 200
    ANIMATION_SPEED = 100

    def __init__(self, screen_width, screen_height, sidebar_width=400):
        self.image = pygame.image.load(self.resource_path("assets/images/final/macrophage-1.png"))
        img = self.image
        self.image = pygame.transform.scale(img, (img.get_width() * 0.2, img.get_height() * 0.2))
        self.frames = self.load_animation_frames()
        self.animation_index = 0
        self.animation_start_time = None
        self.is_animating = False

        self.speed = 5
        self.rect = self.image.get_rect()
        self.sidebar_width = sidebar_width
        self.set_initial_position(screen_width, screen_height, sidebar_width)

        # Direction tracking (default: facing right, D key)
        self.direction = "D"
        self.angle_map = {"W": 90, "A": 180, "S": 270, "D": 0}  # Map keys to rotation angles

    def load_animation_frames(self):
        frames = []
        for i in range(1, 9):
            frame = pygame.image.load(self.resource_path(f"assets/images/final/macrophage-{i}.png"))
            frame = pygame.transform.scale(frame, (frame.get_width() * 0.2, frame.get_height() * 0.2))
            frames.append(frame)
        return frames

    def set_initial_position(self, screen_width, screen_height, sidebar_width):
        game_width = screen_width - sidebar_width
        center_x = sidebar_width + game_width // 2 - self.DEFAULT_OFFSET
        center_y = screen_height // 2
        self.rect.center = (center_x, center_y)

    def start_animation(self):
        self.is_animating = True
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_index = 0

    def update_animation(self):
        if self.is_animating:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.animation_start_time

            frame_duration = self.ANIMATION_SPEED
            self.animation_index = (elapsed_time // frame_duration) % len(self.frames)

            if elapsed_time >= len(self.frames) * frame_duration:
                self.is_animating = False
                self.image = self.frames[0]
            else:
                self.image = self.frames[self.animation_index]

    def handle_input(self, screen_width, screen_height, sidebar_width):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
            self.direction = "W"
        if keys[pygame.K_s] and self.rect.bottom < screen_height:  # Move down
            self.rect.y += self.speed
            self.direction = "S"
        if keys[pygame.K_a] and self.rect.left > sidebar_width:  # Move left
            self.rect.x -= self.speed
            self.direction = "A"
        if keys[pygame.K_d] and self.rect.right < screen_width:  # Move right
            self.rect.x += self.speed
            self.direction = "D"

    def handle_collision(self, pathogens):
        if pathogens:
            self.start_animation()

    def update(self, screen_width, screen_height, sidebar_width):
        self.handle_input(screen_width, screen_height, sidebar_width)
        self.update_animation()

    def draw(self, screen):
        # Rotate the image based on the current direction
        rotated_image = pygame.transform.rotate(self.image, self.angle_map[self.direction])
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        # Draw the rotated image
        screen.blit(rotated_image, rotated_rect)

    def get_collision_rect(self):
        return self.rect.inflate(0, 0)

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)