import pygame
import random
import math
import array
import os

# --- INITIALIZATION ---
pygame.init()
pygame.mixer.init()

# --- CONFIGURATION ---
WIDTH, HEIGHT = 500, 750
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -14
BASE_SCROLL_SPEED = 2

# Camera threshold (where the screen starts pushing down)
CAMERA_LINE = HEIGHT // 3

# Aesthetic Colors
BG_TOP = (26, 28, 41)
BG_BOTTOM = (42, 45, 67)
WHITE = (255, 255, 255)
PINK = (255, 121, 198)
CYAN = (139, 233, 253)
GREEN = (80, 250, 123)
YELLOW = (241, 250, 140)
RED = (255, 85, 85)
DARK_PANEL = (40, 42, 54)
UI_BG = (60, 64, 80)


# --- SYNTHESIZED SOUND GENERATOR ---
def generate_sound(frequency, duration, volume=0.5, wave_type='sine'):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == 'sine':
            val = math.sin(2.0 * math.pi * frequency * t)
        elif wave_type == 'square':
            val = 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
        elif wave_type == 'noise':
            val = random.uniform(-1, 1)

        envelope = 1.0 - (i / n_samples)
        buf.append(int(val * envelope * volume * 32767))
    return pygame.mixer.Sound(buffer=buf)


SND_JUMP = generate_sound(400, 0.1, 0.3, 'square')
SND_COIN = generate_sound(880, 0.1, 0.3, 'sine')
SND_HIT = generate_sound(150, 0.3, 0.5, 'noise')

# --- MUSIC LOADING (Fixed for Pygbag) ---
# Priority 1: Look for OGG (Required for Web/Pygbag)
if os.path.exists("bg_music.ogg"):
    pygame.mixer.music.load("bg_music.ogg")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
# Priority 2: Look for MP3 (Fallback for local testing)
elif os.path.exists("bg_music.mp3"):
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# --- SETUP DISPLAY ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Ascent: Tower of Trials")
clock = pygame.time.Clock()
font_large = pygame.font.SysFont("impact", 50)
font_medium = pygame.font.SysFont("arial", 25, bold=True)
font_small = pygame.font.SysFont("arial", 16)


# --- SPRITE GENERATION ---
def create_character_surface(char_type):
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 230, 213), (8, 10, 16, 12))

    if char_type == 0:  # Demon Girl
        pygame.draw.rect(surf, (255, 85, 85), (4, 4, 24, 10))
        pygame.draw.rect(surf, (255, 85, 85), (4, 10, 6, 16))
        pygame.draw.rect(surf, (255, 85, 85), (22, 10, 6, 16))
        pygame.draw.polygon(surf, (30, 30, 30), [(6, 4), (2, -4), (10, 4)])
        pygame.draw.polygon(surf, (30, 30, 30), [(26, 4), (30, -4), (22, 4)])
        pygame.draw.rect(surf, (30, 30, 30), (10, 22, 12, 10))
        pygame.draw.rect(surf, (80, 250, 123), (10, 14, 4, 4))
        pygame.draw.rect(surf, (80, 250, 123), (18, 14, 4, 4))
    elif char_type == 1:  # Cyan Pop Star
        pygame.draw.rect(surf, (139, 233, 253), (4, 4, 24, 10))
        pygame.draw.rect(surf, (139, 233, 253), (0, 10, 8, 20))
        pygame.draw.rect(surf, (139, 233, 253), (24, 10, 8, 20))
        pygame.draw.rect(surf, (68, 71, 90), (8, 22, 16, 10))
        pygame.draw.rect(surf, (255, 121, 198), (10, 14, 4, 4))
        pygame.draw.rect(surf, (255, 121, 198), (18, 14, 4, 4))
    elif char_type == 2:  # Straw Hat
        pygame.draw.rect(surf, (68, 71, 90), (4, 8, 24, 10))
        pygame.draw.rect(surf, (255, 204, 0), (2, 4, 28, 6))
        pygame.draw.rect(surf, (255, 204, 0), (8, 0, 16, 6))
        pygame.draw.rect(surf, (255, 85, 85), (8, 22, 16, 10))
        pygame.draw.rect(surf, (241, 250, 140), (10, 14, 4, 4))
        pygame.draw.rect(surf, (241, 250, 140), (18, 14, 4, 4))

    return pygame.transform.scale(surf, (44, 44))


