import pygame
import sys
import random

# Colores
negro = (0, 0, 0)
gris = (124, 130, 133)
verde = (0, 255, 0)
azul_claro = (100, 149, 237)
amarillo = (255, 250, 0)
rosa = (255, 192, 203)
naranja = (255, 165, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)
blanco = (255, 255, 255)

# Colores únicos para los carros
colores_unicos = [
    rojo, azul, naranja, rosa, verde, amarillo, blanco, gris,
    (128, 0, 128),      # púrpura
    (0, 255, 255),      # cian
    (255, 105, 180),    # rosa fuerte
    (0, 100, 0),        # verde oscuro
    (210, 105, 30),     # chocolate
    (75, 0, 130),       # índigo
    (255, 20, 147),     # rosa profundo
    (0, 191, 255),      # azul cielo
    (255, 140, 0),      # naranja oscuro
    (127, 255, 212),    # aguamarina
    (220, 20, 60)       # carmesí
]

# Inicialización
pygame.init()
ventana = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Crossy Road")
clock = pygame.time.Clock()

# Fuente y vidas
fuente = pygame.font.SysFont("arial", 36)
vidas = 3

# Sprite Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 550
        self.vel = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if teclas[pygame.K_UP]:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.vel

        self.rect.x = max(0, min(self.rect.x, 900 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 700 - self.rect.height))

    def draw(self, surface):
        x = self.rect.x
        y = self.rect.y
        pygame.draw.rect(surface, amarillo, (x, y, 50, 50))
        pygame.draw.rect(surface, amarillo, (x+50, y+8, 15, 35))
        pygame.draw.rect(surface, amarillo, (x-15, y+8, 15, 35))
        pygame.draw.rect(surface, amarillo, (x+7, y-10, 35, 15))
        pygame.draw.rect(surface, negro, (x+28, y+5, 13, 13))
        pygame.draw.rect(surface, negro, (x+10, y+5, 13, 13))
        pygame.draw.rect(surface, naranja, (x+20, y+15, 11, 11))
        pygame.draw.rect(surface, rosa, (x+35, y+18, 11, 11))
        pygame.draw.rect(surface, rosa, (x+5, y+18, 11, 11))
        pygame.draw.rect(surface, naranja, (x+35, y+50, 10, 20))
        pygame.draw.rect(surface, naranja, (x+10, y+50, 10, 20))

# Sprite Carro
class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, color, velocidad):
        super().__init__()
        self.image = pygame.Surface((60, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        if self.velocidad > 0 and self.rect.left > 900:
            self.rect.right = 0
        elif self.velocidad < 0 and self.rect.right < 0:
            self.rect.left = 900

# Grupos
jugador = Jugador()
grupo_jugador = pygame.sprite.Group(jugador)
grupo_carros = pygame.sprite.Group()

# Barajar colores y usarlos sin repetir
random.shuffle(colores_unicos)
color_index = 0

# Carros del carril superior (hacia la derecha, y = 130)
for _ in range(6):
    x = random.randint(-2000, 0)
    velocidad = random.choice([2, 3, 4])
    color = colores_unicos[color_index % len(colores_unicos)]
    color_index += 1
    grupo_carros.add(Carro(x, 130, color, velocidad))

# Carros del carril del medio (hacia la derecha, y = 320)
for _ in range(8):
    x = random.randint(-2000, 0)
    velocidad = random.choice([3, 5, 6])
    color = colores_unicos[color_index % len(colores_unicos)]
    color_index += 1
    grupo_carros.add(Carro(x, 320, color, velocidad))

# Carros del carril inferior (hacia la izquierda, y = 370)
for _ in range(8):
    x = random.randint(900, 2500)
    velocidad = -random.choice([2, 4, 5, 6])
    color = colores_unicos[color_index % len(colores_unicos)]
    color_index += 1
    grupo_carros.add(Carro(x, 370, color, velocidad))

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jugador.update()
    grupo_carros.update()

    # Colisiones
    if pygame.sprite.spritecollideany(jugador, grupo_carros):
        print("¡Colisión!")
        vidas -= 1
        jugador.rect.x, jugador.rect.y = 400, 550
        pygame.time.delay(500)
        if vidas == 0:
            ventana.fill(negro)
            texto_gameover = fuente.render("GAME OVER", True, rojo)
            ventana.blit(texto_gameover, (350, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

    ventana.fill(azul_claro)

    # Fondo
    pygame.draw.rect(ventana, verde, (0, 1, 900, 200))
    pygame.draw.rect(ventana, verde, (0, 500, 900, 200))
    pygame.draw.rect(ventana, negro, (0, 290, 900, 160))
    pygame.draw.rect(ventana, gris, (0, 450, 900, 50))
    pygame.draw.rect(ventana, gris, (0, 240, 900, 50))
    pygame.draw.rect(ventana, gris, (0, 50, 900, 50))
    pygame.draw.rect(ventana, negro, (0, 100, 900, 150))
    for x in [20, 240, 450, 650]:
        pygame.draw.rect(ventana, amarillo, (x, 160, 170, 20))
        pygame.draw.rect(ventana, amarillo, (x, 355, 170, 20))

    grupo_carros.draw(ventana)
    jugador.draw(ventana)

    # Dibujar vidas
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, blanco)
    ventana.blit(texto_vidas, (20, 20))

    pygame.display.update()
    clock.tick(60)
   