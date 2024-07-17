import pygame
from game import Game


def main():
    pygame.init()

    # For now, manually set the mode here
    mode = 'timed'  # or 'timed'

    game = Game(mode)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.handle_event(event)

        game.update()
        game.render()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
