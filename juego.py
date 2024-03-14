import pygame
import random
import sys

#Tamaño de la pantalla
WIDTH = 1100
HEIGHT = 800

#Colores del juego
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Cuadro Jugador
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
PLAYER_SPEED = 10

#Cuadro Enemigo
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 70
ENEMY_SPEED = 4
ENEMY_COUNT = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tu Cuadro contra El Mundo")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -ENEMY_HEIGHT)
        self.speedy = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -ENEMY_HEIGHT)
            self.speedy = ENEMY_SPEED

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(ENEMY_COUNT):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

game_over = False

def show_game_over():
    font = pygame.font.Font(None, 64)
    game_over_text = font.render("NI MODO CHOCASTE :)", True, WHITE)
    game_over_text2 = font.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect2 = game_over_text2.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(game_over_text, text_rect)
    screen.blit(game_over_text2, text_rect2)
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        #Colision entre jugador y cuadro enemigo
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True

        screen.fill(BLACK)
        all_sprites.draw(screen)
    else:
        show_game_over()

    pygame.display.flip()
pygame.quit()
sys.exit()