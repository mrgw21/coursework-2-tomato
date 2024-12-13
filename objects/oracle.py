import pygame
import os
import sys

class Oracle:
    def __init__(self, sidebar_width):
        # Load Oracle images
        self.image_default = pygame.image.load(self.resource_path("assets/images/dr_tomato.png"))  # Default image
        self.image_hover = pygame.image.load(self.resource_path("assets/images/dr_tomato.png"))  # Hover image
        self.image_click = pygame.image.load(self.resource_path("assets/images/dr_tomato.png"))  # Click image
        self.image = pygame.transform.scale(self.image_default, (250, 200))  # Adjusted size
        self.rect = self.image.get_rect()

        # Sidebar reference for positioning
        self.sidebar_width = sidebar_width

        # Initialize modal properties
        self.modal_rect = pygame.Rect(0, 0, 400, 300)  # Modal dimensions: 600x600
        self.show_modal = False

        # Set Oracle's initial position and modal position
        self.set_position()

        # Initialize message attributes
        self.message_surface = None
        self.message_rect = None
        self.message_bg_rect = None  # Background rect for the message
        self.font = pygame.font.SysFont("Arial", 24)  # Font for messages
        self.message = ""  # Default empty message

    def set_position(self):
        # Adjust Oracle position within the sidebar
        screen_height = pygame.display.get_surface().get_height()
        self.rect.bottom = screen_height - 10  # Margin from the bottom
        self.rect.x = self.sidebar_width // 2 - self.rect.width // 2  # Center horizontally in sidebar

        # Dynamically position modal (top right of Oracle)
        self.modal_rect.topleft = (
            self.rect.right + 10,  # Slight padding to the right of Oracle
            self.rect.top - self.modal_rect.height  # Align modal top-right
        )

    def draw(self, screen):
        # Draw Oracle image
        screen.blit(self.image, self.rect)

        # Draw modal if active
        if self.show_modal:
            pygame.draw.rect(screen, (220, 220, 220), self.modal_rect)  # White background
            pygame.draw.rect(screen, (0, 0, 0), self.modal_rect, 3)    # Black border

            # Render the message inside the modal
            if hasattr(self, "message") and self.message:
                font = pygame.font.SysFont("Arial", 18)
                max_line_width = self.modal_rect.width - 20  # Padding inside the modal
                lines = self.wrap_text(self.message, font, max_line_width)
                line_height = font.get_linesize()
                start_y = self.modal_rect.top + 10  # Vertical padding from top
                for i, line in enumerate(lines):
                    text_surface = font.render(line, True, (0, 0, 0))
                    text_x = self.modal_rect.left + 10  # Horizontal padding
                    text_y = start_y + i * line_height
                    if text_y + line_height > self.modal_rect.bottom - 10:  # Prevent overflow
                        break
                    screen.blit(text_surface, (text_x, text_y))

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:  # Add any remaining text as the last line
            lines.append(current_line.strip())
        return lines

    def handle_hover(self, mouse_pos):
        # Change image to hover state if mouse is over Oracle
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.transform.scale(self.image_hover, (250, 200))
        else:
            self.image = pygame.transform.scale(self.image_default, (250, 200))

    def handle_click(self, mouse_pos, cells, level):
        if any(cell.show_modal for cell in cells):
            return
        # Change image to click state and toggle modal visibility
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.transform.scale(self.image_click, (250, 200))
            self.show_modal = not self.show_modal  # Toggle modal visibility

            # Pause the game if Oracle's modal is opened
            if self.show_modal:
                level.paused = True
            else:
                level.paused = False
    
    def tutorial_handle_click(self, message):
        self.image = pygame.transform.scale(self.image_click, (250, 200))
        self.show_modal = not self.show_modal  # Toggle modal visibility

        # Assign the dynamic message for display in the modal
        if self.show_modal:
            self.message = message
        else:
            self.message = ""  # Clear the message when modal is closed
            

    def reset_image(self):
        # Reset to default image after a click
        self.image = pygame.transform.scale(self.image_default, (250, 200))

    def display_message(self, message, screen):
        self.message = message

        # Create the text surface
        self.message_surface = self.font.render(self.message, True, (0, 0, 0))  # Black text
        self.message_rect = self.message_surface.get_rect()
        
        # Position the text above the Oracle
        self.message_rect.topleft = (self.rect.x - 10, self.rect.top - 35)  # Display above Oracle

        # Create an oval background shape for the message
        padding = 30  # Padding around the text
        self.message_bg_rect = pygame.Rect(
            self.message_rect.x - padding,  # Left side with padding
            self.message_rect.y - padding,  # Top side with padding
            self.message_rect.width + padding * 2,  # Width with padding
            self.message_rect.height + padding * 2  # Height with padding
        )

    def draw_message(self, screen):
        if self.message_surface and self.message_bg_rect:
            # Draw the message background
            pygame.draw.ellipse(screen, (255, 255, 255), self.message_bg_rect)  # White background
            pygame.draw.ellipse(screen, (0, 0, 0), self.message_bg_rect, 2)  # Black border

            # Draw the message text
            screen.blit(self.message_surface, self.message_rect)
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)