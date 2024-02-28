import pygame
import random

pygame.font.init()


# Sets width and height of game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Create background and scale it to the window size
background = pygame.transform.scale(pygame.image.load("background.jpeg"), (width, height))

# Player size
player_width = 30
player_height = 30
player_vel = 5

# Apple size
apple_width = 30
apple_height = 30

# Font type and size
font = pygame.font.SysFont("comicsans", 30)


# Draws objects on display
def draw(player, apple, tail, score):
    window.blit(background, (0, 0))

    # Draw score
    score_text = font.render(f"Score: {score}", 1, "white")
    window.blit(score_text, (10, 10))

    # Draw player, apple and tail
    pygame.draw.rect(window, "green", player)
    pygame.draw.rect(window, "red", apple)
    for segment in tail:
        pygame.draw.rect(window, "green", segment)

    pygame.display.update()

# Function that checks if player is in collision with apple
def eaten(player, apple):
    return player.colliderect(apple)

# Function that checks if playes is in collision with tail
def tail_collision(player, tail):
    for segment in tail[11:]:
        if player.colliderect(segment):
            return True

# Function that display end game window
def game_over(score):
    window.blit(background, (0, 0))
    game_over_text = font.render("Game Over", 1, "red")
    score_text = font.render(f"You've got: {score} points", 1, "white")

    window.blit(game_over_text, (width / 2 - game_over_text.get_width() / 2, height / 2 - 40))
    window.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 2))

    pygame.display.update()
    pygame.time.delay(3000)


def main():
    run = True

    # Initialize player and apple
    player = pygame.Rect(370, 270, player_width, player_height)
    apple = pygame.Rect(370, 170, apple_width, apple_height)
    tail = []
    tail_extension = 0
    score = 0

    #Initialize clock (It's used to set "speed" of while loop if not, player would be super fast)
    clock = pygame.time.Clock()

    move_direction = (0, 0)

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:  # Handle key press
                if event.key == pygame.K_LEFT:
                    move_direction = (-player_vel, 0)  # Set movement to the left
                elif event.key == pygame.K_RIGHT:
                    move_direction = (player_vel, 0)  # Set movement to the right
                elif event.key == pygame.K_UP:
                    move_direction = (0, -player_vel)  # Set movement upward
                elif event.key == pygame.K_DOWN:
                    move_direction = (0, player_vel)  # Set movement downward

        # Update player position
        if 0 <= player.x + move_direction[0] <= width - player_width:
            player.x += move_direction[0]
        if 0 <= player.y + move_direction[1] <= height - player_height:
            player.y += move_direction[1]

        # Update tail
        tail.insert(0, player.copy())
        if len(tail) > 1:
            tail.pop()

        # Check if player has eaten the apple
        if eaten(player, apple):
            apple.x = random.randint(0, width - apple.width)
            apple.y = random.randint(0, height - apple_height)
            tail_extension += 10
            score += 1

        # Extend tail
        while tail_extension > 0 and len(tail) > 0:
            tail.append(pygame.Rect(tail[-1].x, tail[-1].y, player_width, player_height))
            tail_extension -= 1

        # Check tail collision
        if tail_collision(player, tail):
            game_over(score)
            run = False

        # Check collision with window borders
        if player.x < 0 or player.x + player_width > width or player.y < 0 or player.y + player_height > height:
            game_over(score)
            run = False

        # Draw objects on the screen
        draw(player, apple, tail, score)

    pygame.quit()


if __name__ == "__main__":
    main()
