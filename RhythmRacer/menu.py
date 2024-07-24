import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.options = ["Start Game", "Mode", "Difficulty", "High Scores", "Quit"]
        self.selected = 0
        self.modes = ["Continuous", "Timed"]
        self.selected_mode = 0
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.title_font.render("Rhythm Racer", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300 + i * 50))

        mode_text = self.font.render(f"{self.modes[self.selected_mode]}", True, (255, 255, 255))
        self.screen.blit(mode_text, (SCREEN_WIDTH//2 + 100, 350))

        difficulty_text = self.font.render(f"{self.difficulties[self.selected_difficulty]}", True, (255, 255, 255))
        self.screen.blit(difficulty_text, (SCREEN_WIDTH//2 + 100, 400))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_LEFT:
                if self.options[self.selected] == "Mode":
                    self.selected_mode = (self.selected_mode - 1) % len(self.modes)
                elif self.options[self.selected] == "Difficulty":
                    self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
            elif event.key == pygame.K_RIGHT:
                if self.options[self.selected] == "Mode":
                    self.selected_mode = (self.selected_mode + 1) % len(self.modes)
                elif self.options[self.selected] == "Difficulty":
                    self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected] in ["Start Game", "High Scores", "Quit"]:
                    return self.options[self.selected]
        return None

    def show_high_scores(self, high_scores):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            title = self.title_font.render("High Scores", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            for i, (mode, scores) in enumerate(high_scores.items()):
                mode_text = self.font.render(f"{mode.capitalize()}:", True, (255, 255, 255))
                self.screen.blit(mode_text, (SCREEN_WIDTH // 4, 200 + i * 200))

                for j, score in enumerate(scores[:5]):  # Display top 5 scores
                    score_text = self.font.render(f"{score['name']}: {score['score']}", True, (255, 255, 255))
                    self.screen.blit(score_text, (SCREEN_WIDTH // 4, 240 + i * 200 + j * 40))

            instruction_text = self.font.render("Press SPACE to return to menu", True, (255, 255, 255))
            self.screen.blit(instruction_text,
                             (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT - 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True
