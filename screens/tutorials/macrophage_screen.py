import os
import pygame
import sys
import math
from objects.oracle import Oracle
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen


class MacrophageScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False
        self.step = 0
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.sidebar_width = 400
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.semi_title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.oracle = Oracle(self.sidebar_width)
        self.oracle.display_message("Click on the stars!", self.screen)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load(self.resource_path("assets/tutorials/macrophage.png"))

        # Load and scale the star icons
        self.original_star_image = pygame.image.load(self.resource_path("assets/icons/star.png"))
        self.grey_star_image = pygame.image.load(self.resource_path(("assets/icons/grey_star.png")))
        self.star_image = pygame.transform.scale(self.original_star_image, (30, 30))
        self.grey_star_image = pygame.transform.scale(self.grey_star_image, (30, 30))

        # Load and set up the continue button
        self.continue_button_image = pygame.image.load(self.resource_path("assets/icons/continue.png"))
        self.continue_button_image = pygame.transform.scale(self.continue_button_image, (100, 50))
        self.continue_button_rect = self.continue_button_image.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        )
        self.show_continue_button = False  # Flag to display the continue button
        self.shimmer_done = False

        # Define button locations and their corresponding context text
        self.buttons = [
            {
                "relative_position": (70, 100),
                "context": "The macrophage is one of your first lines of defense against pathogens.",
                "clicked": False,
            },
            {
                "relative_position": (100, 400),
                "context": "Vesicles, called lysosomes, containing hydrolytic enzymes merge with the phagosome, causing the degradation of the pathogen.",
                "clicked": False,
            },
            {
                "relative_position": (415, 250),
                "context": "The macrophage can recognize, bind to, and engulf foreign pathogens.",
                "clicked": False,
            },
            {
                "relative_position": (550, 400),
                "context": "Once broken down, the material is then expelled from the cell.",
                "clicked": False,
            },
            {
                "relative_position": (550, 205),
                "context": "This forms a ‘phagosome’, inside the cytoplasm of the phagocyte.​",
                "clicked": False,
            },
        ]

        # Prepend "Dr. Tomato:" to all contexts
        for button in self.buttons:
            button["context"] = f"Dr. Tomato: {button['context']}"

        self.clicked_button_index = None

        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.reposition_elements()

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0

        # Resize the image dynamically
        self.image = pygame.transform.scale(
            self.original_image,
            (int((screen_width - self.sidebar_width) * 0.6), int(screen_height * 0.6)),
        )
        self.image_rect = self.image.get_rect(
            center=(
                (screen_width - self.sidebar_width) // 2 + self.sidebar_width,
                screen_height // 2,
            )
        )

        # Recalculate button positions
        for button in self.buttons:
            relative_x, relative_y = button["relative_position"]
            button["position"] = (self.image_rect.left + relative_x, self.image_rect.top + relative_y)

        # Adjust the continue button position
        self.continue_button_rect = self.continue_button_image.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        )

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if clicking outside the modal
            if self.clicked_button_index is not None:
                modal_width = self.image_rect.width
                modal_height = 100
                modal_x = (self.screen.get_width() - modal_width) // 2
                modal_y = self.screen.get_height() - modal_height - 50

                if not (modal_x <= mouse_pos[0] <= modal_x + modal_width and
                        modal_y <= mouse_pos[1] <= modal_y + modal_height):
                    self.clicked_button_index = None
                    self.shimmer_done = False
                    return

            # Handle star button clicks
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (40, 40))
                if button_rect.collidepoint(mouse_pos):
                    if self.clicked_button_index != i:
                        self.clicked_button_index = i
                        self.shimmer_done = False  # Reset shimmer
                        self.clicked_button_index_changed = True  # Ensure shimmer restarts
                    button["clicked"] = True

                    if all(b["clicked"] for b in self.buttons):
                        self.show_continue_button = True

            # Handle continue button click
            if self.show_continue_button and self.continue_button_rect.collidepoint(mouse_pos):
                self.completed = True
                self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.completed = True
                self.running = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def draw_modal_with_pulsing_context(self):
        if self.clicked_button_index is None:
            return

        # Get the current button context
        context = self.buttons[self.clicked_button_index]["context"]

        # Separate "Dr. Tomato:" and the rest of the context
        speaker = "Dr. Tomato:"
        message = context.replace(speaker, "").strip()

        # Set modal dimensions
        modal_width = self.image_rect.width
        base_font_size = 20
        max_font_size = 24
        pulse_duration = 1000  # Slower pulse duration
        total_pulses = 2  # Number of pulses

        # Handle pulsing effect
        if self.pulse_start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.pulse_start_time
            current_pulse = elapsed_time // pulse_duration

            if current_pulse < total_pulses:
                pulse_progress = (elapsed_time % pulse_duration) / pulse_duration
                scale_factor = 1 + 0.2 * math.sin(pulse_progress * math.pi)
                font_size = min(int(base_font_size * scale_factor), max_font_size)
                pulsing_font = pygame.font.SysFont("Arial", font_size)
            else:
                pulsing_font = pygame.font.SysFont("Arial", base_font_size)
                self.pulse_start_time = None
        else:
            pulsing_font = pygame.font.SysFont("Arial", base_font_size)

        # Wrap the message text to fit within modal width
        wrapped_message = self.wrap_text(message, pulsing_font, modal_width - 20)
        text_height = pulsing_font.size(speaker)[1] + sum(
            pulsing_font.size(line)[1] + 5 for line in wrapped_message
        )  # Add spacing for lines
        modal_height = max(100, text_height + 40)  # Ensure a minimum modal height

        # Keep the modal lower on the screen
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = self.screen.get_height() - modal_height - 50  # Original lower position

        # Draw modal background (white) and border
        pygame.draw.rect(self.screen, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Render the speaker ("Dr. Tomato:") at the top of the modal
        speaker_surface = pulsing_font.render(speaker, True, (0, 0, 0))
        self.screen.blit(speaker_surface, (modal_x + 10, modal_y + 10))

        # Render the wrapped message text
        y_offset = modal_y + 20 + pulsing_font.size(speaker)[1]  # Below the speaker
        for line in wrapped_message:
            text_surface = pulsing_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (modal_x + 10, y_offset))
            y_offset += pulsing_font.get_height() + 5  # Add line spacing

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw the title
        effective_center_x = (
            (self.screen.get_width() - (self.sidebar.width if self.sidebar.visible else 0)) // 2
            + (self.sidebar.width if self.sidebar.visible else 0)
        )
        title_text = self.title_font.render("Macrophage Information", True, (0, 0, 139))
        title_rect = title_text.get_rect(center=(effective_center_x, 50))
        self.screen.blit(title_text, title_rect)

        guide_text = self.semi_title_font.render("Click on the stars!", True, (0, 0, 139))
        guide_rect = guide_text.get_rect(center=(effective_center_x, 100))
        self.screen.blit(guide_text, guide_rect)

        # Draw the macrophage tutorial image with a black border
        border_thickness = 5  # Thickness of the border
        border_rect = self.image_rect.inflate(border_thickness * 2, border_thickness * 2)
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect)  # Draw the black border
        self.screen.blit(self.image, self.image_rect)  # Blit the original image on top

        # Draw the star buttons with gleaming effect
        for button in self.buttons:
            self.draw_star_with_gleaming(self.screen, button["position"], button["clicked"])

        # Draw the continue button if applicable
        if self.show_continue_button:
            self.screen.blit(self.continue_button_image, self.continue_button_rect)

        # Draw the Oracle
        self.oracle.draw(self.screen)
        self.oracle.draw_message(self.screen)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Macrophage Information")

        self.draw_modal_with_shimmering_context()
    
    def draw_star_with_gleaming(self, screen, position, is_clicked):
        if not is_clicked:
            elapsed_time = pygame.time.get_ticks() % 1000
            scale_factor = 1 + 0.1 * math.sin((elapsed_time / 1000) * 2 * math.pi)
            gleaming_star = pygame.transform.scale(
                self.star_image,
                (int(self.star_image.get_width() * scale_factor), int(self.star_image.get_height() * scale_factor)),
            )
            gleaming_rect = gleaming_star.get_rect(center=(position[0] + 28, position[1] + 28))
            screen.blit(gleaming_star, gleaming_rect)
        else:
            screen.blit(self.grey_star_image, position)

    def draw_modal_with_shimmering_context(self):
        if self.clicked_button_index is None:
            return

        # Get the current button context
        context = self.buttons[self.clicked_button_index]["context"]

        # Separate "Dr. Tomato:" and the rest of the context
        speaker = "Dr. Tomato:"
        message = context.replace(speaker, "").strip()

        # Set modal dimensions
        modal_width = self.image_rect.width
        font = pygame.font.SysFont("Arial", 20)
        wrapped_message = self.wrap_text(message, font, modal_width - 20)
        text_height = font.size(speaker)[1] + sum(
            font.size(line)[1] + 5 for line in wrapped_message
        )
        modal_height = max(100, text_height + 40)

        # Position modal on screen
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = self.screen.get_height() - modal_height - 50

        # Draw modal background and border
        pygame.draw.rect(self.screen, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Render speaker
        speaker_surface = font.render(speaker, True, (0, 0, 0))
        self.screen.blit(speaker_surface, (modal_x + 10, modal_y + 10))

        # Shimmering effect variables
        max_highlight_length = 45  # Characters highlighted at once
        shimmer_speed = 0.05  # Speed of shimmer
        total_characters = sum(len(line) for line in wrapped_message)

        # Initialize shimmer tracking
        if not hasattr(self, "shimmer_start_time") or self.clicked_button_index_changed:
            self.shimmer_start_time = pygame.time.get_ticks()
            self.shimmer_done = False
            self.clicked_button_index_changed = False

        elapsed_time = pygame.time.get_ticks() - self.shimmer_start_time
        shimmer_position = int(elapsed_time * shimmer_speed)

        # If shimmer is done, render static modal
        if shimmer_position >= total_characters + max_highlight_length:
            self.shimmer_done = True

        if not self.shimmer_done:
            # Render wrapped context text with shimmer
            full_text = " ".join(wrapped_message)  # Combine wrapped lines into a single block
            y_offset = modal_y + 20 + font.size(speaker)[1]
            shimmer_start = max(0, shimmer_position - max_highlight_length)
            shimmer_end = shimmer_position

            char_index = 0  # Global character index for shimmer effect

            for line in wrapped_message:
                modal_x = (self.screen.get_width() - modal_width) // 2  # Reset modal_x for each line

                for char in line:
                    if not char.strip():  # Skip whitespace
                        try:
                            modal_x += font.size(char)[0]
                        except pygame.error:
                            modal_x += 5  # Handle width calculation issues gracefully
                        char_index += 1
                        continue

                    # Determine color for shimmer effect
                    if shimmer_start <= char_index < shimmer_end:
                        color = (255, 140, 0)  # Shimmer color
                    else:
                        color = (0, 0, 0)  # Default black text

                    try:
                        char_surface = font.render(char, True, color)
                        if char_surface.get_width() > 0:  # Avoid blitting zero-width surfaces
                            self.screen.blit(char_surface, (modal_x + 10, y_offset))
                            modal_x += char_surface.get_width()
                    except pygame.error:
                        continue

                    char_index += 1  # Increment global character index

                try:
                    y_offset += font.get_height() + 5
                except pygame.error:
                    y_offset += 5

            # Stop shimmering once the entire text block is processed
            if shimmer_position >= len(full_text) + max_highlight_length:
                self.shimmer_done = True
        else:
            # Render static black text
            y_offset = modal_y + 20 + font.size(speaker)[1]
            for line in wrapped_message:
                modal_x = (self.screen.get_width() - modal_width) // 2  # Reset modal_x for each line
                for char in line:
                    if not char.strip():  # Skip whitespace
                        try:
                            modal_x += font.size(char)[0]
                        except pygame.error:
                            modal_x += 5
                        continue

                    try:
                        # Render character in black
                        char_surface = font.render(char, True, (0, 0, 0))
                        if char_surface.get_width() > 0:
                            self.screen.blit(char_surface, (modal_x + 10, y_offset))
                            modal_x += char_surface.get_width()
                    except pygame.error:
                        continue

                try:
                    y_offset += font.get_height() + 5
                except pygame.error:
                    y_offset += 5

    def hsv_to_rgb(self, h, s, v):
        h = h * 6.0
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = {
            0: (v, t, p),
            1: (q, v, p),
            2: (p, v, t),
            3: (p, q, v),
            4: (t, p, v),
            5: (v, p, q),
        }[i % 6]
        return int(r * 255), int(g * 255), int(b * 255)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.manager.draw_active_screen()
            pygame.display.flip()

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)