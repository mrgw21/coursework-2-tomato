import pygame
from screens.screen_manager import ScreenManager
from levels.level1 import Level1
from levels.level2 import Level2
from screens.controls import ControlsScreen
from screens.about import AboutScreen
from screens.homescreen import HomeScreen
from screens.quizzes import QuizzesScreen
# from screens.settings import SettingsScreen
from screens.preliminary import PreliminaryScreen
from screens.leaderboards.leaderboard_level1 import LeaderboardLevel1
from screens.leaderboards.leaderboard_level2 import LeaderboardLevel2
from screens.tutorials.bacteria_screen import BacteriaScreen
from screens.tutorials.macrophage_screen import MacrophageScreen
from screens.tutorials.virus_screen import VirusScreen
from data.save_manager import load_progress
import os
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    icon = pygame.image.load(resource_path("assets/images/insideimmuneicon2.png")).convert_alpha()
    icon = pygame.transform.smoothscale(icon, (64, 64))
    icon = round_corners(icon, 10)
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Inside Immune")

    progress = load_progress()

    # Create ScreenManager and register all screens
    manager = ScreenManager(screen)
    manager.register_screen("Home", HomeScreen, manager)
    manager.register_screen("Preliminary", PreliminaryScreen, manager)
    manager.register_screen("Introduction", Level1, manager, True, 0)
    manager.register_screen("Level 1", Level1, manager, False, 8)
    manager.register_screen("Level 2", Level2, manager, False, 8)
    manager.register_screen("Quizzes", QuizzesScreen, manager)
    manager.register_screen("Leaderboards", LeaderboardLevel1, manager)
    manager.register_screen("Leaderboard Level 2", LeaderboardLevel2, manager)
    # manager.register_screen("Settings", SettingsScreen, manager)
    manager.register_screen("Controls", ControlsScreen, manager)
    manager.register_screen("About", AboutScreen, manager)
    manager.register_screen("bacteria_tutorial", BacteriaScreen, manager)
    manager.register_screen("macrophage_tutorial", MacrophageScreen, manager)
    manager.register_screen("virus_tutorial", VirusScreen, manager)

    # Set the starting screen
    manager.set_active_screen("Home")

    sidebar_options = {
        "Home": "Home",
        "Introduction": "Preliminary",
        "Level 1": "Level 1",
        "Level 2": "Level 2",
        "Quizzes": "Quizzes",
        "Leaderboards": "Leaderboards",
        # "Settings": "Settings",
        "Controls": "Controls",
        "About": "About",
    }

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                manager.reposition_active_screen()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    active_screen = manager.active_screen
                    if hasattr(active_screen, "sidebar") and active_screen.sidebar:
                        active_screen.sidebar.toggle()
                        if hasattr(active_screen, "handle_sidebar_toggle"):
                            active_screen.handle_sidebar_toggle()  # Adjust elements for sidebar
            else:
                active_screen = manager.active_screen
                if active_screen:
                    # Check if it's a tutorial screen
                    if isinstance(active_screen, MacrophageScreen) or isinstance(active_screen, VirusScreen) or isinstance(active_screen, BacteriaScreen):
                        active_screen.handle_event(event)
                        # Check completion flag
                        if hasattr(active_screen, "completed") and active_screen.completed:
                            manager.register_screen("Level 1 " + str(active_screen.step + 1), Level1, manager, True, active_screen.step + 1)
                            manager.set_active_screen("Level 1 " + str(active_screen.step + 1))
                    else:
                        # Sidebar handling for other screens
                        if hasattr(active_screen, "sidebar") and active_screen.sidebar.visible:
                            clicked_option = active_screen.sidebar.handle_event(event)
                            if clicked_option:
                                if clicked_option == "Exit Game":
                                    pygame.quit()
                                    exit()
                                elif clicked_option in sidebar_options:
                                    manager.set_active_screen(sidebar_options[clicked_option])
                                    break
                        else:
                            # Pass event to the active screen if no sidebar
                            active_screen.handle_event(event)

        # Run the active screen
        if manager.active_screen:
            manager.run_active_screen()

        # Clear screen and draw
        screen.fill((255, 255, 255))
        manager.draw_active_screen()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()

def get_sidebar_option(mouse_pos, options_mapping):
    x, y = mouse_pos
    sidebar_width = 400  # Ensure this matches your actual sidebar width
    y_offset = 120  # Starting Y position of the first option
    spacing = 50  # Spacing between each option in the sidebar

    if x < sidebar_width:  # Check if the click is within the sidebar area
        for index, (option_text, screen_name) in enumerate(options_mapping.items()):  # Correct unpacking
            # Define the rectangle for each option
            option_rect = pygame.Rect(20, y_offset + index * spacing, sidebar_width - 40, 30)
            if option_rect.collidepoint(x, y):  # Check if the mouse is within this option's rectangle
                return screen_name
    return None  # Return None if no option was clicked


def load_pdf_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".jpg"):
            image = pygame.image.load(os.path.join(folder, filename)).convert()
            images.append(image)
    return images

def round_corners(surface, radius):
    size = surface.get_size()
    width, height = size

    # Ensure the radius is not too large
    if radius is None:
        radius = min(width, height) // 8  # Default: Slight rounding

    mask = pygame.Surface(size, pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, *size)

    # Draw rounded rectangle on the mask
    pygame.draw.rect(mask, (0, 0, 0, 0), rect)  # Clear
    pygame.draw.rect(mask, (255, 255, 255, 255), rect.inflate(-radius, -radius), border_radius=radius)

    # Create a new surface for the rounded icon
    rounded_surface = pygame.Surface(size, pygame.SRCALPHA)
    rounded_surface.blit(surface, (0, 0))  # Blit the original image
    rounded_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)  # Apply the rounded corners mask
    return rounded_surface

def resource_path(relative_path):
    try:
        # If running as a PyInstaller bundle, use _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Otherwise, use the current directory
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    main()