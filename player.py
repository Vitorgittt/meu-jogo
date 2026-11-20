import pygame
import math
from settings import *
from sprites import SPRITES

class Projetil:
    def __init__(self, x, y, alvo_x, alvo_y, dano, velocidade=12, cor=CLOVE_CIANO):
        self.x = x
        self.y = y
        self.dano = dano
        self.cor = cor
        self.raio = 6
        angulo = math.atan2(alvo_y - y, alvo_x - x)
        self.vel_x = math.cos(angulo) * velocidade
        self.vel_y = math.sin(angulo) * velocidade

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), self.raio // 2)

class Jogadora:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.raio = 18
        
        self.vida_max = 100
        self.vida = self.vida_max
        self.vida_temp = 0
        self.timer_vida_temp = 0
        
        self.velocidade = 5.0
        self.dano = 25
        self.cadencia_tiro = 18
        
        self.timer_tiro = 0
        self.cooldown_smoke = 0
        self.janela_absorcao = 0
        self.ult_carga = 0
        self.invencivel_timer = 0

    def registrar_abate(self):
        self.janela_absorcao = 240

    def usar_vitalidade(self):
        if self.janela_absorcao > 0:
            self.janela_absorcao = 0
            self.vida_temp = 50
            self.timer_vida_temp = 480
            return True
        return False

    def receber_dano(self, dano):
        if self.invencivel_timer > 0:
            return

        if self.vida_temp > 0:
            if dano <= self.vida_temp:
                self.vida_temp -= dano
                return
            else:
                sobra_dano = dano - self.vida_temp
                self.vida_temp = 0
                self.vida -= sobra_dano
        else:
            self.vida -= dano

    def mover(self, teclas):
        dx, dy = 0, 0
        if teclas[pygame.K_w] or teclas[pygame.K_UP]: dy -= 1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]: dy += 1
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: dx -= 1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: dx += 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        mult_vel = 1.35 if self.timer_vida_temp > 0 else 1.0
        self.x += dx * self.velocidade * mult_vel
        self.y += dy * self.velocidade * mult_vel

        self.x = max(self.raio, min(LARGURA - self.raio, self.x))
        self.y = max(self.raio, min(ALTURA - self.raio, self.y))

        if self.timer_tiro > 0: self.timer_tiro -= 1
        if self.cooldown_smoke > 0: self.cooldown_smoke -= 1
        if self.janela_absorcao > 0: self.janela_absorcao -= 1
        if self.invencivel_timer > 0: self.invencivel_timer -= 1

        if self.timer_vida_temp > 0:
            self.timer_vida_temp -= 1
            if self.timer_vida_temp == 0:
                self.vida_temp = 0

    def desenhar(self, tela, mouse_pos):
        mx, my = mouse_pos

        if self.ult_carga >= 100:
            pygame.draw.circle(tela, CLOVE_ROSA, (int(self.x), int(self.y)), self.raio + 12, 2)
        
        if self.vida_temp > 0:
            pygame.draw.circle(tela, CLOVE_ROSA, (int(self.x), int(self.y)), self.raio + 8, 3)

        sprite_clove = SPRITES["clove"]
        if mx < self.x:
            sprite_clove = pygame.transform.flip(sprite_clove, True, False)
        
        rect = sprite_clove.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(sprite_clove, rect)

        angulo = math.atan2(my - self.y, mx - self.x)
        mira_x = self.x + math.cos(angulo) * (self.raio + 14)
        mira_y = self.y + math.sin(angulo) * (self.raio + 14)
        pygame.draw.circle(tela, CLOVE_CIANO, (int(mira_x), int(mira_y)), 5)