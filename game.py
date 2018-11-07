import pygame

def game_loop():
    pygame.init()

    window_w = 800
    window_h = 600

    white = (255, 255, 255)
    black = (0, 0, 0)

    FPS = 120

    window = pygame.display.set_mode((window_w, window_h))
    pygame.display.set_caption("Game: ")
    clock = pygame.time.Clock()

    ball_radius = 10

    velocity = [1, 1]

    pos_x = window_w/2
    pos_y = window_h/2

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pos_x += velocity[0]
        pos_y += velocity[1]

        if pos_x > window_w or pos_x < 0:
            velocity[0] = -velocity[0]

        if pos_y > window_h or pos_y < 0:
            velocity[1] = -velocity[1]

        # DRAW
        window.fill(white)
        pygame.draw.circle(window, black, (int(pos_x), int(pos_y)), ball_radius)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    game_loop()
