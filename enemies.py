import pygame
import math
import random
from settings import *
from sprites import SPRITES

class ProjetilInimigo:
    """Tiros disparados pelos Chefoes contra a Clove."""
    def __init__(self, x, y, alvo_x, alvo_y, dano, velocidade=6, cor=VERMELHO_ALERTA):
        self.x = x
        self.y = y
        self.dano = dano
        self.cor = cor
        self.raio = 8
        angulo = math.atan2(alvo_y - y, alvo_x - x)
        self.vel_x = math.cos(angulo) * velocidade
        self.vel_y = math.sin(angulo) * velocidade

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 3)

class OrbeEssencia:
    def __init__(self, x, y, valor_cristal=10):
        self.x = x
        self.y = y
        self.raio = 7
        self.valor_cristal = valor_cristal
        self.tempo_vida = 600

    def atualizar(self, player):
        self.tempo_vida -= 1
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist < 130:
            angulo = math.atan2(player.y - self.y, player.x - self.x)
            self.x += math.cos(angulo) * 4.5
            self.y += math.sin(angulo) * 4.5

    def desenhar(self, tela):
        rect = SPRITES["orbe"].get_rect(center=(int(self.x), int(self.y)))
        tela.blit(SPRITES["orbe"], rect)

class Inimigo:
    def __init__(self, onda, tipo="padrao"):
        self.tipo = tipo
        self.eh_boss = tipo.startswith("boss")
        self.timer_habilidade = 120 # Tempo para usar ataque especial
        
        lado = random.choice(["cima", "baixo", "esquerda", "direita"])
        if lado == "cima":
            self.x, self.y = random.randint(0, LARGURA), -40
        elif lado == "baixo":
            self.x, self.y = random.randint(0, LARGURA), ALTURA + 40
        elif lado == "esquerda":
            self.x, self.y = -40, random.randint(0, ALTURA)
        else:
            self.x, self.y = LARGURA + 40, random.randint(0, ALTURA)

        # --- INIMIGOS COMUNS ---
        if tipo == "rush":
            self.nome = "Duelista Rushando"
            self.raio = 16
            self.vida_max = 35 + (onda * 10)
            self.velocidade = 3.8 + (onda * 0.1)
            self.dano = 12
            self.cor = CLOVE_CIANO
            self.recompensa = 15
        elif tipo == "tanque":
            self.nome = "Lag de 999ms"
            self.raio = 26
            self.vida_max = 120 + (onda * 25)
            self.velocidade = 1.6
            self.dano = 25
            self.cor = (255, 140, 0)
            self.recompensa = 30
        elif tipo == "padrao":
            self.nome = "Bot Inimigo"
            self.raio = 18
            self.vida_max = 50 + (onda * 12)
            self.velocidade = 2.4 + (onda * 0.08)
            self.dano = 15
            self.cor = VERMELHO_ALERTA
            self.recompensa = 10

        # --- NOVOS CHEFOES (A CADA 5 ONDAS) ---
        elif tipo == "boss_omen":
            self.nome = "OMEN: O CONTROLADOR DAS SOMBRAS"
            self.raio = 45
            self.vida_max = 900 + (onda * 120)
            self.velocidade = 2.2
            self.dano = 30
            self.cor = CLOVE_ROXO
            self.recompensa = 200
        elif tipo == "boss_reyna":
            self.nome = "REYNA: A IMPERATRIZ VAMPIRICA"
            self.raio = 45
            self.vida_max = 1300 + (onda * 150)
            self.velocidade = 2.8
            self.dano = 35
            self.cor = CLOVE_ROSA
            self.recompensa = 300
        elif tipo == "boss_spike":
            self.nome = "SPIKE NUCLEAR INSTAVEL"
            self.raio = 50
            self.vida_max = 1800 + (onda * 200)
            self.velocidade = 1.5
            self.dano = 45
            self.cor = VERMELHO_ALERTA
            self.recompensa = 450

        self.vida = self.vida_max

    def mover(self, player, smokes, projeteis_inimigos):
        fator_lentidao = 1.0
        for smoke in smokes:
            if math.hypot(self.x - smoke.x, self.y - smoke.y) < smoke.raio:
                fator_lentidao = 0.4
                break

        angulo = math.atan2(player.y - self.y, player.x - self.x)
        self.x += math.cos(angulo) * self.velocidade * fator_lentidao
        self.y += math.sin(angulo) * self.velocidade * fator_lentidao

        # --- HABILIDADES ESPECIAIS DOS CHEFOES ---
        if self.eh_boss:
            self.timer_habilidade -= 1
            if self.timer_habilidade <= 0:
                # Boss 1 (Omen): Teleporta para perto da Clove e dispara 3 tiros
                if self.tipo == "boss_omen":
                    ang_tp = random.uniform(0, math.pi * 2)
                    self.x = max(60, min(LARGURA - 60, player.x + math.cos(ang_tp) * 240))
                    self.y = max(60, min(ALTURA - 60, player.y + math.sin(ang_tp) * 240))
                    for desvio in [-0.25, 0, 0.25]:
                        ang_tiro = math.atan2(player.y - self.y, player.x - self.x) + desvio
                        alvo_x = self.x + math.cos(ang_tiro) * 100
                        alvo_y = self.y + math.sin(ang_tiro) * 100
                        projeteis_inimigos.append(ProjetilInimigo(self.x, self.y, alvo_x, alvo_y, 18, 7, CLOVE_ROXO))
                    self.timer_habilidade = 150

                # Boss 2 (Reyna): Atira rajada rapida de orbes e se cura um pouco
                elif self.tipo == "boss_reyna":
                    self.vida = min(self.vida_max, self.vida + 60)
                    for i in range(6):
                        ang_tiro = (math.pi * 2 / 6) * i
                        alvo_x = self.x + math.cos(ang_tiro) * 100
                        alvo_y = self.y + math.sin(ang_tiro) * 100
                        projeteis_inimigos.append(ProjetilInimigo(self.x, self.y, alvo_x, alvo_y, 20, 6, CLOVE_ROSA))
                    self.timer_habilidade = 110

                # Boss 3 (Spike): Explode uma onda circular de 12 projeteis
                elif self.tipo == "boss_spike":
                    for i in range(12):
                        ang_tiro = (math.pi * 2 / 12) * i
                        alvo_x = self.x + math.cos(ang_tiro) * 100
                        alvo_y = self.y + math.sin(ang_tiro) * 100
                        projeteis_inimigos.append(ProjetilInimigo(self.x, self.y, alvo_x, alvo_y, 22, 5, VERMELHO_ALERTA))
                    self.timer_habilidade = 130

    def desenhar(self, tela):
        if self.tipo in SPRITES:
            img = SPRITES[self.tipo]
        elif self.tipo == "tanque":
            img = SPRITES["lag"]
        else:
            img = SPRITES["bot"]
            if self.tipo == "rush":
                img = img.copy()
                img.fill(CLOVE_CIANO, special_flags=pygame.BLEND_MULT)

        rect = img.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(img, rect)

        # Barra de vida normal (para inimigos comuns)
        if not self.eh_boss and self.vida < self.vida_max:
            largura_barra = self.raio * 2
            pct_vida = max(0, self.vida / self.vida_max)
            pygame.draw.rect(tela, (50, 50, 50), (self.x - self.raio, self.y - self.raio - 14, largura_barra, 5))
            pygame.draw.rect(tela, VERDE_VIDA, (self.x - self.raio, self.y - self.raio - 14, largura_barra * pct_vida, 5))