# --- UI DRAWING ---
def draw_direct_icons(surface, is_paused, is_muted):
    icon_y = 30
    icon_x_start = WIDTH - 170
    spacing = 45

    # 1. Restart Icon
    pygame.draw.circle(surface, UI_BG, (icon_x_start, icon_y), 18)
    pygame.draw.arc(surface, PINK, (icon_x_start - 8, icon_y - 8, 16, 16), 0.5, 5.5, 3)
    pygame.draw.polygon(surface, PINK, [(icon_x_start + 2, icon_y - 10), (icon_x_start + 8, icon_y - 6),
                                        (icon_x_start + 4, icon_y - 2)])

    # 2. Pause/Resume Icon
    px = icon_x_start + spacing
    pygame.draw.circle(surface, UI_BG, (px, icon_y), 18)
    if is_paused:
        pygame.draw.polygon(surface, YELLOW, [(px - 5, icon_y - 8), (px + 8, icon_y), (px - 5, icon_y + 8)])
    else:
        pygame.draw.rect(surface, YELLOW, (px - 6, icon_y - 8, 4, 16))
        pygame.draw.rect(surface, YELLOW, (px + 2, icon_y - 8, 4, 16))

    # 3. Mute Icon
    mx = icon_x_start + spacing * 2
    pygame.draw.circle(surface, UI_BG, (mx, icon_y), 18)
    pygame.draw.rect(surface, CYAN, (mx - 8, icon_y - 4, 4, 8))
    pygame.draw.polygon(surface, CYAN,
                        [(mx - 4, icon_y - 4), (mx + 2, icon_y - 8), (mx + 2, icon_y + 8), (mx - 4, icon_y + 4)])
    if is_muted:
        pygame.draw.line(surface, RED, (mx + 4, icon_y - 4), (mx + 10, icon_y + 4), 2)
        pygame.draw.line(surface, RED, (mx + 10, icon_y - 4), (mx + 4, icon_y + 4), 2)
    else:
        pygame.draw.arc(surface, CYAN, (mx, icon_y - 6, 10, 12), -1, 1, 2)

    # 4. Quit Icon
    qx = icon_x_start + spacing * 3
    pygame.draw.circle(surface, UI_BG, (qx, icon_y), 18)
    pygame.draw.rect(surface, RED, (qx - 6, icon_y - 6, 10, 12), 2)
    pygame.draw.line(surface, RED, (qx - 2, icon_y), (qx + 8, icon_y), 2)
    pygame.draw.polygon(surface, RED, [(qx + 4, icon_y - 4), (qx + 8, icon_y), (qx + 4, icon_y + 4)])


# --- GAME CLASSES ---
class Player:
    def __init__(self, char_type):
        self.image = create_character_surface(char_type)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.vx = 0
        self.vy = JUMP_STRENGTH

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.vx -= 1.5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx += 1.5

        self.vx *= 0.85
        self.vy += GRAVITY

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0


class Platform:
    def __init__(self, x, y, width=80, is_danger=False):
        self.rect = pygame.Rect(x, y, width, 15)
        self.is_danger = is_danger
        self.color = RED if is_danger else random.choice([PINK, CYAN, GREEN, YELLOW])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=5)
        if self.is_danger:
            for i in range(self.rect.width // 20):
                pygame.draw.polygon(surface, (200, 200, 200), [
                    (self.rect.x + i * 20, self.rect.y),
                    (self.rect.x + i * 20 + 10, self.rect.y - 10),
                    (self.rect.x + i * 20 + 20, self.rect.y)
                ])


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)

    def draw(self, surface):
        pygame.draw.ellipse(surface, YELLOW, self.rect)
        pygame.draw.ellipse(surface, (200, 180, 0), self.rect, 2)


