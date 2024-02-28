import pygame
import time
import random

pygame.font.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

background = pygame.transform.scale(pygame.image.load("background.jpeg"), (width, height))

player_width = 30
player_height = 30
player_vel = 5

apple_width = 30
apple_height = 30


font = pygame.font.SysFont("comicsans", 30)


def draw(player, apple, tail, score):
    window.blit(background, (0, 0))

    score_text = font.render(f"Score: {score}", 1, "white")
    window.blit(score_text, (10,10))

    pygame.draw.rect(window, "green", player)
    pygame.draw.rect(window, "red", apple)
    for segment in tail:
        pygame.draw.rect(window, "green", segment)

    pygame.display.update()


def eaten(player, apple):
    return player.colliderect(apple)


def main():
    run = True

    player = pygame.Rect(370, 270, player_width, player_height)
    apple = pygame.Rect(370, 170, apple_width, apple_height)
    tail = []
    score = 0

    clock = pygame.time.Clock()

    move_direction = (0, 0)
    tail_extension = 3

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:  # Obsługa naciśnięcia klawisza
                if event.key == pygame.K_LEFT:
                    move_direction = (-player_vel, 0)  # Ustaw ruch w lewo
                elif event.key == pygame.K_RIGHT:
                    move_direction = (player_vel, 0)  # Ustaw ruch w prawo
                elif event.key == pygame.K_UP:
                    move_direction = (0, -player_vel)  # Ustaw ruch w górę
                elif event.key == pygame.K_DOWN:
                    move_direction = (0, player_vel)  # Ustaw ruch w dół

        if 0 <= player.x + move_direction[0] <= width - player_width:
            player.x += move_direction[0]
        if 0 <= player.y + move_direction[1] <= height - player_height:
            player.y += move_direction[1]

        tail.insert(0, player.copy())
        if len(tail) > 1:
            tail.pop()

        if eaten(player, apple):
            apple.x = random.randint(0, width - apple.width)
            apple.y = random.randint(0, height - apple_height)
            tail_extension += 10
            score += 1
            print(score)
        while tail_extension > 0:
            tail.append(pygame.Rect(tail[-1].x, tail[-1].y, player_width, player_height))
            tail_extension -= 1

        draw(player, apple, tail, score)

    pygame.quit()


if __name__ == "__main__":
    main()
