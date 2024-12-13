import pygame
import random
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar
from data.quizzes import quizzes

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Arial", 25)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)  # Button background
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(
            text_surface,
            (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2)
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class QuizzesScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        # Button colors
        self.colours = [(0, 0, 139), (255, 140, 0), (0, 128, 128), (255, 130, 180)]
        self.buttons = []

        # Initial state
        self.running = True
        self.sidebar_animation_speed = 20
        self.update_button_positions()

    def update_button_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)
        center_y = self.screen.get_height() // 2 + 30
        square_size_x = (self.screen.get_width() - sidebar_width - 300) // 2
        square_size_y = (self.screen.get_height() - 300) // 2

        self.buttons = [
            Button(center_x - square_size_x - 10, center_y + 10, square_size_x, square_size_y, "Comparisons", "Comparisons"),
            Button(center_x - square_size_x - 10, center_y - 10 - square_size_y, square_size_x, square_size_y, "Viruses", "Viruses"),
            Button(center_x + 10, center_y + 10, square_size_x, square_size_y, "Bacteria", "Bacteria"),
            Button(center_x + 10, center_y - 10 - square_size_y, square_size_x, square_size_y, "Immune System", "Immune System"),
        ]

    def toggle_sidebar(self):
        self.sidebar.visible = not self.sidebar.visible
        self.sidebar.is_animating = True
        self.update_button_positions()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        # Draw background and title
        self.screen.fill((255, 255, 255))  # Background
        title_text = self.title_font.render("Quizzes", True, (0, 0, 139))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, 100)))

        line_start = (sidebar_width + 20, 140)
        line_end = (self.screen.get_width() - 20, 140)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)

        # Draw sidebar if visible
        if self.sidebar.visible or self.sidebar.is_animating:
            self.sidebar.draw(self.screen, "Quizzes")

        # Draw buttons
        for button, color in zip(self.buttons, self.colours):
            button.draw(self.screen, color)

    def run_quiz(self, category):
        category_questions = [q for q in quizzes if q["category"] == category]
        correct_answers = 0
        quiz_index = 0

        while quiz_index < 10 and quiz_index < len(category_questions):
            active_question = category_questions[quiz_index]
            active_question_text = active_question["question"]
            active_question_options = active_question["options"]
            random.shuffle(active_question_options)

            # Draw question and options
            self.screen.fill((255, 255, 255))  # Clear screen
            question_surface = self.title_font.render(active_question_text, True, (0, 0, 0))
            x_question = (self.screen.get_width() - question_surface.get_width()) // 2
            self.screen.blit(question_surface, (x_question, 50))

            # Draw answer options
            option_buttons = []
            x = self.screen.get_width() // 2 - 250
            y_offset = 250
            for i, option in enumerate(active_question_options):
                button = Button(x, y_offset, 500, 100, option["text"], option["is_correct"])
                button.draw(self.screen, self.colours[i % len(self.colours)])
                option_buttons.append(button)
                y_offset += 130

            pygame.display.flip()

            # Wait for user input
            answered = False
            while not answered:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Return to the main quizzes screen
                            return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in option_buttons:
                            if button.is_clicked(mouse_pos):
                                if button.action:  # Check if correct answer
                                    correct_answers += 1
                                quiz_index += 1
                                answered = True

        # Display score
        self.display_score(correct_answers)

        # Display score
        self.display_score(correct_answers)

    def display_score(self, correct_answers):
        self.screen.fill((255, 255, 255))  # Clear screen
        score_text = f"Your score: {correct_answers}/10"
        score_surface = self.title_font.render(score_text, True, (0, 0, 0))
        self.screen.blit(
            score_surface,
            (self.screen.get_width() // 2 - score_surface.get_width() // 2, self.screen.get_height() // 2)
        )
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # Toggle sidebar
                        self.toggle_sidebar()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            self.run_quiz(button.action)  # Launch selected quiz
                            return  # Return to stop double event handling

                    # Handle sidebar option clicks
                    option_clicked = self.sidebar.handle_event(event)
                    if option_clicked:
                        if option_clicked == "Introduction":
                            option_clicked = "Preliminary"
                        self.manager.set_active_screen(option_clicked)
                        return  # Exit after handling sidebar click

            self.draw()
            pygame.display.flip()