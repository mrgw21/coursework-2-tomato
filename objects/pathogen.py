import math
import pygame
import os
import sys

class Pathogen:
    def __init__(self, x, y, type, screen_width=None, screen_height=None, can_replicate=True):
        self.x = x
        self.y = y
        self.speed = 0.4
        self.alive = False
        self.type = type

        # Launch-related attributes
        self.launch_velocity = (0, 0)
        self.launching = False  # Indicates whether the pathogen is in the launching phase
        self.launch_start_time = None  # Time when the launch started

        # Set target cell and attack timer
        self.target_cell = None
        self.attack_timer = 0  # For delayed attacks

        self.replicas = 0
        self.spawn_time = pygame.time.get_ticks()
        self.can_replicate = can_replicate  # Determines if the pathogen can replicate

        if self.type == "bacteria":
            self.original_image = pygame.image.load(self.resource_path("assets/images/final/bacteria.png"))
            self.original_image = pygame.transform.scale(self.original_image, (80, 80))
            self.collision_shrink = -35  # Collision box shrink for bacteria
        else:
            self.original_image = pygame.image.load(self.resource_path("assets/images/final/virus.png"))
            self.original_image = pygame.transform.scale(self.original_image, (180, 180))
            self.collision_shrink = -140  # Collision box shrink for virus

        self.image = self.original_image  # Copy of the image for rotation
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Adjust initial position dynamically based on screen dimensions
        if screen_width and screen_height:
            self.adjust_initial_position(screen_width, screen_height)

    def adjust_initial_position(self, screen_width, screen_height):
        # Centerize position dynamically based on current screen size
        self.rect.x = screen_width // 2 + (self.rect.x - screen_width // 2)
        self.rect.y = screen_height // 2 + (self.rect.y - screen_height // 2)
    

    def update_position(self, cells):
        current_time = pygame.time.get_ticks()

        if self.launching and self.launch_start_time:
            # Check if 1 second has passed since launching
            if current_time - self.launch_start_time > 1000:  # 1 second
                self.launching = False  # End the launching phase
                self.find_closest_uninfected_cell(cells)  # Find a new target
                self.launch_velocity = (0, 0)  # Stop the launch velocity

        # Apply launch velocity if still launching
        if self.launching:
            self.x += self.launch_velocity[0]
            self.y += self.launch_velocity[1]
            self.rect.center = (self.x, self.y)
        elif self.target_cell:
            # Move towards the target after the launch phase
            self.move_towards_target(cells)

    def move_towards_target(self, cells):
        # Find the closest uninfected cell
        target_cell = self.find_closest_uninfected_cell(cells)

        if target_cell:
            target_x, target_y = target_cell.rect.center

            # Rotate to face the target
            self.rotate_towards_target(target_x, target_y)

            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance > 30:  # Move towards the cell
                dx, dy = dx / distance, dy / distance
                self.x += dx * self.speed
                self.y += dy * self.speed
                self.rect.center = (self.x, self.y)
            elif self.get_collision_rect().colliderect(target_cell.get_collision_rect()):
                # Infect the cell if colliding
                target_cell.die()
                self.alive = True  # Mark pathogen as used
                return True
        return False

    def rotate_towards_target(self, target_x, target_y):
        # Calculate the angle to the target
        dx, dy = target_x - self.x, target_y - self.y
        angle = math.degrees(math.atan2(dy, -dx))

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, angle)
        # Preserve the center after rotation
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def find_closest_uninfected_cell(self, cells):
        closest_cell = None
        min_distance = float('inf')
        
        for cell in cells:
            if cell.health == "uninfected":  # Only target uninfected cells
                distance = math.hypot(cell.rect.centerx - self.x, cell.rect.centery - self.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_cell = cell

        return closest_cell

    def attack_infected_cell(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_timer > 1500:  # Attack delay of 1.5 seconds
            self.attack_timer = current_time  # Reset the attack timer
            return True
        return False

    def draw(self, screen):
        if not self.alive:
            # Draw the pathogen image
            screen.blit(self.image, self.rect)

            # Draw collision rect for debugging
            # pygame.draw.rect(screen, (255, 0, 0), self.get_collision_rect(), 2)
    
    def reposition(self, sidebar_width, width_ratio, height_ratio):
        # Adjust the position based on resizing ratios
        new_x = sidebar_width + (self.rect.centerx - sidebar_width) * width_ratio
        new_y = self.rect.centery * height_ratio

        # Ensure pathogen does not overlap the sidebar
        if new_x < sidebar_width:
            new_x = sidebar_width + 20  # Offset slightly outside the sidebar

        # Update pathogen position
        self.rect.centerx = int(new_x)
        self.rect.centery = int(new_y)
        self.x, self.y = self.rect.center  # Update the logical position as well
    
    def get_collision_rect(self):
        # Get the original, unrotated rect based on the original image size
        base_rect = self.original_image.get_rect(center=self.rect.center)
        
        # Inflate the base rect dynamically to create the collision rect
        collision_rect = base_rect.inflate(self.collision_shrink, self.collision_shrink)
        return collision_rect
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)