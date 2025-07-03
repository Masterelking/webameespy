import pygame
import sys
import math
import random
from pygame.math import Vector2

# Initialisation de Pygame
pygame.init()

# Configuration de l'écran
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Canne")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (20, 25, 40)
DARKER_BG = (10, 15, 30)
NEON_BLUE = (0, 195, 255)
NEON_RED = (255, 0, 128)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (180, 90, 255)
NEON_ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)

# Positions possibles sur le plateau (9 positions)
POSITIONS = [
    Vector2(200, 100), Vector2(400, 100), Vector2(600, 100),
    Vector2(200, 300), Vector2(400, 300), Vector2(600, 300),
    Vector2(200, 500), Vector2(400, 500), Vector2(600, 500)
]

# Définition des positions adjacentes (incluant les diagonales)
ADJACENT_POSITIONS = [
    [1, 3, 4, 8], # 0: droite, bas, diagonale bas-droite, diagonale bas-droite-loin
    [0, 2, 3, 4, 5, 7], # 1: gauche, droite, diagonale bas-gauche, bas, diagonale bas-droite, bas-loin
    [1, 4, 5, 6], # 2: gauche, diagonale bas-gauche, bas, diagonale bas-gauche-loin
    [0, 1, 4, 6, 7, 8], # 3: haut, diagonale haut-droite, droite, bas, diagonale bas-droite, bas-loin
    [0, 1, 2, 3, 5, 6, 7, 8], # 4: diagonales et adjacents dans toutes les directions
    [1, 2, 4, 6, 7, 8], # 5: haut, diagonale haut-gauche, gauche, bas, diagonale bas-gauche, bas-loin
    [3, 4, 7, 0, 2], # 6: haut, diagonale haut-droite, droite, diagonale haut-droite-loin, diagonale haut-gauche-loin
    [3, 4, 5, 6, 8, 1], # 7: haut-loin, diagonale haut-gauche, haut, diagonale haut-droite, droite, gauche
    [4, 5, 7, 0, 6]  # 8: gauche, diagonale haut-gauche, haut, diagonale haut-droite-loin, diagonale haut-gauche-loin
]

# Position du centre
CENTER_POSITION = 4

# Définition des chemins diagonaux vers le centre
DIAGONAL_TO_CENTER = {
    0: [1, 4],
    2: [1, 4],
    6: [3, 4],
    8: [7, 4]
}

class FloatingBall:
    def __init__(self, x, y, color, size=20, speed_factor=1):
        self.pos = Vector2(x, y)
        self.original_y = y
        self.color = color
        self.size = size
        self.phase = random.uniform(0, 2 * math.pi)
        self.amplitude = random.uniform(30, 100)
        self.speed = random.uniform(0.001, 0.003) * speed_factor
        self.horizontal_speed = random.uniform(-0.2, 0.2)
        
    def update(self):
        # Mouvement vertical sinusoïdal
        self.phase += self.speed
        self.pos.y = self.original_y + math.sin(self.phase) * self.amplitude
        
        # Léger mouvement horizontal
        self.pos.x += self.horizontal_speed
        
        # Rebondir sur les bords
        if self.pos.x < 0 or self.pos.x > WINDOW_WIDTH:
            self.horizontal_speed *= -1
            
    def draw(self, screen):
        # Effet de lueur
        for r in range(3):
            alpha = 100 - r * 30
            glow_color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, glow_color, (int(self.pos.x), int(self.pos.y)), self.size + r * 3)
            
        # Bille principale
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size)
        
        # Reflet
        highlight_size = int(self.size * 0.4)
        highlight_pos = (int(self.pos.x - self.size * 0.3), int(self.pos.y - self.size * 0.3))
        pygame.draw.circle(screen, (255, 255, 255, 180), highlight_pos, highlight_size)

class RisingFallingBall:
    def __init__(self, color, size=20):
        self.color = color
        self.size = size
        self.reset()
        
    def reset(self):
        # Position initiale en bas de l'écran
        self.pos = Vector2(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT + self.size)
        self.speed = random.uniform(1, 3)
        self.life = random.randint(200, 400)  # Durée de vie plus longue
        
    def update(self):
        # Mouvement vers le haut
        self.pos.y -= self.speed
        self.life -= 1
        
        # Réinitialiser si la bille sort de l'écran ou si sa durée de vie est écoulée
        if self.pos.y < -self.size or self.life <= 0:
            self.reset()
            
    def draw(self, screen):
        # Effet de lueur
        for r in range(3):
            alpha = 100 - r * 30
            glow_color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, glow_color, (int(self.pos.x), int(self.pos.y)), self.size + r * 3)
            
        # Bille principale
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size)
        
        # Reflet
        highlight_size = int(self.size * 0.4)
        highlight_pos = (int(self.pos.x - self.size * 0.3), int(self.pos.y - self.size * 0.3))
        pygame.draw.circle(screen, (255, 255, 255, 180), highlight_pos, highlight_size)

class Particle:
    def __init__(self, pos, color, speed=1, size=3, life=30, gravity=0):
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * speed
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity
        
    def update(self):
        self.pos += self.vel
        if self.gravity != 0:
            self.vel.y += self.gravity
        self.life -= 1
        self.size = max(0, self.size * (self.life / self.max_life))
        
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        color = (*self.color[:3], alpha) if len(self.color) > 3 else self.color
        pygame.draw.circle(screen, color, (int(self.pos.x), int(self.pos.y)), int(self.size))

