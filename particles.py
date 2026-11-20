import pygame
import random
from settings import *

class Particula:
    def __init__(self, x, y, cor, tamanho, vel_x, vel_y, duracao):
        self.x = x
        self.y = y
        self.cor = cor
        self.tamanho = tamanho
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.duracao = duracao
        self.vida_max = duracao

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.duracao -= 1
        self.tamanho = max(1, self.tamanho * 0.95)

    def desenhar(self, tela):
        if self.duracao > 0:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), int(self.tamanho))

class SmokeClove:
    """Habilidade Q: Cria uma esfera de fumaca roxa/rosa que da lentidao nos inimigos."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 110
        self.duracao = 360 # Dura 6 segundos (60 FPS * 6)

    def atualizar(self):
        self.duracao -= 1

    def desenhar(self, tela):
        if self.duracao > 0:
            superficie = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
            alpha = min(140, int((self.duracao / 360) * 160))
            pygame.draw.circle(superficie, (138, 43, 226, alpha), (self.raio, self.raio), self.raio)
            pygame.draw.circle(superficie, (255, 105, 180, alpha + 40), (self.raio, self.raio), self.raio, 3)
            tela.blit(superficie, (self.x - self.raio, self.y - self.raio))
