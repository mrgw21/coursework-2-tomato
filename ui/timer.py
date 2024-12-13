import pygame

class Timer:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, remaining_time, paused, game_over=False):
        # Draw Timer
        timer_text = self.font.render(f"{remaining_time // 60:02}:{remaining_time % 60:02}", True, (0, 0, 0))
        timer_rect = timer_text.get_rect(topright=(screen.get_width() - 70, 30))
        screen.blit(timer_text, timer_rect)

        # Draw "Paused" text if the game is paused and not over
        if paused and not game_over:
            paused_font = pygame.font.SysFont('Arial', 24)
            paused_text = paused_font.render("Paused", True, (0, 0, 139))
            paused_rect = paused_text.get_rect(right=timer_rect.left - 10, centery=timer_rect.centery)
            screen.blit(paused_text, paused_rect)