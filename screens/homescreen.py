import os
import pygame
import sys
from data.save_manager import load_progress

class HomeScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.running = True

        # Colors
        self.BACKGROUND_COLOR = (255, 255, 255)  # White
        self.PRIMARY_COLOR = (0, 0, 139)  # Dark Blue
        self.SECONDARY_COLOR = (255, 140, 0)  # Dark Orange
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREYED_OUT_COLOR = (169, 169, 169)  # Grey

        # Fonts
        self.font = pygame.font.SysFont("Arial", 36)
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)

        # Load the title image as a JPEG
        self.title_image = pygame.image.load(self.resource_path("assets/images/inside-immune-title.jpg"))

        # Load progress
        self.progress = load_progress()

        # Buttons with their corresponding target screens
        self.buttons = {
            "Introduction": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 50, 200, 50),
                "color": self.PRIMARY_COLOR,
                "options": ["Preliminary"]
            },
            "Level 1": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 150, 200, 50),
                "color": self.PRIMARY_COLOR,
                "options": ["Level 1"]
            },
            "Level 2": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 250, 200, 50),
                # Determine color based on progress
                "color": self.PRIMARY_COLOR if self.progress.get("level1_completed", False) else self.GREYED_OUT_COLOR,
                "options": ["Level 2"],
                "enabled": self.progress.get("level1_completed", False)  # Check if Level 1 is completed
            },
            "Quizzes": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 350, 200, 50),
                "color": self.SECONDARY_COLOR,
                "options": ["Quizzes"]
            },
            "Exit Game": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 450, 200, 50),
                "color": (139, 0, 0)  # Dark Red
            }
        }

        self.current_menu = None  # Track which menu is open

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()

        # Adjust button positions dynamically
        self.buttons["Introduction"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 50, 200, 50
        )
        self.buttons["Level 1"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 150, 200, 50
        )
        self.buttons["Level 2"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 250, 200, 50
        )
        self.buttons["Quizzes"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 350, 200, 50
        )
        self.buttons["Exit Game"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 450, 200, 50
        )

    def draw_button(self, button_text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(button_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_background(self):
        self.screen.fill(self.BACKGROUND_COLOR)

    def draw_main_buttons(self):
        for button_text, button_data in self.buttons.items():
            self.draw_button(button_text, button_data["rect"], button_data["color"])

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = event.pos
            for button_text, button_data in self.buttons.items():
                if button_data["rect"].collidepoint(mouse_pos):
                    if button_text == "Exit Game":
                        pygame.quit()
                        exit()
                    elif button_text == "Level 2" and not button_data.get("enabled", True):
                        pass
                    else:
                        # Directly set the screen based on the options key
                        self.manager.set_active_screen(button_data["options"][0])
                        self.running = False

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw_background()

            # Draw the title image
            resized_title_image = pygame.transform.scale(
                self.title_image, (self.screen.get_width() // 1.5, self.screen.get_height() // 1.5)
            )
            title_rect = self.title_image.get_rect(center=(self.screen.get_width() // 2, 140))
            self.screen.blit(self.title_image, title_rect)

            self.draw_main_buttons()
            pygame.display.flip()
        
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)