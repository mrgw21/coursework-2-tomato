import pygame
import os
import sys
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar

class SettingsScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)

        # Sidebar setup
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        # Initialize fullscreen state
        self.is_fullscreen = False
        self.running = True

    def toggle_fullscreen(self):
        """Switch between fullscreen and windowed modes."""
        if self.is_fullscreen:
            # Switch to windowed mode, use the current window size
            current_size = self.screen.get_size()  # Get the current window size
            self.screen = pygame.display.set_mode(current_size, pygame.RESIZABLE)
        else:
            # Switch to fullscreen mode (macOS specific handling)
            screen_info = pygame.display.Info()  # Get the current screen info (resolution)
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        self.is_fullscreen = not self.is_fullscreen

    def run(self):
        """Main loop for the Settings screen."""
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos)
                elif event.type == pygame.VIDEORESIZE:
                    # Handle resizing without switching the fullscreen state
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                # Handle sidebar interactions
                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        self.manager.set_active_screen(option_clicked)
                        return

            self.draw()
            pygame.display.update()  # Use update() instead of flip() to avoid conflicts with screen mode changes

    def handle_click(self, mouse_pos):
        """Handle mouse clicks for toggling between windowed and fullscreen modes."""
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0

        # Define the toggle button position
        screen_toggle_rect = pygame.Rect(sidebar_width + 300, 170, 350, 40)
        if screen_toggle_rect.collidepoint(mouse_pos):
            self.toggle_fullscreen()

    def draw(self):
        """Render the Settings screen."""
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))  # White background

        # Draw Title
        title_text = self.title_font.render("Settings", True, (0, 0, 139))  # Dark Blue
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, 100)))

        # Draw header line
        line_start = (sidebar_width + 20, 150)
        line_end = (self.screen.get_width() - 20, 150)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)  # Orange line

        # Define colors for windowed and fullscreen text
        windowed_color = (255, 140, 0) if not self.is_fullscreen else (0, 0, 0)  # Orange if active
        fullscreen_color = (255, 140, 0) if self.is_fullscreen else (0, 0, 0)  # Orange if active

        # Create text labels for "Screen:", "Windowed", and "Full Screen"
        screen_label = self.text_font.render("Screen:", True, (0, 0, 0))  # Black
        windowed_label = self.text_font.render("Windowed", True, windowed_color)
        fullscreen_label = self.text_font.render("Full Screen", True, fullscreen_color)

        # Draw labels for toggling modes
        self.screen.blit(screen_label, (sidebar_width + 120, 170))
        self.screen.blit(windowed_label, (sidebar_width + 300, 170))
        self.screen.blit(self.text_font.render(" /", True, (0, 0, 0)), (sidebar_width + 450, 170))
        self.screen.blit(fullscreen_label, (sidebar_width + 500, 170))

        # Draw Sidebar
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Settings")

    def get_sidebar_option(self, mouse_pos, options):
        """Get which sidebar option was clicked."""
        y_offset = 120
        spacing = 50
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)
            if option_rect.collidepoint(mouse_pos):
                return option
        return None

    @staticmethod
    def resource_path(relative_path):
        """Get the absolute path to a resource."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)