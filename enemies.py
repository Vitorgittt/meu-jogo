import pygame
import math
import random
from settings import *
from sprites import SPRITES

class OrbeEssencia:
    """Dropado pelos inimigos para carregar a Ultimate e dar Cristais."""
    def __init__(self, x, y, valor_cristal=10):
        self.x = x
        self.y = y
        self.raio = 7
        self.valor_cristal = valor_cristal
        self.tempo_vida = 600 # Dura 10 segundos no chao

    def atualizar(self, player):
        self.tempo_vida -= 1
        # Ima suave quando a Clove chega perto
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist < 130:
            angulo = math.atan2(player.y - self.y, player.x - self.x)
            self.x += math.cos(angulo) * 4.5
            self.y += math.sin(angulo) * 4.5

    def desenhar(self, tela):
        pygame.draw.circle(tela, CLOVE_ROSA, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 3)

class Inimigo:
    def __init__(self, onda, tipo="padrao"):
        self.tipo = tipo
        
        # Nasce fora das bordas da tela
        lado = random.choice(["cima", "baixo", "esquerda", "direita"])
        if lado == "cima":
            self.x, self.y = random.randint(0, LARGURA), -30
        elif lado == "baixo":
            self.x, self.y = random.randint(0, LARGURA), ALTURA + 30
        elif lado == "esquerda":
            self.x, self.y = -30, random.randint(0, ALTURA)
        else:
            self.x, self.y = LARGURA + 30, random.randint(0, ALTURA)

        # Configura atributos por tipo de inimigo do Valorant
        if tipo == "rush": # Duelista rapido (Jett/Neon)
            self.nome = "Duelista Rushando"
            self.raio = 14
            self.vida_max = 35 + (onda * 10)
            self.velocidade = 3.8 + (onda * 0.1)
            self.dano = 12
            self.cor = CLOVE_CIANO
            self.recompensa = 15
        elif tipo == "tanque": # Pesado / Ping Alto
            self.nome = "Lag de 999ms"
            self.raio = 26
            self.vida_max = 120 + (onda * 25)
            self.velocidade = 1.6
            self.dano = 25
            self.cor = (255, 140, 0) # Laranja
            self.recompensa = 30
        elif tipo == "boss": # Chefao a cada 5 ondas
            self.nome = "CHEFAO: O MATCHMAKING INJUSTO"
            self.raio = 48
            self.vida_max = 800 + (onda * 150)
            self.velocidade = 2.0
            self.dano = 35
            self.cor = VERMELHO_ALERTA
            self.recompensa = 150
        else: # Bot padrao
            self.nome = "Bot Inimigo"
            self.raio = 18
            self.vida_max = 50 + (onda * 12)
            self.velocidade = 2.4 + (onda * 0.08)
            self.dano = 15
            self.cor = VERMELHO_ALERTA
            self.recompensa = 10

        self.vida = self.vida_max

    def mover(self, player, smokes):
        # Verifica se esta dentro de alguma Smoke da Clove (fica 60% mais lento)
        fator_lentidao = 1.0
        for smoke in smokes:
            if math.hypot(self.x - smoke.x, self.y - smoke.y) < smoke.raio:
                fator_lentidao = 0.4
                break

        angulo = math.atan2(player.y - self.y, player.x - self.x)
        self.x += math.cos(angulo) * self.velocidade * fator_lentidao
        self.y += math.sin(angulo) * self.velocidade * fator_lentidao

    def desenhar(self, tela):
     if self.tipo == "tanque":
         img = SPRITES["lag"]
         rect = img.get_rect(center=(int(self.x), int(self.y)))
         tela.blit(img, rect)
     elif self.tipo == "boss":
         # Chefao usa o sprite do Bot ampliado em 2.5x!
         img = pygame.transform.scale(SPRITES["bot"], (95, 95))
         rect = img.get_rect(center=(int(self.x), int(self.y)))
         tela.blit(img, rect)
     else:
         img = SPRITES["bot"]
         if self.tipo == "rush": # Duelista ganha tom azulado rapido
             img = img.copy()
             img.fill(CLOVE_CIANO, special_flags=pygame.BLEND_MULT)
         rect = img.get_rect(center=(int(self.x), int(self.y)))
         tela.blit(img, rect)

     # Barra de vida acima do inimigo
     if self.vida < self.vida_max:
         largura_barra = self.raio * 2
         pct_vida = max(0, self.vida / self.vida_max)
         pygame.draw.rect(tela, (50, 50, 50), (self.x - self.raio, self.y - self.raio - 14, largura_barra, 5))
         pygame.draw.rect(tela, VERDE_VIDA, (self.x - self.raio, self.y - self.raio - 14, largura_barra * pct_vida, 5))
