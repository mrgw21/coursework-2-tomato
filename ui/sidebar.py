import pygame
from data.save_manager import load_progress

class Sidebar:
    def __init__(self):
        self.width = 400
        self.options = ["Home", "Introduction", "Level 1", "Level 2", "Quizzes", "Leaderboards", "Controls", "About", "Exit Game"]
        self.visible = True
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 25, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)

        # Load player progress
        self.progress = load_progress()

    def draw(self, screen, current_screen, clicked_option=None):
        if not self.visible:
            return

        # Background
        pygame.draw.rect(screen, (0, 128, 128), (0, 0, self.width, screen.get_height()))

        # Title
        title = self.title_font.render("Inside Immune", True, (255, 255, 255))
        screen.blit(title, (20, 40))

        # Options
        y_offset = 120  # Start below the titles with some padding
        spacing = 50  # Space between each menu option
        for i, option in enumerate(self.options):
            # Determine color and font based on option state
            if option == "Level 2" and not self.progress.get("level1_completed", False):
                # Grey out Level 2 if Level 1 is not completed
                font = self.font  # Regular font
                color = (169, 169, 169)  # Grey
            elif option == clicked_option:
                font = self.menu_font  # Use bold font for clicked option
                color = (255, 140, 0)  # Golden yellow for clicked option
            elif option == current_screen:
                font = self.menu_font  # Bold the current screen
                color = (255, 140, 0)  # Golden yellow for the current screen
            else:
                font = self.font  # Regular font for others
                color = (255, 255, 255)  # White for others

            text = font.render(option, True, color)
            screen.blit(text, (20, y_offset + i * spacing))

    def toggle(self):
        self.visible = not self.visible

    def handle_event(self, event):
        if not self.visible or event.type != pygame.MOUSEBUTTONDOWN:
            return None

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < self.width:  # Check if the click is within the sidebar
            y_offset = 120  # Starting Y position of options
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(20, y_offset + i * 50, self.width - 40, 30)

                if option_rect.collidepoint(mouse_x, mouse_y):
                    # Prevent access to Level 2 if locked
                    if option == "Level 2" and not self.progress.get("level1_completed", False):
                        return None  # Ignore the click
                    return option  # Return the clicked option text
        return None