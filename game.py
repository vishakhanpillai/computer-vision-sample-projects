import cv2
import mediapipe as mp
import pygame
import sys
import random

# Init Pygame
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Body Dodge")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# Player
player_width = 50
player_height = 20
player_y = HEIGHT - player_height - 10
player_x = WIDTH // 2

# Falling block
block_width = 30
block_height = 30
block_x = random.randint(0, WIDTH - block_width)
block_y = -block_height
block_speed = 20

# Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

def get_player_position():
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)
    if results.pose_landmarks:
        # Get left and right shoulder landmarks
        l_sh = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_sh = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        center_x = int(((l_sh.x + r_sh.x) / 2) * WIDTH)
        return center_x
    return None

def check_collision(px, bx, by):
    if by + block_height > player_y:
        if bx < px + player_width and bx + block_width > px:
            return True
    return False

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get player X from body
    pos = get_player_position()
    if pos:
        player_x = pos - player_width // 2  # Center the box

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Move and draw block
    block_y += block_speed
    if block_y > HEIGHT:
        block_y = -block_height
        block_x = random.randint(0, WIDTH - block_width)

    pygame.draw.rect(screen, RED, (block_x, block_y, block_width, block_height))

    # Check collision
    if check_collision(player_x, block_x, block_y):
        font = pygame.font.SysFont(None, 60)
        text = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 30))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    pygame.display.update()
    clock.tick(30)

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