class Ball:
    def __init__(self, color, position, player_name=""):
        self.color = color
        self.position = Vector2(position)
        self.target = Vector2(position)
        self.angle = 0
        self.scale = 1.0
        self.pulse_dir = 0.01
        self.particles = []
        self.trail = []
        self.selected = False
        self.player_name = player_name
        
    def update(self):
        # Animation de déplacement
        direction = self.target - self.position
        if direction.length() > 1:
            move = direction.normalize() * min(direction.length(), 10)
            self.position += move
            self.angle += move.length() * 0.1
            
            # Ajouter des particules lors du mouvement
            if random.random() < 0.3:
                self.particles.append(Particle(self.position, self.color, speed=2, size=5, life=20))
                
            # Ajouter à la traînée
            self.trail.append((Vector2(self.position), 10))
        else:
            self.position = self.target
            
        # Animation de pulsation
        if self.selected:
            self.scale += self.pulse_dir
            if self.scale > 1.2 or self.scale < 0.9:
                self.pulse_dir *= -1
        else:
            self.scale = 1.0
            
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Mettre à jour la traînée
        for i, (pos, life) in enumerate(self.trail[:]):
            self.trail[i] = (pos, life - 1)
        self.trail = [t for t in self.trail if t[1] > 0]

    def draw(self, screen):
        # Dessiner la traînée
        for pos, life in self.trail:
            alpha = int(255 * (life / 10))
            color = (*self.color[:3], alpha) if len(self.color) > 3 else self.color
            size = int(25 * (life / 10))
            pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), size)
        
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Dessiner la bille
        radius = int(25 * self.scale)
        glow_radius = radius + 10
        
        # Effet de lueur
        for r in range(glow_radius, radius, -2):
            alpha = int(100 * (1 - (r - radius) / 10))
            glow_color = (*self.color[:3], alpha) if len(self.color) > 3 else self.color
            pygame.draw.circle(screen, glow_color, (int(self.position.x), int(self.position.y)), r)
            
        # Bille principale
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), radius)
        
        # Reflet
        highlight = (255, 255, 255, 150)
        highlight_pos = (int(self.position.x - radius * 0.3), int(self.position.y - radius * 0.3))
        highlight_size = int(radius * 0.4)
        pygame.draw.circle(screen, highlight, highlight_pos, highlight_size)

class AnimatedButton:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE, icon=None, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.hover = False
        self.click_effect = 0
        self.particles = []
        self.icon = icon
        self.scale = 1.0
        self.pulse_dir = 0.002
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Animation de survol
        target_color = [min(c + 40, 255) if self.hover else c for c in self.base_color]
        for i in range(3):
            self.color = tuple(self.color[i] + (target_color[i] - self.color[i]) * 0.1 for i in range(3))
            
        # Animation de clic
        if self.click_effect > 0:
            self.click_effect -= 1
            
        # Animation de pulsation
        self.scale += self.pulse_dir
        if self.scale > 1.05 or self.scale < 0.95:
            self.pulse_dir *= -1
            
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        # Calculer la taille et la position avec l'échelle
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        x_offset = (scaled_width - self.rect.width) // 2
        y_offset = (scaled_height - self.rect.height) // 2
        
        scaled_rect = pygame.Rect(
            self.rect.x - x_offset,
            self.rect.y - y_offset,
            scaled_width,
            scaled_height
        )
        
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Effet de lueur
        for i in range(3):
            glow_rect = scaled_rect.inflate(6 - i*2, 6 - i*2)
            glow_color = tuple(max(0, c - 40) for c in self.color)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=15)
        
        # Bouton principal
        pygame.draw.rect(screen, self.color, scaled_rect, border_radius=15)
        
        # Effet de clic
        if self.click_effect > 0:
            click_alpha = int(100 * (self.click_effect / 10))
            s = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)
            s.fill((255, 255, 255, click_alpha))
            s.set_alpha(click_alpha)
            screen.blit(s, scaled_rect)
        
        # Texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Icône (si présente)
        if self.icon:
            icon_rect = self.icon.get_rect(midright=(text_rect.left - 10, text_rect.centery))
            screen.blit(self.icon, icon_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.click_effect = 10
            # Ajouter des particules lors du clic
            for _ in range(20):
                self.particles.append(
                    Particle(
                        (random.randint(self.rect.left, self.rect.right), 
                         random.randint(self.rect.top, self.rect.bottom)),
                        self.base_color,
                        speed=3,
                        size=4,
                        life=20
                    )
                )
            return True
        return False

class TabButton(AnimatedButton):
    def __init__(self, x, y, width, height, text, color, text_color=WHITE, active=False):
        super().__init__(x, y, width, height, text, color, text_color)
        self.active = active
        
    def draw(self, screen):
        # Dessiner le fond du bouton
        if self.active:
            # Effet de lueur pour l'onglet actif
            for i in range(3):
                glow_rect = self.rect.inflate(6 - i*2, 6 - i*2)
                glow_color = tuple(max(0, c - 40) for c in self.color)
                # Dessiner seulement le haut, gauche et droite pour l'onglet
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=15)
            pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        else:
            # Onglet inactif
            inactive_color = tuple(max(0, c - 70) for c in self.color)
            pygame.draw.rect(screen, inactive_color, self.rect, border_radius=15)
        
        # Texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class TextInputBox:
    def __init__(self, x, y, width, height, placeholder="", font_size=32, color=NEON_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (60, 60, 80)
        self.border_color = color
        self.text = ""
        self.placeholder = placeholder
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 15  # Limite de caractères
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                # Filtrer les caractères valides
                if event.unicode.isprintable():
                    self.text += event.unicode
        return False
    
    def update(self):
        # Animation du curseur
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        # Dessiner le fond
        border_color = self.border_color if self.active else (100, 100, 120)
        
        # Effet de lueur si actif
        if self.active:
            for i in range(3):
                glow_rect = self.rect.inflate(6 - i*2, 6 - i*2)
                pygame.draw.rect(screen, border_color, glow_rect, border_radius=10)
        
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=10)
        
        # Dessiner le texte ou le placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, WHITE)
        else:
            text_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        
        # Positionner le texte
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)
        
        # Dessiner le curseur si actif
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            if cursor_x < self.rect.right - 10:  # Éviter que le curseur sorte de la boîte
                pygame.draw.line(screen, WHITE, 
                                (cursor_x, self.rect.y + 10), 
                                (cursor_x, self.rect.y + self.rect.height - 10), 2)

