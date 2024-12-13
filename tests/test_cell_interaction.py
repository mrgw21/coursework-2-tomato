import unittest
import pygame
from objects.cell import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
        self.cell = Cell(0, center_pos=(400, 300))

    def tearDown(self):
        pygame.quit()

    def test_initial_state(self):
        self.assertTrue(self.cell.state)
        self.assertEqual(self.cell.health, "uninfected")
        self.assertFalse(self.cell.show_modal)

    def test_reposition(self):
        self.cell.reposition(center_pos=(400, 300))
        self.assertTrue(0 <= self.cell.rect.x <= 800)
        self.assertTrue(0 <= self.cell.rect.y <= 600)

    def test_die(self):
        self.cell.die()
        self.assertFalse(self.cell.state)
        self.assertEqual(self.cell.health, "infected")

    def test_handle_click_toggle_modal(self):
        level_mock = type('Level', (), {'paused': False})
        mouse_pos = (self.cell.rect.centerx, self.cell.rect.centery)
        self.cell.handle_click(mouse_pos, [self.cell], level_mock)
        self.assertTrue(self.cell.show_modal)
        self.assertTrue(level_mock.paused)
        self.cell.handle_click(mouse_pos, [self.cell], level_mock)
        self.assertFalse(self.cell.show_modal)
        self.assertFalse(level_mock.paused)

    def test_handle_modal_close(self):
        self.cell.show_modal = True
        level_mock = type('Level', (), {'paused': True})
        modal_width, modal_height = 300, 500
        modal_x, modal_y = 20, (self.screen.get_height() - modal_height) // 2
        close_button_width, close_button_height = 90, 25
        close_button_x = modal_x + modal_width - close_button_width - 10
        close_button_y = modal_y + 10
        mouse_pos = (close_button_x + close_button_width // 2, close_button_y + close_button_height // 2)
        self.cell.handle_modal_close(mouse_pos, level_mock)
        self.assertFalse(self.cell.show_modal)
        self.assertFalse(level_mock.paused)

    def test_keydown_esc_closes_modal(self):
        self.cell.show_modal = True
        level_mock = type('Level', (), {'paused': True})
        self.cell.handle_keydown(pygame.K_ESCAPE, level_mock)
        self.assertFalse(self.cell.show_modal)
        self.assertFalse(level_mock.paused)

    def test_get_info_text(self):
        info_text = self.cell.get_info_text()
        self.assertEqual(info_text, "Cells protect the body from pathogens.")

    def test_draw_modal(self):
        self.cell.show_modal = True
        self.cell.draw_modal(self.screen)

    def test_pause_on_modal_open(self):
        level_mock = type('Level', (), {'paused': False})
        mouse_pos = (self.cell.rect.centerx, self.cell.rect.centery)
        self.cell.handle_click(mouse_pos, [self.cell], level_mock)
        self.assertTrue(self.cell.show_modal)
        self.assertTrue(level_mock.paused)

    def test_resume_on_modal_close(self):
        self.cell.show_modal = True
        level_mock = type('Level', (), {'paused': True})
        self.cell.handle_keydown(pygame.K_ESCAPE, level_mock)
        self.assertFalse(self.cell.show_modal)
        self.assertFalse(level_mock.paused)

    def test_pause_resume_toggle(self):
        level_mock = type('Level', (), {'paused': False})
        mouse_pos = (self.cell.rect.centerx, self.cell.rect.centery)
        self.cell.handle_click(mouse_pos, [self.cell], level_mock)
        self.assertTrue(self.cell.show_modal)
        self.assertTrue(level_mock.paused)
        self.cell.handle_click(mouse_pos, [self.cell], level_mock)
        self.assertFalse(self.cell.show_modal)
        self.assertFalse(level_mock.paused)

if __name__ == "__main__":
    unittest.main()