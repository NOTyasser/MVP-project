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

# Load player (flyfighter) image and get its rectangle
PLAYER_IMG = pygame.image.load("flyfighter.png")  # Ensure this image has a transparent background
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (40, 60))  # Adjust the size if needed
PLAYER_RECT = PLAYER_IMG.get_rect()

# Player velocity
PLAYER_VEL = 5

# Star dimensions
STAR_WIDTH = 10
STAR_HEIGHT = 20
# Star velocity
STAR_VEL = 3

# Falling star parameters
NUM_FALLING_STARS = 100
FALLING_STAR_MIN_SIZE = 1
FALLING_STAR_MAX_SIZE = 3
FALLING_STAR_MIN_SPEED = 1
FALLING_STAR_MAX_SPEED = 3

# Asteroid parameters
ASTEROID_WIDTH = 60
ASTEROID_HEIGHT = 80
ASTEROID_VEL = 2
NUM_ASTEROIDS = 5

# Red ball parameters
RED_BALL_SIZE = 10
RED_BALL_VEL = 5

# Font for displaying time
FONT = pygame.font.SysFont("comicsans", 30)

# Star class for falling stars
class FallingStar:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(FALLING_STAR_MIN_SIZE, FALLING_STAR_MAX_SIZE)
        self.speed = random.randint(FALLING_STAR_MIN_SPEED, FALLING_STAR_MAX_SPEED)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.circle(WIN, (255, 255, 255), (self.x, self.y), self.size)

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = ASTEROID_VEL
        self.last_drop_time = time.time()

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)

    def draw(self):
        points = [(self.x, self.y), (self.x + ASTEROID_WIDTH // 2, self.y + ASTEROID_HEIGHT), (self.x - ASTEROID_WIDTH // 2, self.y + ASTEROID_HEIGHT)]
        pygame.draw.polygon(WIN, (0, 0, 0), points)

    def drop_red_ball(self):
        current_time = time.time()
        if current_time - self.last_drop_time > 2:  # Drops a red ball every 2 seconds
            self.last_drop_time = current_time
            return RedBall(self.x, self.y + ASTEROID_HEIGHT)
        return None

    def get_rect(self):
        # Return the bounding box of the asteroid for collision detection
        return pygame.Rect(self.x - ASTEROID_WIDTH // 2, self.y, ASTEROID_WIDTH, ASTEROID_HEIGHT)

# Red ball class
class RedBall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = RED_BALL_SIZE
        self.speed = RED_BALL_VEL

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            return True  # Indicates the ball is out of the screen and should be removed
        return False

    def draw(self):
        pygame.draw.circle(WIN, (255, 0, 0), (self.x, self.y), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

# Function to draw objects on the screen
def draw(player_rect, elapsed_time, stars, falling_stars, asteroids, red_balls):
    # Draw background
    WIN.blit(BG, (0, 0))

    # Render and draw elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw player
    WIN.blit(PLAYER_IMG, (player_rect.x, player_rect.y))

    # Draw stars
    for star in stars:
        pygame.draw.rect(WIN, "black", star)

    # Draw falling stars
    for falling_star in falling_stars:
        falling_star.draw()

    # Draw asteroids
    for asteroid in asteroids:
        asteroid.draw()

    # Draw red balls
    for red_ball in red_balls:
        red_ball.draw()

    # Update display
    pygame.display.update()

# Main function
def main():
    run = True

    # Create player rectangle
    player_rect = PLAYER_RECT
    player_rect.x = 200
    player_rect.y = HEIGHT - PLAYER_RECT.height
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # Variables for star generation
    star_add_increment = 2000
    star_count = 0

    # List to store stars, falling stars, asteroids, and red balls
    stars = []
    falling_stars = [FallingStar() for _ in range(NUM_FALLING_STARS)]
    asteroids = [Asteroid() for _ in range(NUM_ASTEROIDS)]
    red_balls = []
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
        if keys[pygame.K_LEFT] and player_rect.x - PLAYER_VEL >= 0:
            player_rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_rect.x + PLAYER_VEL + player_rect.width <= WIDTH:
            player_rect.x += PLAYER_VEL

        # Move stars and check for collisions
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player_rect.y and star.colliderect(player_rect):
                stars.remove(star)
                hit = True
                break

        # Move falling stars
        for falling_star in falling_stars:
            falling_star.move()

        # Move asteroids and drop red balls
        for asteroid in asteroids:
            asteroid.move()
            if asteroid.get_rect().colliderect(player_rect):
                hit = True
                break
            red_ball = asteroid.drop_red_ball()
            if red_ball:
                red_balls.append(red_ball)
        

        # Move red balls and check for collisions
        for red_ball in red_balls[:]:
            if red_ball.move():
                red_balls.remove(red_ball)
            elif red_ball.get_rect().colliderect(player_rect):
                hit = True
                break

        # End game if player is hit by a star, an asteroid, or a red ball
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Draw game elements
        draw(player_rect, elapsed_time, stars, falling_stars, asteroids, red_balls)

    # Quit Pygame
    pygame.quit()

# Execute main function if script is run directly
if __name__ == "__main__":
    main()
