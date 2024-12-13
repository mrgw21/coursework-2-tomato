import pygame
import os
import sys
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar


class AboutScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)

        # Sidebar setup
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        # Initialize running state
        self.running = True

    def run(self):
        """Main loop for the About screen."""
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
                    if self.sidebar.visible and self.sidebar.handle_event(event):
                        option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                        if option_clicked:
                            self.running = False
                            self.manager.set_active_screen(option_clicked)
                            return

            self.draw()
            pygame.display.update()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))  # White background

        # Draw Title
        title_text = self.title_font.render("About", True, (0, 0, 139))  # Dark Blue
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, 100)))

        # Draw header line
        line_start = (sidebar_width + 20, 150)
        line_end = (self.screen.get_width() - 20, 150)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)  # Orange line

        # Draw description
        description_lines = [
            "Inside Immune: A Serious Game Project",
            "Developed by Team Tomato",
            "Version 1.0",
            "",
            "Description:",
            "This game is designed to educate players about the",
            "fundamental mechanisms of the immune system.",
            "Dive into interactive intros, levels, and quizzes!",
        ]
        y_offset = 200
        for line in description_lines:
            line_surface = self.text_font.render(line, True, (0, 0, 0))  # Black
            self.screen.blit(line_surface, (sidebar_width + 250, y_offset))
            y_offset += 30

        # Draw Team Members
        team_header = self.text_font.render("Team Members:", True, (0, 0, 139))  # Dark Blue
        self.screen.blit(team_header, (sidebar_width + 250, y_offset + 20))
        y_offset += 60

        team_members = [
            "Alger Da Costa",
            "Anmol Choudhary",
            "Anuj Verma",
            "Kiranjeet Dhillon",
            "Rasyid Gatra Wijaya",
            "Nat Strange",
        ]
        for member in team_members:
            member_surface = self.text_font.render(member, True, (0, 0, 0))  # Black
            self.screen.blit(member_surface, (sidebar_width + 300, y_offset))
            y_offset += 30

        # Draw Sidebar
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "About")

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