class Game:
    def __init__(self, player1_name="Joueur 1", player2_name="Joueur 2"):
        self.board = [None] * 9
        self.current_player = 1
        self.phase = "placement"
        self.placed_balls = {1: 0, 2: 0}
        self.selected_ball = None
        self.winner = None
        self.balls = []
        self.scores = {1: 0, 2: 0}
        self.round = 1
        self.total_rounds = 1
        self.player_names = {1: player1_name, 2: player2_name}
        self.player_colors = {1: NEON_BLUE, 2: NEON_RED}
        self.particles = []
        self.grid_animation = 0
        self.grid_pulse = 0
        self.valid_moves_particles = []
        self.winner_particles = []
        self.confetti = []
        self.transition_alpha = 255
        self.transition_direction = -1
        self.background_balls = []
        self.rising_balls = []
        
        # Créer des billes flottantes en arrière-plan
        for _ in range(15):
            self.background_balls.append(
                FloatingBall(
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT),
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN]),
                    size=random.randint(5, 15)
                )
            )
            
        # Créer des billes qui montent et descendent
        for _ in range(20):
            self.rising_balls.append(
                RisingFallingBall(
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN, NEON_YELLOW]),
                    size=random.randint(5, 15)
                )
            )
        
    def is_valid_move(self, start, end):
        if self.board[end] is not None:
            return False
        if end in ADJACENT_POSITIONS[start]:
            return True
        return False

    def get_valid_moves(self, start):
        return [end for end in range(9) if self.is_valid_move(start, end)]

    def handle_click(self, position):
        if self.winner or self.transition_alpha > 0:
            return

        if self.phase == "placement":
            if self.board[position] is None:
                self.board[position] = self.current_player
                new_ball = Ball(self.player_colors[self.current_player], POSITIONS[position], 
                               self.player_names[self.current_player])
                self.balls.append(new_ball)
                self.placed_balls[self.current_player] += 1
                
                # Ajouter des particules lors du placement
                for _ in range(30):
                    self.particles.append(
                        Particle(
                            POSITIONS[position],
                            self.player_colors[self.current_player],
                            speed=random.uniform(2, 5),
                            size=random.uniform(3, 8),
                            life=random.randint(20, 40)
                        )
                    )

                self.winner = self.check_winner()
                if self.winner:
                    self.scores[self.winner] += 1
                    self.create_winner_particles()
                elif self.placed_balls[1] == 3 and self.placed_balls[2] == 3:
                    self.phase = "movement"
                    # Animation de transition de phase
                    self.transition_alpha = 255
                    self.transition_direction = -1
                else:
                    self.current_player = 3 - self.current_player

        else:  # Phase de mouvement
            if self.selected_ball is None:
                if self.board[position] == self.current_player:
                    self.selected_ball = position
                    # Marquer la bille comme sélectionnée
                    for ball in self.balls:
                        if ball.position == POSITIONS[position]:
                            ball.selected = True
                    
                    # Créer des particules pour les mouvements valides
                    self.valid_moves_particles = []
                    valid_moves = self.get_valid_moves(position)
                    for move in valid_moves:
                        for _ in range(10):
                            self.valid_moves_particles.append(
                                Particle(
                                    POSITIONS[move],
                                    NEON_GREEN,
                                    speed=1,
                                    size=random.uniform(2, 5),
                                    life=random.randint(20, 40)
                                )
                            )
            else:
                if self.is_valid_move(self.selected_ball, position):
                    self.board[position] = self.current_player
                    self.board[self.selected_ball] = None
                    
                    # Désélectionner toutes les billes
                    for ball in self.balls:
                        ball.selected = False
                    
                    for ball in self.balls:
                        if ball.position == POSITIONS[self.selected_ball]:
                            ball.target = Vector2(POSITIONS[position])
                            break
                    
                    # Ajouter des particules lors du mouvement
                    start_pos = POSITIONS[self.selected_ball]
                    end_pos = POSITIONS[position]
                    for _ in range(20):
                        pos = start_pos.lerp(end_pos, random.random())
                        self.particles.append(
                            Particle(
                                pos,
                                self.player_colors[self.current_player],
                                speed=random.uniform(1, 3),
                                size=random.uniform(2, 6),
                                life=random.randint(10, 30)
                            )
                        )
                    
                    self.selected_ball = None
                    self.valid_moves_particles = []

                    self.winner = self.check_winner()
                    if self.winner:
                        self.scores[self.winner] += 1
                        self.create_winner_particles()
                    else:
                        self.current_player = 3 - self.current_player
                else:
                    # Désélectionner la bille si le mouvement n'est pas valide
                    for ball in self.balls:
                        ball.selected = False
                    self.selected_ball = None
                    self.valid_moves_particles = []

    def create_winner_particles(self):
        # Créer une explosion de particules pour célébrer la victoire
        for _ in range(200):
            pos = Vector2(
                random.randint(0, WINDOW_WIDTH),
                random.randint(0, WINDOW_HEIGHT)
            )
            color = self.player_colors[self.winner]
            self.winner_particles.append(
                Particle(
                    pos,
                    color,
                    speed=random.uniform(2, 8),
                    size=random.uniform(3, 10),
                    life=random.randint(30, 90)
                )
            )
            
        # Ajouter des confettis
        for _ in range(100):
            pos = Vector2(
                random.randint(0, WINDOW_WIDTH),
                random.randint(-50, 0)
            )
            color = random.choice([NEON_BLUE, NEON_RED, NEON_GREEN, NEON_YELLOW, NEON_PURPLE, GOLD])
            self.confetti.append(
                Particle(
                    pos,
                    color,
                    speed=random.uniform(1, 3),
                    size=random.uniform(5, 10),
                    life=random.randint(100, 200),
                    gravity=0.05
                )
            )

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] is not None:
                return self.board[combo[0]]
        return None

    def reset(self):
        self.__init__(self.player_names[1], self.player_names[2])

    def next_round(self):
        if self.round < self.total_rounds:
            self.round += 1
            self.board = [None] * 9
            self.current_player = 1
            self.phase = "placement"
            self.placed_balls = {1: 0, 2: 0}
            self.selected_ball = None
            self.winner = None
            self.balls = []
            self.particles = []
            self.valid_moves_particles = []
            self.winner_particles = []
            self.confetti = []
            # Animation de transition
            self.transition_alpha = 255
            self.transition_direction = -1
        else:
            self.winner = 1 if self.scores[1] > self.scores[2] else 2
            if self.scores[1] == self.scores[2]:
                self.winner = 0  # Match nul

    def update(self):
        # Mettre à jour les billes d'arrière-plan
        for ball in self.background_balls:
            ball.update()
            
        # Mettre à jour les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.update()
        
        # Mettre à jour les billes
        for ball in self.balls:
            ball.update()
            
        # Animation de la grille
        self.grid_animation += 0.02
        self.grid_pulse = math.sin(self.grid_animation) * 0.2 + 0.8
        
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Mettre à jour les particules des mouvements valides
        for particle in self.valid_moves_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.valid_moves_particles.remove(particle)
                
        # Mettre à jour les particules de victoire
        for particle in self.winner_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.winner_particles.remove(particle)
                
        # Mettre à jour les confettis
        for confetti in self.confetti[:]:
            confetti.update()
            if confetti.life <= 0 or confetti.pos.y > WINDOW_HEIGHT + 50:
                self.confetti.remove(confetti)
                
        # Animation de transition
        if self.transition_alpha > 0 and self.transition_direction < 0:
            self.transition_alpha = max(0, self.transition_alpha + self.transition_direction * 5)
        elif self.transition_alpha < 255 and self.transition_direction > 0:
            self.transition_alpha = min(255, self.transition_alpha + self.transition_direction * 5)

    def draw(self, screen):
        # Dessiner l'arrière-plan
        screen.fill(DARK_BG)
        
        # Dessiner un motif d'arrière-plan
        for y in range(0, WINDOW_HEIGHT, 40):
            for x in range(0, WINDOW_WIDTH, 40):
                alpha = 20 + int(10 * math.sin(self.grid_animation + x * 0.01 + y * 0.01))
                pygame.draw.circle(screen, (40, 50, 80, alpha), (x, y), 1)
        
        # Dessiner les billes d'arrière-plan
        for ball in self.background_balls:
            ball.draw(screen)
            
        # Dessiner les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.draw(screen)
        
        # Dessiner les particules des mouvements valides
        for particle in self.valid_moves_particles:
            particle.draw(screen)
        
        # Dessiner le plateau avec animation
        for i, pos in enumerate(POSITIONS):
            # Effet de pulsation pour la position sélectionnée
            radius = 30
            if i == self.selected_ball:
                radius = 30 * (1 + math.sin(pygame.time.get_ticks() * 0.01) * 0.2)
                color = NEON_YELLOW
            else:
                color = WHITE
                
            # Effet de grille animée
            for r in range(3):
                alpha = 100 - r * 30
                glow_color = (*color[:3], alpha) if len(color) > 3 else (*color, alpha)
                glow_radius = radius + (3 - r) * 2 * self.grid_pulse
                pygame.draw.circle(screen, glow_color, (int(pos.x), int(pos.y)), int(glow_radius), 1)
            
            # Cercle principal
            pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), int(radius), 2)
            
        # Dessiner les lignes de connexion (incluant les diagonales)
        for i, adjacents in enumerate(ADJACENT_POSITIONS):
            for adj in adjacents:
                start_pos = POSITIONS[i]
                end_pos = POSITIONS[adj]
                # Effet de ligne animée
                alpha = 50 + int(20 * math.sin(self.grid_animation + i * 0.5))
                line_color = (100, 100, 150, alpha)
                pygame.draw.line(screen, line_color, 
                                (int(start_pos.x), int(start_pos.y)), 
                                (int(end_pos.x), int(end_pos.y)), 1)

        # Dessiner les billes
        for ball in self.balls:
            ball.draw(screen)
            
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
            
        # Dessiner les particules de victoire
        for particle in self.winner_particles:
            particle.draw(screen)
            
        # Dessiner les confettis
        for confetti in self.confetti:
            confetti.draw(screen)

        # Afficher les scores avec animation
        self.draw_scores(screen)

        # Afficher l'animation de victoire
        if self.winner:
            self.draw_victory_animation(screen)
            
        # Dessiner l'animation de transition
        if self.transition_alpha > 0:
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(self.transition_alpha)
            s.fill(BLACK)
            screen.blit(s, (0, 0))
            
            if self.transition_alpha > 0:
                font = pygame.font.Font(None, 48)
                if self.phase == "placement":
                    phase_text = "Phase de Placement"
                else:
                    phase_text = "Phase de Mouvement"
                text_surface = font.render(phase_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                
                # Afficher le texte seulement pendant la transition
                if 50 < self.transition_alpha < 200:
                    screen.blit(text_surface, text_rect)

    def draw_scores(self, screen):
        # Créer un panneau de score avec animation
        score_width = 250
        score_height = 120
        score_x = 20
        score_y = 20
        
        # Effet de lueur pour le panneau de score
        for i in range(3):
            glow_rect = pygame.Rect(score_x - i*2, score_y - i*2, 
                                   score_width + i*4, score_height + i*4)
            glow_color = (40, 40, 60, 100 - i*30)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=15)
        
        # Panneau principal
        score_bg = pygame.Rect(score_x, score_y, score_width, score_height)
        pygame.draw.rect(screen, (30, 30, 50, 200), score_bg, border_radius=15)
        
        # Texte des scores
        font = pygame.font.Font(None, 28)
        
        # Score du joueur 1 avec animation
        p1_color = self.player_colors[1]
        if self.current_player == 1 and not self.winner:
            # Animation pour le joueur actuel
            pulse = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.2
            p1_text = f"{self.player_names[1]}: {self.scores[1]}"
            text_surface = font.render(p1_text, True, p1_color)
            text_rect = text_surface.get_rect(topleft=(score_x + 20, score_y + 20))
            # Effet de mise à l'échelle
            scaled_surface = pygame.transform.scale(
                text_surface, 
                (int(text_surface.get_width() * pulse), 
                 int(text_surface.get_height() * pulse))
            )
            scaled_rect = scaled_surface.get_rect(center=text_rect.center)
            screen.blit(scaled_surface, scaled_rect)
        else:
            p1_text = f"{self.player_names[1]}: {self.scores[1]}"
            text_surface = font.render(p1_text, True, p1_color)
            screen.blit(text_surface, (score_x + 20, score_y + 20))
        
        # Score du joueur 2 avec animation
        p2_color = self.player_colors[2]
        if self.current_player == 2 and not self.winner:
            # Animation pour le joueur actuel
            pulse = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.2
            p2_text = f"{self.player_names[2]}: {self.scores[2]}"
            text_surface = font.render(p2_text, True, p2_color)
            text_rect = text_surface.get_rect(topleft=(score_x + 20, score_y + 60))
            # Effet de mise à l'échelle
            scaled_surface = pygame.transform.scale(
                text_surface, 
                (int(text_surface.get_width() * pulse), 
                 int(text_surface.get_height() * pulse))
            )
            scaled_rect = scaled_surface.get_rect(center=text_rect.center)
            screen.blit(scaled_surface, scaled_rect)
        else:
            p2_text = f"{self.player_names[2]}: {self.scores[2]}"
            text_surface = font.render(p2_text, True, p2_color)
            screen.blit(text_surface, (score_x + 20, score_y + 60))

        # Afficher la manche actuelle
        round_text = f"Manche: {self.round}/{self.total_rounds}"
        round_surface = font.render(round_text, True, WHITE)
        round_rect = pygame.Rect(WINDOW_WIDTH - 150, 20, 130, 40)
        
        # Effet de lueur pour le panneau de manche
        for i in range(3):
            glow_rect = round_rect.inflate(i*4, i*4)
            glow_color = (40, 40, 60, 100 - i*30)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=10)
            
        pygame.draw.rect(screen, (30, 30, 50, 200), round_rect, border_radius=10)
        screen.blit(round_surface, (WINDOW_WIDTH - 140, 30))
        
        # Afficher la phase actuelle
        phase_font = pygame.font.Font(None, 28)
        if self.phase == "placement":
            phase_text = "Phase: Placement"
        else:
            phase_text = "Phase: Mouvement"
        phase_surface = phase_font.render(phase_text, True, WHITE)
        phase_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, 20, 160, 40)
        
        # Effet de lueur pour le panneau de phase
        for i in range(3):
            glow_rect = phase_rect.inflate(i*4, i*4)
            glow_color = (40, 40, 60, 100 - i*30)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=10)
            
        pygame.draw.rect(screen, (30, 30, 50, 200), phase_rect, border_radius=10)
        screen.blit(phase_surface, (WINDOW_WIDTH // 2 - 70, 30))
        
        # Bouton de retour au menu principal
        menu_button = AnimatedButton(
            WINDOW_WIDTH - 150, 
            WINDOW_HEIGHT - 60, 
            130, 40, 
            "Menu", 
            NEON_ORANGE,
            font_size=24
        )
        menu_button.update()
        menu_button.draw(screen)
        return menu_button

    def draw_victory_animation(self, screen):
        # Effet de superposition semi-transparente
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(150)
        s.fill(BLACK)
        screen.blit(s, (0, 0))

        # Texte de victoire avec animation
        font = pygame.font.Font(None, 60)
        if self.winner == 0:
            win_text = "Match nul!"
            win_color = WHITE
        else:
            win_text = f"{self.player_names[self.winner]} t'es un 10,"
            win_color = self.player_colors[self.winner]
            
        # Animation de pulsation du texte
        pulse = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.2
        text_surface = font.render(win_text, True, win_color)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        
        # Effet de mise à l'échelle
        scaled_surface = pygame.transform.scale(
            text_surface, 
            (int(text_surface.get_width() * pulse), 
             int(text_surface.get_height() * pulse))
        )
        scaled_rect = scaled_surface.get_rect(center=text_rect.center)
        
        # Effet de lueur autour du texte
        for i in range(5):
            glow_size = 5 - i
            glow_rect = scaled_rect.inflate(glow_size * 10, glow_size * 10)
            glow_color = win_color
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=20)
            
        screen.blit(scaled_surface, scaled_rect)
        
        # Deuxième ligne de texte
        if self.winner != 0:
            second_text = "t'as gagné, c'est zooo!"
            second_surface = font.render(second_text, True, GOLD)
            second_rect = second_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            
            # Effet de mise à l'échelle
            second_scaled = pygame.transform.scale(
                second_surface, 
                (int(second_surface.get_width() * pulse), 
                 int(second_surface.get_height() * pulse))
            )
            second_scaled_rect = second_scaled.get_rect(center=second_rect.center)
            
            # Effet de lueur
            for i in range(5):
                glow_size = 5 - i
                glow_rect = second_scaled_rect.inflate(glow_size * 10, glow_size * 10)
                pygame.draw.rect(screen, GOLD, glow_rect, border_radius=20)
                
            screen.blit(second_scaled, second_scaled_rect)
        
        # Bouton pour continuer
        continue_button = AnimatedButton(
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2 + 120, 
            200, 50, 
            "Continuer", 
            GOLD
        )
        continue_button.update()
        continue_button.draw(screen)
        
        return continue_button

class WelcomeScreen:
    def __init__(self):
        self.rising_balls = []
        self.particles = []
        self.title_animation = 0
        self.title_scale = 1.0
        self.title_dir = 0.001
        self.welcome_text_pos = -100
        self.welcome_text_target = 100
        self.welcome_text_alpha = 0
        self.start_button = AnimatedButton(
            WINDOW_WIDTH // 2 - 150, 
            WINDOW_HEIGHT // 2 + 100, 
            300, 70, 
            "C'est parti !", 
            NEON_GREEN,
            font_size=42
        )
        
        # Créer des billes qui montent et descendent
        for _ in range(30):
            self.rising_balls.append(
                RisingFallingBall(
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN, NEON_YELLOW]),
                    size=random.randint(10, 30)
                )
            )
    
    def update(self):
        # Mettre à jour les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.update()
            
        # Animation du texte de bienvenue
        if self.welcome_text_pos < self.welcome_text_target:
            self.welcome_text_pos += (self.welcome_text_target - self.welcome_text_pos) * 0.05
            self.welcome_text_alpha = min(255, self.welcome_text_alpha + 5)
            
        # Mettre à jour le bouton
        self.start_button.update()
        
        # Animation du titre
        self.title_animation += 0.02
        self.title_scale += self.title_dir
        if self.title_scale > 1.1 or self.title_scale < 0.9:
            self.title_dir *= -1
            
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Ajouter des particules aléatoires
        if random.random() < 0.1:
            self.particles.append(
                Particle(
                    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN, NEON_YELLOW]),
                    speed=random.uniform(0.5, 2),
                    size=random.uniform(2, 5),
                    life=random.randint(30, 60)
                )
            )
    
    def draw(self, screen):
        # Dessiner l'arrière-plan
        screen.fill(DARK_BG)
        
        # Dessiner un motif d'arrière-plan
        for y in range(0, WINDOW_HEIGHT, 40):
            for x in range(0, WINDOW_WIDTH, 40):
                alpha = 20 + int(10 * math.sin(self.title_animation + x * 0.01 + y * 0.01))
                pygame.draw.circle(screen, (40, 50, 80, alpha), (x, y), 1)
        
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Dessiner les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.draw(screen)
        
        # Dessiner le titre avec animation
        font = pygame.font.Font(None, int(80 * self.title_scale))
        welcome_text = "Bienvenue sur Canne"
        
        # Effet de dégradé pour le texte
        colors = [NEON_BLUE, NEON_PURPLE, NEON_RED, NEON_YELLOW, NEON_GREEN]
        text_width = font.size(welcome_text)[0]
        char_width = text_width / len(welcome_text)
        
        # Dessiner chaque caractère avec une couleur différente
        x_pos = WINDOW_WIDTH // 2 - text_width // 2
        for i, char in enumerate(welcome_text):
            color_idx = i % len(colors)
            color = colors[color_idx]
            
            # Effet de pulsation de couleur
            pulse = (math.sin(pygame.time.get_ticks() * 0.002 + i * 0.3) + 1) / 2
            mixed_color = tuple(int(c1 + (c2 - c1) * pulse) for c1, c2 in zip(color, colors[(color_idx + 1) % len(colors)]))
            
            # Effet de rebond vertical
            y_offset = math.sin(self.title_animation + i * 0.3) * 10
            
            char_surface = font.render(char, True, mixed_color)
            screen.blit(char_surface, (x_pos, self.welcome_text_pos + y_offset))
            x_pos += char_width
            
        # Dessiner une ligne décorative sous le texte
        line_y = self.welcome_text_pos + 100
        line_width = 500
        line_x = WINDOW_WIDTH // 2 - line_width // 2
        
        # Animation de la ligne
        for i in range(5):
            line_alpha = min(200, self.welcome_text_alpha) - i * 40
            if line_alpha > 0:  # S'assurer que l'alpha est positif
                line_color = (200, 200, 200, line_alpha)
                line_offset = math.sin(pygame.time.get_ticks() * 0.002 + i * 0.5) * 5
                pygame.draw.line(
                    screen, 
                    line_color, 
                    (line_x, line_y + line_offset), 
                    (line_x + line_width, line_y + line_offset), 
                    2
                )
        
        # Dessiner le bouton de démarrage
        self.start_button.draw(screen)
        
        # Dessiner le texte de copyright
        font = pygame.font.Font(None, 20)
        copyright_text = "© 2025 - Canne"
        text_surface = font.render(copyright_text, True, (150, 150, 150))
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT - 30))

