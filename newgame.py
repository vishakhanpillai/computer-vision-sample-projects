import pygame
import random
import cv2
import mediapipe as mp
import sys

# === Init Pygame ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍉 Fruit Ninja - Hand Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# === Mediapipe Hand Detection ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

# === Game Data ===
score = 0
fruits = []
FRUIT_RADIUS = 30
FRUIT_COLORS = [(255, 0, 0), (0, 255, 0), (255, 165, 0), (138, 43, 226)]

# === Fruit Spawner ===
def spawn_fruit():
    x = random.randint(FRUIT_RADIUS, WIDTH - FRUIT_RADIUS)
    y = HEIGHT + FRUIT_RADIUS
    speed_y = random.uniform(-18, -12)
    color = random.choice(FRUIT_COLORS)
    return {'x': x, 'y': y, 'vy': speed_y, 'color': color, 'sliced': False}

# === Detect Hand Position ===
def get_hand_position():
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        wrist = result.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        hand_x = int(wrist.x * WIDTH)
        hand_y = int(wrist.y * HEIGHT)
        return (hand_x, hand_y)
    return None

# === Game Loop ===
running = True
spawn_timer = 0

while running:
    screen.fill((0, 0, 0))
    spawn_timer += 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn fruit every 30 frames
    if spawn_timer > 30:
        fruits.append(spawn_fruit())
        spawn_timer = 0

    # Get hand position
    hand_pos = get_hand_position()
    if hand_pos:
        pygame.draw.circle(screen, (255, 255, 255), hand_pos, 15)  # Draw hand marker

    # Update and draw fruits
    for fruit in fruits[:]:
        fruit['y'] += fruit['vy']
        fruit['vy'] += 0.5  # Gravity

        # Draw fruit
        if not fruit['sliced']:
            pygame.draw.circle(screen, fruit['color'], (int(fruit['x']), int(fruit['y'])), FRUIT_RADIUS)

        # Check if sliced
        if hand_pos and not fruit['sliced']:
            dx = hand_pos[0] - fruit['x']
            dy = hand_pos[1] - fruit['y']
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < FRUIT_RADIUS + 15:
                fruit['sliced'] = True
                score += 1

        # Remove off-screen fruits
        if fruit['y'] > HEIGHT + FRUIT_RADIUS or fruit['sliced']:
            fruits.remove(fruit)

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Refresh
    pygame.display.update()
    clock.tick(30)

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