# --- MAIN GAME LOOP ---
def main():
    state = "MENU"
    selected_char = 0
    char_images = [create_character_surface(0), create_character_surface(1), create_character_surface(2)]

    player = None
    platforms = []
    coins = []
    particles = []

    score = 0
    highest_score = 0
    current_speed = BASE_SCROLL_SPEED
    game_started_scrolling = False
    is_muted = False

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state in ["PLAYING", "PAUSED"] and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    icon_y = 30
                    icon_x_start = WIDTH - 170
                    spacing = 45

                    if icon_y - 18 < my < icon_y + 18:
                        # Restart
                        if icon_x_start - 18 < mx < icon_x_start + 18:
                            state = "MENU"
                        # Pause/Resume
                        elif (icon_x_start + spacing) - 18 < mx < (icon_x_start + spacing) + 18:
                            state = "PAUSED" if state == "PLAYING" else "PLAYING"
                        # Mute
                        elif (icon_x_start + spacing * 2) - 18 < mx < (icon_x_start + spacing * 2) + 18:
                            is_muted = not is_muted
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.set_volume(0 if is_muted else 0.3)
                        # Quit
                        elif (icon_x_start + spacing * 3) - 18 < mx < (icon_x_start + spacing * 3) + 18:
                            running = False

            if state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if my > 300 and my < 450:
                        if 50 < mx < 150:
                            selected_char = 0
                        elif 200 < mx < 300:
                            selected_char = 1
                        elif 350 < mx < 450:
                            selected_char = 2

                        state = "PLAYING"
                        game_started_scrolling = False
                        player = Player(selected_char)

                        platforms = [Platform(WIDTH // 2 - 40, HEIGHT - 60, 80)]
                        last_x = WIDTH // 2 - 40
                        for i in range(1, 12):
                            width = random.randint(50, 100)
                            if i % 2 == 0:
                                new_x = random.randint(10, WIDTH // 2)
                            else:
                                new_x = random.randint(WIDTH // 2, WIDTH - width - 10)
                            platforms.append(Platform(new_x, HEIGHT - 60 - (i * 110), width))
                            last_x = new_x

                        coins = []
                        particles = []
                        score = 0
                        current_speed = BASE_SCROLL_SPEED

            if state == "GAMEOVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if my > 500 and my < 550: state = "MENU"
                    if my > 580 and my < 630: running = False

        # --- DRAWING BACKGROUND ---
        screen.fill(BG_TOP)
        for y in range(HEIGHT):
            color = (
                BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT,
                BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT,
                BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        if random.random() < 0.1:
            particles.append(
                [random.randint(0, WIDTH), HEIGHT, random.uniform(0.5, 2), random.choice([PINK, CYAN, WHITE])])

        for p in particles[:]:
            p[1] -= p[2]
            if p[1] < 0:
                particles.remove(p)
            else:
                pygame.draw.circle(screen, p[3], (int(p[0]), int(p[1])), 2)

        # --- GAME STATES ---
        if state == "MENU":
            title = font_large.render("PIXEL ASCENT", True, PINK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            subtitle = font_medium.render("Choose Your Fighter", True, WHITE)
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 180))

            for i, img in enumerate(char_images):
                x = 50 + i * 150
                pygame.draw.rect(screen, DARK_PANEL, (x, 300, 100, 150), border_radius=10)
                if i == selected_char:
                    pygame.draw.rect(screen, PINK, (x, 300, 100, 150), width=4, border_radius=10)
                screen.blit(img, (x + 28, 320))

                names = ["Demon", "Popstar", "Hat"]
                name_surf = font_medium.render(names[i], True, WHITE)
                screen.blit(name_surf, (x + 50 - name_surf.get_width() // 2, 380))

            start_text = font_medium.render("Click a character to start!", True, CYAN)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 500))

        elif state in ["PLAYING", "PAUSED"]:
            current_speed = BASE_SCROLL_SPEED + (score // 150) * 0.5

            if state == "PLAYING":
                player.update()

                aura_rect = player.rect.inflate(10, 10)
                pygame.draw.rect(screen, (255, 255, 255, 50), aura_rect, border_radius=10)

                for p in platforms:
                    if player.vy > 0 and player.rect.colliderect(p.rect):
                        if p.is_danger:
                            SND_HIT.play()
                            state = "GAMEOVER"
                            if score > highest_score: highest_score = score
                            break
                        else:
                            player.rect.bottom = p.rect.top
                            player.vy = JUMP_STRENGTH
                            SND_JUMP.play()
                            score += 10
                            for _ in range(5):
                                particles.append([player.rect.centerx, player.rect.bottom, random.uniform(1, 3), WHITE])

                for c in coins[:]:
                    if player.rect.colliderect(c.rect):
                        coins.remove(c)
                        SND_COIN.play()
                        score += 50
                        for _ in range(8):
                            particles.append([c.rect.centerx, c.rect.centery, random.uniform(1, 4), YELLOW])

                if player.rect.y < CAMERA_LINE:
                    game_started_scrolling = True

                if game_started_scrolling:
                    if player.rect.y < CAMERA_LINE:
                        scroll_amount = CAMERA_LINE - player.rect.y
                        player.rect.y = CAMERA_LINE
                        for p in platforms: p.rect.y += scroll_amount
                        for c in coins: c.rect.y += scroll_amount

                    for p in platforms:
                        p.rect.y += current_speed
                        p.draw(screen)
                else:
                    for p in platforms:
                        p.draw(screen)

                for p in platforms[:]:
                    if p.rect.y > HEIGHT:
                        platforms.remove(p)
                        highest_y = min([plat.rect.y for plat in platforms]) if platforms else HEIGHT

                        is_danger = False
                        if score > 200 and random.random() < 0.35:
                            is_danger = True

                        if platforms:
                            top_plat = min(platforms, key=lambda x: x.rect.y)
                            if top_plat.rect.x < WIDTH // 2:
                                new_x = random.randint(WIDTH - 100, WIDTH - 50)
                            else:
                                new_x = random.randint(10, 80)
                        else:
                            new_x = random.randint(0, WIDTH - 80)

                        width = random.randint(50, 100)
                        platforms.append(Platform(new_x, highest_y - random.randint(90, 120), width, is_danger))

                if random.random() < 0.02 and score > 50:
                    coins.append(Coin(random.randint(20, WIDTH - 20), -20))

                for c in coins[:]:
                    if game_started_scrolling: c.rect.y += current_speed
                    c.draw(screen)
                    if c.rect.y > HEIGHT: coins.remove(c)

                screen.blit(player.image, player.rect)

                if player.rect.y > HEIGHT:
                    SND_HIT.play()
                    state = "GAMEOVER"
                    if score > highest_score: highest_score = score

            score_text = font_large.render(f"{score}", True, WHITE)
            screen.blit(score_text, (20, 20))

            draw_direct_icons(screen, state == "PAUSED", is_muted)

            if state == "PAUSED":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))
                screen.blit(overlay, (0, 0))
                pause_txt = font_large.render("PAUSED", True, WHITE)
                screen.blit(pause_txt, (WIDTH // 2 - pause_txt.get_width() // 2, HEIGHT // 2))

        elif state == "GAMEOVER":
            title = font_large.render("GAME OVER", True, RED)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

            score_text = font_medium.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))

            best_text = font_medium.render(f"Best: {highest_score}", True, YELLOW)
            screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, 350))

            pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, 500, 200, 50), border_radius=10)
            play_again = font_medium.render("PLAY AGAIN", True, BG_TOP)
            screen.blit(play_again, (WIDTH // 2 - play_again.get_width() // 2, 512))

            pygame.draw.rect(screen, RED, (WIDTH // 2 - 100, 580, 200, 50), border_radius=10)
            quit_btn = font_medium.render("QUIT", True, BG_TOP)
            screen.blit(quit_btn, (WIDTH // 2 - quit_btn.get_width() // 2, 592))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()