import pygame
from data.leaderboard_manager import LeaderboardManager
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen

class LeaderboardLevel2(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_title_2 = pygame.font.SysFont("Arial", 30)
        self.font_text = pygame.font.SysFont("Arial", 24)
        self.sidebar = Sidebar()
        self.leaderboard = LeaderboardManager(filepath="data/leaderboards/level2_leaderboard.json")
        self.running = True  # Track if the screen is active

        # Buttons for switching leaderboards
        self.buttons = ["Level 1", "Level 2"]
        self.selected_button = "Level 2"  # Default selection
        self.button_font = pygame.font.SysFont("Arial", 24)

    def draw_buttons(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        button_width = 200
        button_height = 40
        x = sidebar_width + 125
        y_offset = 200
        spacing = 10

        for i, button in enumerate(self.buttons):
            y = y_offset + i * (button_height + spacing)

            # Determine button style based on selection
            if button == self.selected_button:
                color = (0, 0, 139)  # Blue for selected
                font = pygame.font.SysFont("Arial", 24, bold=True)  # Bold font
            else:
                color = (255, 140, 0)  # Orange for unselected
                font = self.button_font  # Regular font

            # Draw button text
            text = font.render(button, True, color)
            text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
            pygame.draw.rect(self.screen, (240, 240, 240), (x, y, button_width, button_height))  # Button background
            self.screen.blit(text, text_rect)

    def handle_button_click(self, mouse_pos):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        button_width = 200
        button_height = 40
        x = sidebar_width + 125
        y_offset = 200
        spacing = 10

        for i, button in enumerate(self.buttons):
            y = y_offset + i * (button_height + spacing)
            button_rect = pygame.Rect(x, y, button_width, button_height)

            if button_rect.collidepoint(mouse_pos):
                return button
        return None

    def draw(self):
        self.screen.fill((255, 255, 255))  # Fill background

        # Draw buttons
        self.draw_buttons()

        # Sidebar
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Leaderboards")

        # Draw Title
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        game_width = self.screen.get_width() - sidebar_width
        center_x = sidebar_width + game_width // 2

        # Main Title
        title_text = self.font_title.render("Leaderboard", True, (0, 0, 139))  # Dark Blue
        title_rect = title_text.get_rect(center=(center_x, 50))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        title_2_text = self.font_title_2.render("Level 2", True, (0, 0, 139))  # Dark Blue
        title_2_rect = title_2_text.get_rect(center=(center_x, 100))
        self.screen.blit(title_2_text, title_2_rect)

        # Draw Orange Line below Title
        line_start = (sidebar_width + 20, 140)
        line_end = (self.screen.get_width() - 20, 140)
        pygame.draw.line(self.screen, (255, 140, 0), line_start, line_end, 5)

        # Get leaderboard data, or use defaults if no data exists
        leaderboard = self.leaderboard.get_leaderboard("Level2") or []

        # Calculate how many default entries are needed
        missing_entries = 10 - len(leaderboard)

        # Fill missing entries with default values
        if missing_entries > 0:
            leaderboard.extend(
                [{"score": 0, "timestamp": "00:00 01-01-2000"} for _ in range(missing_entries)]
        )

        # Limit leaderboard to the top 10 entries
        leaderboard = leaderboard[:10]

        # Centerize leaderboard table
        table_width = 500  # Approximate width of the leaderboard table
        table_x = sidebar_width + (game_width - table_width) // 2
        start_y = 200
        row_height = 40

        col_widths = {
            "rank": 100,
            "score": 300,
            "timestamp": 300,
        }

        col_positions = {
            "rank": table_x,
            "score": table_x + col_widths["rank"],
            "timestamp": table_x + col_widths["rank"] + col_widths["score"],
        }

        # Draw Column Headers
        headers = {"rank": "Rank", "score": "Score", "timestamp": "Achieved at"}
        header_font = pygame.font.SysFont("Arial", 24, bold=True)

        for col, text in headers.items():
            header_text = header_font.render(text, True, (0, 0, 0))  # Black for headers
            header_x = col_positions[col] + (col_widths[col] - header_text.get_width()) // 2
            header_y = start_y - 40
            self.screen.blit(header_text, (header_x, header_y))

        # Draw Leaderboard Entries
        for i, entry in enumerate(leaderboard):
            rank = f"{i + 1}"  # Rank starts at 1
            score = f"{entry['score']}"  # Score
            achieved_at = entry["timestamp"]  # Timestamp

            rank_text = self.font_text.render(rank, True, (0, 0, 0))
            score_text = self.font_text.render(score, True, (0, 0, 0))
            achieved_at_text = self.font_text.render(achieved_at, True, (0, 0, 0))

            rank_x = col_positions["rank"] + (col_widths["rank"] - rank_text.get_width()) // 2
            score_x = col_positions["score"] + (col_widths["score"] - score_text.get_width()) // 2
            achieved_at_x = col_positions["timestamp"] + (col_widths["timestamp"] - achieved_at_text.get_width()) // 2
            y_position = start_y + i * row_height

            self.screen.blit(rank_text, (rank_x, y_position))
            self.screen.blit(score_text, (score_x, y_position))
            self.screen.blit(achieved_at_text, (achieved_at_x, y_position))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.manager.set_active_screen("Home")
            elif event.key == pygame.K_m:
                self.sidebar.toggle()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_button = self.handle_button_click(mouse_pos)
            if clicked_button:
                self.switch_leaderboard(clicked_button)

            clicked_option = self.sidebar.handle_event(event)
            if clicked_option:
                self.running = False
                self.manager.set_active_screen(clicked_option)
        elif event.type == pygame.VIDEORESIZE:
            self.reposition_elements()  # Adjust positions for new window size

    def switch_leaderboard(self, button):
        self.selected_button = button  # Highlight the clicked button
        if button == "Level 1":
            self.running = False
            self.manager.set_active_screen("Leaderboards")
        elif button == "Level 2":
            return  # Already on this screen

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()