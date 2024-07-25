import pygame
from high_scores import HighScores
from game import Game
from menu import Menu
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display=1)
    pygame.display.set_caption("Rhythm Racer")

    menu = Menu(screen)
    high_scores = HighScores()
    game = None
    clock = pygame.time.Clock()

    running = True
    in_menu = True

    while running:
        if in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                action = menu.handle_event(event)
                if action == "Start Game":
                    if game:
                        game.cleanup()
                    game = Game(menu.modes[menu.selected_mode].lower(), menu.difficulties[menu.selected_difficulty].lower())
                    in_menu = False
                elif action == "High Scores":
                    if not menu.show_high_scores(high_scores.scores):
                        running = False
                elif action == "Quit":
                    running = False

            menu.draw()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                action = game.handle_event(event)
                if action == "MENU":
                    in_menu = True

            game.update()
            game.render()

            if game.is_game_over():
                game.cleanup()
                screen.blit(game.game_over_screen, (0, 0))
                pygame.display.flip()
                pygame.time.wait(3500)  # Wait before returning to menu
                in_menu = True

        pygame.display.flip()
        clock.tick(60)

    if game:
        game.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()