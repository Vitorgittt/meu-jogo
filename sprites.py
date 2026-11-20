import pygame
import os
from settings import *

def criar_superficie_pixel(matriz, paleta, escala=3):
    """Converte uma matriz de texto em uma imagem Pixel Art com fundo transparente."""
    altura = len(matriz)
    largura = len(matriz)
    surf = pygame.Surface((largura * escala, altura * escala), pygame.SRCALPHA)
    
    for y, linha in enumerate(matriz):
        for x, char in enumerate(linha):
            if char in paleta:
                pygame.draw.rect(surf, paleta[char], (x * escala, y * escala, escala, escala))
    return surf

def carregar_ou_gerar_sprite(nome_arquivo, tamanho, matriz_fallback, paleta_fallback, escala=3):
    """Tenta carregar uma imagem PNG da pasta 'assets/'. Se nao existir, gera a Pixel Art."""
    caminho = os.path.join("assets", nome_arquivo)
    if os.path.exists(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    return criar_superficie_pixel(matriz_fallback, paleta_fallback, escala)

# ==============================================================================
# MATRIZES DE PIXEL ART (CLOVE, INIMIGOS E CRISTAIS)
# ==============================================================================

# 1. Sprite da Clove (Cabelo curto rosa/roxo, olhos brilhantes, jaqueta escura)
PALETA_CLOVE = {
    'R': CLOVE_ROSA,      # Cabelo Rosa Neon
    'P': CLOVE_ROXO,      # Mechas Roxas / Jaqueta
    'C': CLOVE_CIANO,     # Detalhes Ciano / Olhos
    'S': (255, 224, 189), # Pele
    'D': (30, 30, 45)     # Roupa Escura
}
MATRIZ_CLOVE = [
    "....RRRRRR....",
    "...RRRRRRRR...",
    "..RRPPRRRPRR..",
    "..RPRSSSSPRR..",
    "..RRSCSSCPRR..",
    "...RSSSSSSR...",
    "....PPDDPP....",
    "..PPPPDDPPPP..",
    ".PP.PPCCPP.PP.",
    ".SS.DDDDDD.SS.",
    "....DDDDDD....",
    "....DD..DD....",
    "....PP..PP...."
]

# 2. Bot Inimigo (Robo de treino do Valorant)
PALETA_BOT = {
    'V': VERMELHO_ALERTA,
    'C': (150, 150, 170),
    'E': (40, 40, 50),
    'A': (255, 200, 0)
}
MATRIZ_BOT = [
    ".....VV.....",
    "....CCCC....",
    "...CEAAEC...",
    "...CCCCCC...",
    "....EEEE....",
    "..CCCCCCCC..",
    ".CC.CVVC.CC.",
    ".EE.CCCC.EE.",
    "....EEEE....",
    "....CC.CC..."
]

# 3. Inimigo Tanque (Simbolo de Ping Alto / Wi-Fi Vermelho)
PALETA_LAG = {
    'V': (255, 60, 0),
    'L': (255, 165, 0)
}
MATRIZ_LAG = [
    "...VVVVVV...",
    ".VV......VV.",
    "V..LLLLLL..V",
    "..L......L..",
    "....VVVV....",
    "...V....V...",
    ".....LL.....",
    ".....LL....."
]

# 4. Cristal / Orbe de Essencia
PALETA_ORBE = {
    'R': CLOVE_ROSA,
    'B': BRANCO,
    'P': CLOVE_ROXO
}
MATRIZ_ORBE = [
    "...R...",
    "..RBR..",
    ".RBBBR.",
    "RPBBBRP",
    ".RBBBR.",
    "..RPR..",
    "...P..."
]

# Dicionario global que guarda os sprites prontos
SPRITES = {}

def inicializar_sprites():
    SPRITES["clove"] = carregar_ou_gerar_sprite("clove.png", (48, 48), MATRIZ_CLOVE, PALETA_CLOVE, escala=3)
    SPRITES["bot"] = carregar_ou_gerar_sprite("bot.png", (44, 44), MATRIZ_BOT, PALETA_BOT, escala=3)
    SPRITES["lag"] = carregar_ou_gerar_sprite("lag.png", (56, 56), MATRIZ_LAG, PALETA_LAG, escala=5)
    SPRITES["orbe"] = carregar_ou_gerar_sprite("orbe.png", (24, 24), MATRIZ_ORBE, PALETA_ORBE, escala=3)
