import pygame

class BaseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.previous_width = screen.get_width()
        self.previous_height = screen.get_height()

    def run(self):
        raise NotImplementedError("Each screen must implement its own 'run' method.")

    def draw(self):
        raise NotImplementedError("Each screen must implement its own 'draw' method.")

    def handle_event(self, event):
        pass

    def reposition_elements(self):
        new_width = self.screen.get_width()
        new_height = self.screen.get_height()

        width_ratio = new_width / self.previous_width
        height_ratio = new_height / self.previous_height

        self.update_positions(width_ratio, height_ratio)
        self.previous_width = new_width
        self.previous_height = new_height

    def update_positions(self, width_ratio, height_ratio):
        pass


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {}
        self.active_screen = None
        self.modal_active = False
        self.modal_content = None
        self.modal_rect = None
        self.font = pygame.font.SysFont("Arial", 24)
        self.modal_close_callback = None

    def register_screen(self, name, screen_class, *args, **kwargs):
        self.screens[name] = (screen_class, args, kwargs)

    def set_active_screen(self, name):
        if name in self.screens:
            screen_class, args, kwargs = self.screens[name]
            self.active_screen = screen_class(self.screen, *args, **kwargs)
        elif name == "Exit Game":
            pygame.quit()
            exit()
        else:
            raise ValueError(f"Screen '{name}' is not registered.")

    def run_active_screen(self):
        if self.active_screen:
            self.active_screen.run()

    def draw_active_screen(self):
        if self.active_screen:
            self.active_screen.draw()
        if self.modal_active:
            self.draw_modal()

    def handle_event(self, event):
        if self.modal_active:
            if event.type == pygame.MOUSEBUTTONDOWN and self.modal_rect.collidepoint(event.pos):
                self.close_modal()
            return  # Block other events when the modal is active
        if self.active_screen:
            self.active_screen.handle_event(event)

    def reposition_active_screen(self):
        if self.active_screen:
            self.active_screen.reposition_elements()

    def show_modal(self, content, close_callback=None):
        self.modal_active = True
        self.modal_content = content
        self.modal_close_callback = close_callback

        # Modal dimensions
        modal_width = 800
        modal_height = 100
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.modal_rect = pygame.Rect(
            (screen_width - modal_width) // 2,
            (screen_height - modal_height) // 2 + 400,
            modal_width,
            modal_height
        )

    def close_modal(self):
        self.modal_active = False
        self.modal_content = None
        self.modal_rect = None
        if self.modal_close_callback:
            self.modal_close_callback()
            self.modal_close_callback = None
            
    def draw_modal(self):
        if not self.modal_active or not self.modal_content:
            return

        # Draw modal background and border
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect)  # Modal background
        pygame.draw.rect(self.screen, (0, 0, 0), self.modal_rect, 2)    # Modal border

        # Prepare the font and calculate text positions
        font = pygame.font.SysFont("Arial", 18)
        max_width = self.modal_rect.width - 20  # Padding inside the modal
        wrapped_lines = self.wrap_text(self.modal_content, font, max_width)

        line_height = font.get_linesize()
        y_offset = self.modal_rect.top + 10  # Padding from the top

        # Draw each line
        for line in wrapped_lines:
            if y_offset + line_height > self.modal_rect.bottom - 10:  # Prevent overflow
                break
            text_surface = font.render(line, True, (0, 0, 0))  # Render text
            self.screen.blit(text_surface, (self.modal_rect.left + 10, y_offset))  # Left-align with padding
            y_offset += line_height

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
        if current_line:
            lines.append(current_line.strip())  # Add the last line

        return lines