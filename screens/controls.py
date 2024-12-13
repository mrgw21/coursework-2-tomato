import pygame
import os
import sys
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar

class ControlsScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)

        # Sidebar setup
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        # Load and scale WASD Image
        self.image = pygame.image.load(self.resource_path("assets/images/WASD.png"))

        # Make the WASD image smaller
        scaled_width = self.screen.get_width() // 4  # Reduce width
        scaled_height = self.screen.get_height() // 6  # Reduce height
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

        # Initialize WASD image position
        self.image_rect = self.image.get_rect()
        self.update_image_position()

        self.control_lines = [
            "Move: W A S D keys",
            "Toggle Sidebar: M",
            "Pause: P",
        ]

        self.text_positions = []
        self.calculate_text_positions()
        self.running = True

    def update_image_position(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.image_rect = self.image.get_rect(
            center=(self.screen.get_width() // 2 + sidebar_width // 2, self.screen.get_height() // 3)
        )

    def calculate_text_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        # Place control text below the WASD image
        image_bottom_y = self.image_rect.bottom
        self.text_positions = [
            [center_x, image_bottom_y + 40 + i * 40] for i in range(len(self.control_lines))
        ]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_m:
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()
                elif event.type == pygame.VIDEORESIZE:
                    self.reposition_elements(event.w, event.h)

                # Handle sidebar interactions
                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        if option_clicked == "Introduction":
                            option_clicked = "Preliminary"
                        self.manager.set_active_screen(option_clicked)
                        return

            self.draw()
            pygame.display.flip()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))

        # Draw Title Text
        title_text = self.title_font.render("Controls", True, (0, 0, 139))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, 100)))

        line_start = (sidebar_width + 20, 150)
        line_end = (self.screen.get_width() - 20, 150)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)

        # Draw WASD Image
        self.screen.blit(self.image, self.image_rect)

        # Draw Control Information
        for i, line in enumerate(self.control_lines):
            if ":" in line:
                action, key = line.split(": ", 1)
                action_text = self.text_font.render(action + ":", True, (255, 140, 0))
                key_text = self.text_font.render(key, True, (0, 0, 0))

                # Draw the action and key text
                action_rect = action_text.get_rect(center=(self.text_positions[i][0] - 100, self.text_positions[i][1]))
                key_rect = key_text.get_rect(center=(self.text_positions[i][0] + 50, self.text_positions[i][1]))
                
                self.screen.blit(action_text, action_rect)
                self.screen.blit(key_text, key_rect)
            else:
                text = self.text_font.render(line, True, (0, 0, 0))
                self.screen.blit(text, text.get_rect(center=(self.text_positions[i][0], self.text_positions[i][1])))

        # Draw Sidebar
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Controls")

    def handle_sidebar_toggle(self):
        self.update_image_position()
        self.calculate_text_positions()

    def reposition_elements(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.update_image_position()
        self.calculate_text_positions()

    def get_sidebar_option(self, mouse_pos, options):
        y_offset = 120
        spacing = 50
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)
            if option_rect.collidepoint(mouse_pos):
                return option
        return None

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)