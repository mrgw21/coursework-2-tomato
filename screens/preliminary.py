import pygame
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar

class PreliminaryScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)
        self.bold_text_font = pygame.font.SysFont("Arial", 25, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 30, bold=True)

        # Sidebar setup
        self.sidebar = Sidebar()
        self.sidebar.visible = False

        # Load Dr. Tomato image
        self.image = pygame.image.load("assets/images/dr_tomato.png")

        # Scale the Dr. Tomato image while keeping proportions
        original_width, original_height = self.image.get_size()
        scale_factor = min(self.screen.get_width() // 6 / original_width, self.screen.get_height() // 3 / original_height)
        scaled_width = int(original_width * scale_factor)
        scaled_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.image_rect = self.image.get_rect()
        self.update_image_position()

        self.text_lines = [
            "Hello passionate learners! My name is",
            "Dr Tomato",
            "In this game, I will help you learn the",
            "fundamental of immune system and",
            "guide you how to play Inside Immune!",
            "",
            "In the next screen, please read and",
            "follow my instructions!",
        ]

        # Button configuration
        self.button_width = 300
        self.button_height = 80
        self.button_color = (255, 255, 255)
        self.button_border_color = (0, 0, 139)
        self.button_text_color = (0, 0, 0)
        self.button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.update_button_position()

        self.text_positions = []
        self.calculate_text_positions()
        self.running = True

    def update_image_position(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.image_rect.center = (
            self.screen.get_width() // 4 + sidebar_width // 2,
            self.screen.get_height() // 2,
        )

    def update_button_position(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.button_rect.center = (
            self.screen.get_width() // 2 + (sidebar_width // 2),
            self.screen.get_height() - 150,
        )

    def calculate_text_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)
        start_y = self.screen.get_height() // 3

        self.text_positions = [
            (center_x, start_y + i * 40) for i in range(len(self.text_lines))
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
                    elif event.key == pygame.K_RETURN:  # "Enter" key transitions to Introduction
                        self.running = False
                        self.manager.set_active_screen("Introduction")
                        return
                    elif event.key == pygame.K_m:
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.button_rect.collidepoint(event.pos):
                        self.running = False
                        self.manager.set_active_screen("Introduction")
                        return
                elif event.type == pygame.VIDEORESIZE:
                    self.reposition_elements(event.w, event.h)

                # Handle sidebar interactions
                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        self.manager.set_active_screen(option_clicked)
                        return

            self.draw()
            pygame.display.flip()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))

        # Draw Title Text
        title_text = self.title_font.render("Topic 1", True, (0, 0, 139))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, 80)))

        line_start = (sidebar_width + 200, 140)
        line_end = (self.screen.get_width() - 200, 140)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)

        # Draw Subtitle Line
        subtitle_text = self.title_font.render("Viral and Bacteria Response", True, (0, 0, 139))
        self.screen.blit(subtitle_text, subtitle_text.get_rect(center=(center_x, 200)))

        # Draw Dr. Tomato Image
        self.screen.blit(self.image, self.image_rect)

        # Draw Text Lines
        for i, line in enumerate(self.text_lines):
            if line == "Dr Tomato":
                text_surface = self.bold_text_font.render(line, True, (255, 0, 0))
            else:
                text_surface = self.text_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, text_surface.get_rect(center=self.text_positions[i]))

        # Draw Continue Button
        pygame.draw.rect(
            self.screen, self.button_border_color, self.button_rect, border_radius=10
        )  # Button border
        pygame.draw.rect(
            self.screen, self.button_color, self.button_rect.inflate(-6, -6), border_radius=10
        )  # Button fill
        button_text = self.button_font.render("Continue", True, self.button_text_color)
        self.screen.blit(button_text, button_text.get_rect(center=self.button_rect.center))

        # Draw Sidebar
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Topic 1")

    def handle_sidebar_toggle(self):
        self.update_image_position()
        self.update_button_position()
        self.calculate_text_positions()

    def reposition_elements(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.update_image_position()
        self.update_button_position()
        self.calculate_text_positions()

    def get_sidebar_option(self, mouse_pos, options):
        y_offset = 120
        spacing = 50
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)
            if option_rect.collidepoint(mouse_pos):
                return option
        return None