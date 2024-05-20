import pygame
import time
import random

# Initialize Pygame font
pygame.font.init()

# Set window dimensions
WIDTH, HEIGHT = 1000, 800
# Create Pygame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Set window title
pygame.display.set_caption("Space Dodge")

# Load background image and scale it to window dimensions
BG = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))

# Player dimensions
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
# Player velocity
PLAYER_VEL = 5

# Star dimensions
STAR_WIDTH = 10
STAR_HEIGHT = 20
# Star velocity
STAR_VEL = 3

# Font for displaying time
FONT = pygame.font.SysFont("comicsans", 30)

# Function to draw objects on the screen
def draw(player, elapsed_time, stars):
    # Draw background
    WIN.blit(BG, (0, 0))

    # Render and draw elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw player
    pygame.draw.rect(WIN, "red", player)

    # Draw stars
    for star in stars:
        pygame.draw.rect(WIN, "purple", star)

    # Update display
    pygame.display.update()

# Main function
def main():
    run = True

    # Create player rectangle
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # Variables for star generation
    star_add_increment = 2000
    star_count = 0

    # List to store stars
    stars = []
    hit = False

    while run:
        # Track time passed
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add stars at intervals
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            # Increase difficulty by reducing interval
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Move player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        # Move stars and check for collisions
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # End game if player is hit by a star
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Draw game elements
        draw(player, elapsed_time, stars)

    # Quit Pygame
    pygame.quit()

# Execute main function if script is run directly
if __name__ == "__main__":
    main()