class GameModeSelect:
    def __init__(self, shared_rising_balls):
        self.rising_balls = shared_rising_balls
        self.particles = []
        self.animation_time = 0
        self.back_button = AnimatedButton(20, 20, 100, 40, "Retour", NEON_RED)
        
        # Créer les boutons de mode de jeu
        self.mode_buttons = []
        
        # Mode Carreaux Chinois
        self.mode_buttons.append({
            "button": AnimatedButton(
                WINDOW_WIDTH // 2 - 300, 
                WINDOW_HEIGHT // 2 - 100, 
                250, 200, 
                "", 
                NEON_BLUE
            ),
            "name": "Carreaux Chinois",
            "mode": "carreaux"
        })
        
        # Mode Bottle Line
        self.mode_buttons.append({
            "button": AnimatedButton(
                WINDOW_WIDTH // 2 + 50, 
                WINDOW_HEIGHT // 2 - 100, 
                250, 200, 
                "", 
                NEON_RED
            ),
            "name": "Bottle Line",
            "mode": "bottle"
        })
    
    def update(self):
        # Mettre à jour les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.update()
            
        # Mettre à jour l'animation
        self.animation_time += 0.02
        
        # Mettre à jour le bouton de retour
        self.back_button.update()
        
        # Mettre à jour les boutons de mode
        for button_data in self.mode_buttons:
            button_data["button"].update()
            
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Ajouter des particules aléatoires
        if random.random() < 0.05:
            self.particles.append(
                Particle(
                    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN]),
                    speed=random.uniform(0.5, 2),
                    size=random.uniform(2, 5),
                    life=random.randint(30, 60)
                )
            )
    
    def draw(self, screen):
        # Dessiner l'arrière-plan
        screen.fill(DARK_BG)
        
        # Dessiner un motif d'arrière-plan
        for y in range(0, WINDOW_HEIGHT, 40):
            for x in range(0, WINDOW_WIDTH, 40):
                alpha = 20 + int(10 * math.sin(self.animation_time + x * 0.01 + y * 0.01))
                pygame.draw.circle(screen, (40, 50, 80, alpha), (x, y), 1)
        
        # Dessiner les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.draw(screen)
            
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Dessiner un titre
        font = pygame.font.Font(None, 60)
        title_text = "Sélectionner le Mode"
        text_surface = font.render(title_text, True, WHITE)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 80))
        
        # Dessiner une ligne décorative sous le titre
        line_y = 150
        line_width = 400
        line_x = WINDOW_WIDTH // 2 - line_width // 2
        pygame.draw.line(screen, WHITE, (line_x, line_y), (line_x + line_width, line_y), 2)
        
        # Dessiner les boutons de mode
        for button_data in self.mode_buttons:
            button = button_data["button"]
            button.draw(screen)
            
            # Dessiner le design du mode à l'intérieur du bouton
            if button_data["mode"] == "carreaux":
                # Design pour Carreaux Chinois
                center_x = button.rect.centerx
                center_y = button.rect.centery - 20
                radius = 30
                
                # Dessiner un mini plateau
                positions = [
                    (center_x - radius, center_y - radius),
                    (center_x, center_y - radius),
                    (center_x + radius, center_y - radius),
                    (center_x - radius, center_y),
                    (center_x, center_y),
                    (center_x + radius, center_y),
                    (center_x - radius, center_y + radius),
                    (center_x, center_y + radius),
                    (center_x + radius, center_y + radius)
                ]
                
                # Dessiner les positions
                for pos in positions:
                    pygame.draw.circle(screen, WHITE, pos, 5, 1)
                    
                # Dessiner quelques lignes de connexion
                pygame.draw.line(screen, WHITE, positions[0], positions[1], 1)
                pygame.draw.line(screen, WHITE, positions[1], positions[2], 1)
                pygame.draw.line(screen, WHITE, positions[3], positions[4], 1)
                pygame.draw.line(screen, WHITE, positions[4], positions[5], 1)
                pygame.draw.line(screen, WHITE, positions[6], positions[7], 1)
                pygame.draw.line(screen, WHITE, positions[7], positions[8], 1)
                pygame.draw.line(screen, WHITE, positions[0], positions[3], 1)
                pygame.draw.line(screen, WHITE, positions[3], positions[6], 1)
                pygame.draw.line(screen, WHITE, positions[1], positions[4], 1)
                pygame.draw.line(screen, WHITE, positions[4], positions[7], 1)
                pygame.draw.line(screen, WHITE, positions[2], positions[5], 1)
                pygame.draw.line(screen, WHITE, positions[5], positions[8], 1)
                
                # Dessiner quelques billes
                pygame.draw.circle(screen, NEON_BLUE, positions[0], 8)
                pygame.draw.circle(screen, NEON_RED, positions[2], 8)
                pygame.draw.circle(screen, NEON_BLUE, positions[4], 8)
                pygame.draw.circle(screen, NEON_RED, positions[6], 8)
                pygame.draw.circle(screen, NEON_BLUE, positions[8], 8)
                
            else:
                # Design pour Bottle Line
                center_x = button.rect.centerx
                center_y = button.rect.centery - 20
                
                # Dessiner une bouteille stylisée
                bottle_neck_top = (center_x, center_y - 40)
                bottle_neck_bottom = (center_x, center_y - 20)
                bottle_left_top = (center_x - 30, center_y - 20)
                bottle_right_top = (center_x + 30, center_y - 20)
                bottle_left_bottom = (center_x - 30, center_y + 40)
                bottle_right_bottom = (center_x + 30, center_y + 40)
                
                # Dessiner le contour de la bouteille
                pygame.draw.line(screen, WHITE, bottle_neck_top, bottle_neck_bottom, 2)
                pygame.draw.line(screen, WHITE, bottle_left_top, bottle_right_top, 2)
                pygame.draw.line(screen, WHITE, bottle_left_top, bottle_left_bottom, 2)
                pygame.draw.line(screen, WHITE, bottle_right_top, bottle_right_bottom, 2)
                pygame.draw.line(screen, WHITE, bottle_left_bottom, bottle_right_bottom,  2)
                pygame.draw.line(screen, WHITE, bottle_left_bottom, bottle_right_bottom, 2)
                
                # Dessiner quelques billes dans la bouteille
                pygame.draw.circle(screen, NEON_RED, (center_x, center_y), 8)
                pygame.draw.circle(screen, NEON_BLUE, (center_x - 15, center_y + 15), 8)
                pygame.draw.circle(screen, NEON_RED, (center_x + 15, center_y + 15), 8)
                pygame.draw.circle(screen, NEON_BLUE, (center_x, center_y + 30), 8)
            
            # Dessiner le nom du mode
            name_font = pygame.font.Font(None, 28)
            name_surface = name_font.render(button_data["name"], True, WHITE)
            name_rect = name_surface.get_rect(center=(button.rect.centerx, button.rect.bottom - 30))
            screen.blit(name_surface, name_rect)
            
        # Dessiner le bouton de retour
        self.back_button.draw(screen)

