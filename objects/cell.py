import os
import sys
import pygame
import random

class Cell:
    def __init__(self, position, center_pos=(0, 0)):
        self.image = pygame.image.load(self.resource_path("assets/images/final/uninfected_cell.png"))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 20, self.image.get_height() // 20))
        self.rect = self.image.get_rect()
        self.position = position
        self.state = True  # True means uninfected, False means infected
        self.health = "uninfected"  # Health status of the cell
        self.show_modal = False
        self.cell_number = position + 1  # Numbering for cells
        self.quiz = None 
        self.selected_option = None
        self.failed_attempts = 0
        self.quiz_locked = False  # Lock the quiz after correct or 3 failed attempts
        self.quiz_feedback = None
        self.is_tutorial = False

        self.hint_index = 0 # Start at first hint
        self.infection_timer = 0  # Timer for slowing infected cell attacks
        self.neighbors = []

        self.option_coords = []

        # Set initial position of the cell
        self.reposition(center_pos)

    def reposition(self, center_pos, spacing=30):
        # Diamond layout configuration
        row_layout = [3, 5, 7, 7, 7, 5, 3]  # Cells per row
        idx = 0

        # Calculate the total width and height of the diamond
        total_rows = len(row_layout)
        max_row_width = max(row_layout)
        diamond_width = max_row_width * spacing  # Total width of the diamond
        diamond_height = total_rows * spacing    # Total height of the diamond

        # Calculate the top-left corner of the diamond relative to the center
        diamond_top = center_pos[1] - diamond_height // 2 + 3
        diamond_left = center_pos[0] - diamond_width // 2 + 2

        # Get the specific position for the current cell
        idx = 0
        for row_index, row_count in enumerate(row_layout):
            y_pos = diamond_top + row_index * spacing
            x_start = diamond_left + (max_row_width - row_count) // 2 * spacing
            for col_index in range(row_count):
                x_pos = x_start + col_index * spacing
                if idx == self.position:  # Current cell's position
                    self.rect.x = x_pos
                    self.rect.y = y_pos
                    # Adjust rect size to ensure it aligns with cell dimensions
                    self.rect.width = spacing
                    self.rect.height = spacing
                    return
                idx += 1

    def get_collision_rect(self):
        base_rect = self.image.get_rect(center=self.rect.center)
        collision_rect = base_rect.inflate(-70, -70)
        return collision_rect

    def die(self):
        self.state = False
        self.health = "infected"
        self.image = pygame.image.load(self.resource_path("assets/images/final/infected_cell.png"))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 20, self.image.get_height() // 20))
        self.infection_timer = pygame.time.get_ticks()
    
    def draw(self, screen, sidebar_width, cells, level):
        # Recalculate the image's position to center it inside the rect
        image_x = self.rect.centerx - self.image.get_width() // 2
        image_y = self.rect.centery - self.image.get_height() // 2

        # Draw the image centered within the rect
        screen.blit(self.image, (image_x, image_y))

        # Optionally draw the collision rect for debugging
        # pygame.draw.rect(screen, (0, 255, 0), self.get_collision_rect(), 2)

        # If the modal is active, draw it
        if self.show_modal:
            self.draw_modal(screen, sidebar_width, cells, level)

    def draw_modal(self, screen, sidebar_width, cells, level):
        # Define modal dimensions
        modal_width = 550
        modal_height = 700

        # Position the modal to the left, always to the right of the sidebar
        screen_height = screen.get_height()
        padding = 10  # Add some padding between the modal and the sidebar
        modal_x = sidebar_width + padding
        modal_y = (screen_height - modal_height) // 2  # Vertically center the modal

        # Draw modal background and border
        pygame.draw.rect(screen, (220, 220, 220), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Font for text
        font = pygame.font.SysFont("Arial", 20)

        # Close button
        close_button_width = 90
        close_button_height = 25
        close_button_x = modal_x + modal_width - close_button_width - 10
        close_button_y = modal_y + 10

        # Draw the button background (same as modal color)
        pygame.draw.rect(screen, (220, 220, 220), (close_button_x, close_button_y, close_button_width, close_button_height))
        pygame.draw.rect(screen, (204, 0, 0), (close_button_x, close_button_y, close_button_width, close_button_height), 2)

        # Render the button text in red
        close_button_text = font.render("X (ESC)", True, (204, 0, 0))
        text_rect = close_button_text.get_rect(
            center=(close_button_x + close_button_width // 2, close_button_y + close_button_height // 2)
        )
        screen.blit(close_button_text, text_rect)

        # Handle close button click detection
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if (close_button_x <= mouse_pos[0] <= close_button_x + close_button_width and
                close_button_y <= mouse_pos[1] <= close_button_y + close_button_height):
            if mouse_pressed[0]:  # Left mouse button pressed
                self.reset_quiz_state()
                self.show_modal = False  # Close the modal
                level.paused = False

        # Display cell information
        cell_number_text = f"Cell #{self.cell_number}"
        health_text = f"Health: {self.health}"
        info_text = self.get_info_text()

        content_start_y = close_button_y + close_button_height + 20

        # Display cell number and health
        screen.blit(font.render(cell_number_text, True, (0, 0, 0)), (modal_x + 10, content_start_y))
        screen.blit(font.render(health_text, True, (0, 0, 0)), (modal_x + 10, content_start_y + 30))

        # Draw cell image
        cell_image_path = "assets/images/final/dead_cell.png" if self.health == "dead" else "assets/images/final/infected_cell.png"
        cell_image = pygame.image.load(level.resource_path(cell_image_path))
        cell_image = pygame.transform.scale(cell_image, (300, 300))
        screen.blit(cell_image, (modal_x + (modal_width // 2) - 150, content_start_y))

        # Draw quiz if applicable
        if self.quiz:
            current_y = self.draw_quiz(screen, modal_x, modal_y, content_start_y + 250, modal_width)

            # Draw feedback (including hints) below the options
            if hasattr(self, "quiz_feedback") and self.quiz_feedback:
                # Create white box for feedback
                feedback_box_width = modal_width - 20
                feedback_box_x = modal_x + 10
                feedback_box_y = current_y + 20  # Place below the quiz options

                pygame.draw.rect(screen, (255, 255, 255), (feedback_box_x, feedback_box_y, feedback_box_width, 100))
                pygame.draw.rect(screen, (0, 0, 0), (feedback_box_x, feedback_box_y, feedback_box_width, 100), 2)

                # Add "Dr. Tomato:" at the top of the hint box
                speaker_text = "Dr. Tomato:"
                speaker_surface = font.render(speaker_text, True, (0, 0, 0))
                screen.blit(speaker_surface, (feedback_box_x + 10, feedback_box_y + 10))

                # Render the hint text inside the box
                feedback_text = self.quiz_feedback["message"]
                feedback_color = self.quiz_feedback["color"]

                # Wrap and draw feedback text
                feedback_lines = self.wrap_text(feedback_text, font, feedback_box_width - 20)
                current_y = feedback_box_y + 40  # Start below "Dr. Tomato:"
                for line in feedback_lines:
                    rendered_line = font.render(line, True, feedback_color)
                    screen.blit(rendered_line, (feedback_box_x + 10, current_y))
                    current_y += 25  # Line spacing
    
    def draw_quiz(self, screen, modal_x, modal_y, start_y, modal_width):
        font = pygame.font.SysFont('Arial', 18)
        quiz = self.quiz

        # Question text
        question_text = self.wrap_text(quiz["question"], font, modal_width - 20)
        current_y = start_y

        # Display the question text
        for line in question_text:
            rendered_text = font.render(line, True, (0, 0, 0))
            screen.blit(rendered_text, (modal_x + 10, current_y))
            current_y += 25  # Line spacing for wrapped lines

        # Add spacing between the question and the first option
        current_y += 20

        new_option_coords = []  # Temporary list to store new coordinates
        for i, option in enumerate(quiz["options"]):
            # Vertical position for this option's radio button
            option_y = current_y  # Align the radio button with the first line of option text

            # Determine the color based on selection
            if hasattr(self, "selected_option") and self.selected_option == option:
                if option["is_correct"]:
                    circle_color = (0, 128, 128)  # Green for correct
                    text_color = (0, 128, 128)
                else:
                    circle_color = (204, 0, 0)  # Red for incorrect
                    text_color = (204, 0, 0)
            else:
                circle_color = (220, 220, 220)  # Modal background color (default filling)
                text_color = (0, 0, 0)

            # Draw filled circle for the radio button
            circle_x = modal_x + 20  # Left margin for the radio button
            pygame.draw.circle(screen, circle_color, (circle_x, option_y + 10), 10, 0)  # Filled circle
            pygame.draw.circle(screen, (0, 0, 0), (circle_x, option_y + 10), 10, 1)  # Outline circle

            # Wrap and render the option text
            wrapped_text = self.wrap_text(option["text"], font, modal_width - 60)  # Account for left margin
            text_x = circle_x + 20  # Offset the text to the right of the radio button
            for line in wrapped_text:
                rendered_text = font.render(line, True, text_color)
                screen.blit(rendered_text, (text_x, current_y))
                current_y += 25  # Line spacing for wrapped lines

            # Update the Y-position for the next option
            current_y += 10  # Add extra spacing between options

            # Store the clickable area for this option
            new_option_coords.append({"circle": (circle_x, option_y + 10), "radius": 10, "option": option})

        # Update `option_coords` to reflect new positions
        self.option_coords = new_option_coords

        return current_y

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] < max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
    
    def reset_quiz(self):
        self.hint_index = 0
        self.selected_option = None

    def handle_radio_button_click(self, screen, mouse_pos, cells, level):
        # If the modal is not open or options are missing, return early
        if not self.show_modal or not hasattr(self, "option_coords"):
            return

        # Prevent further interaction if locked (3 failed attempts or correct answer)
        if hasattr(self, "quiz_locked") and self.quiz_locked and not level.tutorial_phase:
            return

        for option_data in self.option_coords:
            circle_x, circle_y = option_data["circle"]
            radius = option_data["radius"]
            distance = ((mouse_pos[0] - circle_x) ** 2 + (mouse_pos[1] - circle_y) ** 2) ** 0.5
            if distance <= radius:
                # Avoid re-processing the same option click
                if self.selected_option == option_data["option"]:
                    return  # Ignore duplicate clicks

                # Process the new selected option
                self.selected_option = option_data["option"]
                self.handle_quiz_answer(option_data["option"], level)
                break

    def draw_wrapped_text(self, screen, text, font, x, y, max_width):
        words = text.split(' ')
        space = font.size(' ')[0]
        line = []
        line_width = 0
        for word in words:
            word_width = font.size(word)[0]
            if line_width + word_width > max_width:
                screen.blit(font.render(' '.join(line), True, (0, 0, 0)), (x, y))
                y += font.get_height()
                line = [word]
                line_width = word_width + space
            else:
                line.append(word)
                line_width += word_width + space
        if line:
            screen.blit(font.render(' '.join(line), True, (0, 0, 0)), (x, y))
    
    def get_info_text(self):
        return "Cells protect the body from pathogens."

    def handle_click(self, mouse_pos, cells, level):
        if self.health == "uninfected" or self.health == "dead":
            return

        if self.rect.collidepoint(mouse_pos):
            # Close modals for all other cells and reset their quiz states
            for cell in cells:
                if cell != self:
                    cell.reset_quiz_state()

            # Open modal for the current cell
            self.show_modal = True
            level.paused = True
    
    def handle_quiz_answer(self, selected_option, level):
        current_time = pygame.time.get_ticks()

        # Prevent further interaction if locked
        if hasattr(self, "quiz_locked") and self.quiz_locked:
            return

        if selected_option["is_correct"]:
            self.quiz_feedback = {
                "message": "Correct! You've saved this cell.",
                "color": (0, 128, 128),
            }
            self.stop_infection_and_neighbors()  # Stops infection spread.
            self.feedback_timer = current_time  # Start feedback timer.
            if level.points == 0:
                level.add_points(100)
            else:
                level.add_points(110)
            self.show_modal = True
            self.quiz_locked = True  # Lock only after a correct answer
        else:
            # Wrong answer: Increment attempts
            self.failed_attempts += 1
            hints = self.quiz.get("hints", [])
            if self.hint_index < len(hints):
                hint_message = hints[self.hint_index]
                self.quiz_feedback = {"message": f"{hint_message}", "color": (204, 0, 0)}
                self.hint_index += 1
            else:
                # Lock only after 3 failed attempts
                if self.failed_attempts >= 3:
                    self.quiz_feedback = {
                        "message": "You have used all 3 attempts. No more hints.",
                        "color": (204, 0, 0),
                    }
                    self.quiz_locked = True
                    self.show_modal = True
                    self.feedback_timer = current_time  # Start feedback timer
            level.add_points(-10)

        # Ensure the modal remains open during feedback
        level.paused = True

    def infect_neighbors(self, level):
        # Use the actual number of neighbors to limit infection spread
        if level.tutorial_phase:
            return

        if not self.neighbors:
            return  # Skip if the cell has no neighbors

        # Calculate max neighbors to infect as a fraction of total neighbors
        max_neighbors_to_infect = max(1, len(self.neighbors) // 2)  # Infect up to half of the neighbors, but at least 1
        neighbors_to_infect = random.sample(self.neighbors, min(max_neighbors_to_infect, len(self.neighbors)))

        for neighbor in neighbors_to_infect:
            if neighbor.health == "uninfected":
                neighbor.die()
                level.add_points(-10)

    def update_infection(self, level):
        if self.health != "infected" or self.infection_timer is None or level.tutorial_phase:
            return
        # Ensure tutorial pathogens cannot spread infection
        current_time = pygame.time.get_ticks()
        infection_delay = 4000  # Set delay to 4 seconds (adjust as needed)

        if current_time - self.infection_timer > infection_delay:
            # Prevent infection spread from tutorial pathogens
            self.infect_neighbors(level)
            self.infection_timer = current_time  # Reset timer

    def stop_infection(self):
        self.state = False  # Ensure the cell is marked as no longer infectious
        self.health = "dead"  # Update health status
        self.image = pygame.image.load(self.resource_path("assets/images/final/dead_cell.png"))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 20, self.image.get_height() // 20))
        self.infection_timer = None  # Disable infection spread

    def stop_infection_and_neighbors(self):
        self.stop_infection()  # Stop the infection of this cell
        for neighbor in self.neighbors:
            if neighbor.health == "infected":
                # Only stop the spread but do not reset the health or state of infected neighbors
                neighbor.infection_timer = None  # Stop infection spread from this neighbor
    
    def reset_quiz_state(self):
        self.hint_index = 0
        self.quiz_feedback = None
        self.selected_option = None
        self.show_modal = False
        self.failed_attempts = 0
        self.quiz_locked = False
        self.feedback_timer = None  # Reset the feedback timer
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)