class RoundSelect:
    def __init__(self, shared_rising_balls):
        self.rising_balls = shared_rising_balls
        self.particles = []
        self.animation_time = 0
        self.back_button = AnimatedButton(20, 20, 100, 40, "Retour", NEON_RED)
        
        # Créer les boutons de sélection de manches
        self.round_buttons = []
        
        button_width = 250
        button_height = 80
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        # 1 Manche
        self.round_buttons.append({
            "button": AnimatedButton(
                button_x, 200, button_width, button_height, 
                "1 Manche", NEON_BLUE
            ),
            "rounds": 1
        })
        
        # 3 Manches
        self.round_buttons.append({
            "button": AnimatedButton(
                button_x, 300, button_width, button_height, 
                "3 Manches", NEON_GREEN
            ),
            "rounds": 3
        })
        
        # 5 Manches
        self.round_buttons.append({
            "button": AnimatedButton(
                button_x, 400, button_width, button_height, 
                "5 Manches", NEON_PURPLE
            ),
            "rounds": 5
        })
        
        # Bouton pour continuer
        self.continue_button = AnimatedButton(
            WINDOW_WIDTH // 2 - 100, 
            500, 
            200, 60, 
            "Continuer", 
            GOLD
        )
    
    def update(self):
        # Mettre à jour les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.update()
            
        # Mettre à jour l'animation
        self.animation_time += 0.02
        
        # Mettre à jour le bouton de retour
        self.back_button.update()
        
        # Mettre à jour les boutons de manches
        for button_data in self.round_buttons:
            button_data["button"].update()
            
        # Mettre à jour le bouton continuer
        self.continue_button.update()
            
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Ajouter des particules aléatoires
        if random.random() < 0.05:
            self.particles.append(
                Particle(
                    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN]),
                    speed=random.uniform(0.5, 2),
                    size=random.uniform(2, 5),
                    life=random.randint(30, 60)
                )
            )
    
    def draw(self, screen):
        # Dessiner l'arrière-plan
        screen.fill(DARK_BG)
        
        # Dessiner un motif d'arrière-plan
        for y in range(0, WINDOW_HEIGHT, 40):
            for x in range(0, WINDOW_WIDTH, 40):
                alpha = 20 + int(10 * math.sin(self.animation_time + x * 0.01 + y * 0.01))
                pygame.draw.circle(screen, (40, 50, 80, alpha), (x, y), 1)
        
        # Dessiner les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.draw(screen)
            
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Dessiner un titre
        font = pygame.font.Font(None, 60)
        title_text = "Nombre de Manches"
        text_surface = font.render(title_text, True, WHITE)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 80))
        
        # Dessiner une ligne décorative sous le titre
        line_y = 150
        line_width = 400
        line_x = WINDOW_WIDTH // 2 - line_width // 2
        pygame.draw.line(screen, WHITE, (line_x, line_y), (line_x + line_width, line_y), 2)
        
        # Dessiner les boutons de manches
        for button_data in self.round_buttons:
            button_data["button"].draw(screen)
            
        # Dessiner le bouton continuer
        self.continue_button.draw(screen)
            
        # Dessiner le bouton de retour
        self.back_button.draw(screen)

class PlayerNameInput:
    def __init__(self, shared_rising_balls, player_num=1):
        self.rising_balls = shared_rising_balls
        self.particles = []
        self.animation_time = 0
        self.player_num = player_num
        self.back_button = AnimatedButton(20, 20, 100, 40, "Retour", NEON_RED)
        self.continue_button = AnimatedButton(
            WINDOW_WIDTH // 2 - 100, 
            400, 
            200, 50, 
            "Continuer", 
            NEON_GREEN
        )
        
        # Couleur en fonction du joueur
        input_color = NEON_BLUE if player_num == 1 else NEON_RED
        
        self.name_input = TextInputBox(
            WINDOW_WIDTH // 2 - 150,
            250,
            300,
            50,
            f"Nom du Joueur {player_num}",
            font_size=32,
            color=input_color
        )
    
    def update(self, events):
        # Mettre à jour les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.update()
            
        # Mettre à jour l'animation
        self.animation_time += 0.02
        
        # Mettre à jour les boutons
        self.back_button.update()
        self.continue_button.update()
        
        # Mettre à jour le champ de saisie
        self.name_input.update()
        
        # Gérer les événements pour le champ de saisie
        enter_pressed = False
        for event in events:
            if self.name_input.handle_event(event):
                enter_pressed = True
                
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # Ajouter des particules aléatoires
        if random.random() < 0.05:
            self.particles.append(
                Particle(
                    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
                    random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN]),
                    speed=random.uniform(0.5, 2),
                    size=random.uniform(2, 5),
                    life=random.randint(30, 60)
                )
            )
            
        return enter_pressed
    
    def draw(self, screen):
        # Dessiner l'arrière-plan
        screen.fill(DARK_BG)
        
        # Dessiner un motif d'arrière-plan
        for y in range(0, WINDOW_HEIGHT, 40):
            for x in range(0, WINDOW_WIDTH, 40):
                alpha = 20 + int(10 * math.sin(self.animation_time + x * 0.01 + y * 0.01))
                pygame.draw.circle(screen, (40, 50, 80, alpha), (x, y), 1)
        
        # Dessiner les billes qui montent et descendent
        for ball in self.rising_balls:
            ball.draw(screen)
            
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Dessiner un titre
        font = pygame.font.Font(None, 60)
        title_text = f"Joueur {self.player_num}"
        text_color = NEON_BLUE if self.player_num == 1 else NEON_RED
        text_surface = font.render(title_text, True, text_color)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 80))
        
        # Dessiner une ligne décorative sous le titre
        line_y = 150
        line_width = 400
        line_x = WINDOW_WIDTH // 2 - line_width // 2
        pygame.draw.line(screen, text_color, (line_x, line_y), (line_x + line_width, line_y), 2)
        
        # Dessiner le champ de saisie
        self.name_input.draw(screen)
        
        # Dessiner les boutons
        self.back_button.draw(screen)
        self.continue_button.draw(screen)
        
        # Dessiner un texte d'instruction
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = "Entrez votre nom et appuyez sur Entrée ou cliquez sur Continuer"
        instruction_surface = instruction_font.render(instruction_text, True, (200, 200, 200))
        screen.blit(instruction_surface, (WINDOW_WIDTH // 2 - instruction_surface.get_width() // 2, 320))

def main():
    clock = pygame.time.Clock()
    
    # États du jeu
    WELCOME = 0
    MODE_SELECT = 1
    ROUND_SELECT = 2
    PLAYER1_NAME = 3
    PLAYER2_NAME = 4
    GAME = 5
    
    game_state = WELCOME
    selected_mode = "carreaux"  # Par défaut: Carreaux Chinois
    selected_rounds = 1
    player1_name = "Joueur 1"
    player2_name = "Joueur 2"
    
    # Initialiser le menu principal
    welcome_screen = WelcomeScreen()
    
    # Créer des billes qui montent et descendent pour les partager entre les écrans
    shared_rising_balls = []
    for _ in range(30):
        shared_rising_balls.append(
            RisingFallingBall(
                random.choice([NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_GREEN, NEON_YELLOW]),
                size=random.randint(5, 20)
            )
        )
    
    # Initialiser les écrans de sélection
    game_mode_select = GameModeSelect(shared_rising_balls)
    round_select = RoundSelect(shared_rising_balls)
    player1_input = PlayerNameInput(shared_rising_balls, 1)
    player2_input = PlayerNameInput(shared_rising_balls, 2)
    
    # Initialiser le jeu
    game = None
    menu_button = None
    continue_button = None

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == WELCOME:
                    if welcome_screen.start_button.is_clicked(event.pos):
                        game_state = MODE_SELECT
                
                elif game_state == MODE_SELECT:
                    if game_mode_select.back_button.is_clicked(event.pos):
                        game_state = WELCOME
                    else:
                        for button_data in game_mode_select.mode_buttons:
                            if button_data["button"].is_clicked(event.pos):
                                selected_mode = button_data["mode"]
                                game_state = ROUND_SELECT
                
                elif game_state == ROUND_SELECT:
                    if round_select.back_button.is_clicked(event.pos):
                        game_state = MODE_SELECT
                    elif round_select.continue_button.is_clicked(event.pos):
                        game_state = PLAYER1_NAME
                    else:
                        for button_data in round_select.round_buttons:
                            if button_data["button"].is_clicked(event.pos):
                                selected_rounds = button_data["rounds"]
                
                elif game_state == PLAYER1_NAME:
                    if player1_input.back_button.is_clicked(event.pos):
                        game_state = ROUND_SELECT
                    elif player1_input.continue_button.is_clicked(event.pos):
                        player1_name = player1_input.name_input.text if player1_input.name_input.text else "Joueur 1"
                        game_state = PLAYER2_NAME
                
                elif game_state == PLAYER2_NAME:
                    if player2_input.back_button.is_clicked(event.pos):
                        game_state = PLAYER1_NAME
                    elif player2_input.continue_button.is_clicked(event.pos):
                        player2_name = player2_input.name_input.text if player2_input.name_input.text else "Joueur 2"
                        game = Game(player1_name, player2_name)
                        game.total_rounds = selected_rounds
                        game.transition_alpha = 255
                        game.transition_direction = -1
                        game_state = GAME
                
                elif game_state == GAME:
                    if menu_button and menu_button.is_clicked(event.pos):
                        game_state = WELCOME
                        welcome_screen = WelcomeScreen()
                    elif game.winner and continue_button and continue_button.is_clicked(event.pos):
                        if game.round < game.total_rounds:
                            game.next_round()
                        else:
                            game_state = WELCOME
                            welcome_screen = WelcomeScreen()
                    else:
                        # Gestion du jeu
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_pos = next((i for i, pos in enumerate(POSITIONS) if (mouse_pos[0] - pos.x)**2 + (mouse_pos[1] - pos.y)**2 < 900), None)
                        if clicked_pos is not None:
                            game.handle_click(clicked_pos)

        # Mise à jour
        if game_state == WELCOME:
            welcome_screen.update()
        elif game_state == MODE_SELECT:
            game_mode_select.update()
        elif game_state == ROUND_SELECT:
            round_select.update()
        elif game_state == PLAYER1_NAME:
            enter_pressed = player1_input.update(events)
            if enter_pressed:
                player1_name = player1_input.name_input.text if player1_input.name_input.text else "Joueur 1"
                game_state = PLAYER2_NAME
        elif game_state == PLAYER2_NAME:
            enter_pressed = player2_input.update(events)
            if enter_pressed:
                player2_name = player2_input.name_input.text if player2_input.name_input.text else "Joueur 2"
                game = Game(player1_name, player2_name)
                game.total_rounds = selected_rounds
                game.transition_alpha = 255
                game.transition_direction = -1
                game_state = GAME
        elif game_state == GAME:
            game.update()

        # Rendu
        if game_state == WELCOME:
            welcome_screen.draw(screen)
        elif game_state == MODE_SELECT:
            game_mode_select.draw(screen)
        elif game_state == ROUND_SELECT:
            round_select.draw(screen)
        elif game_state == PLAYER1_NAME:
            player1_input.draw(screen)
        elif game_state == PLAYER2_NAME:
            player2_input.draw(screen)
        elif game_state == GAME:
            game.draw(screen)
            menu_button = game.draw_scores(screen)
            if game.winner:
                continue_button = game.draw_victory_animation(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
