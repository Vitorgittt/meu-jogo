import pygame
import random
import math
from settings import *
from player import Jogadora, Projetil
from enemies import Inimigo, OrbeEssencia, ProjetilInimigo
from particles import Particula, SmokeClove
from sprites import inicializar_sprites
from audio import GerenciadorAudio

pygame.init()

# Configura tela com suporte a Fullscreen
flags = pygame.FULLSCREEN if TELA_CHEIA else 0
tela = pygame.display.set_mode((LARGURA, ALTURA), flags)
pygame.display.set_caption(TITULO)
inicializar_sprites()
relogio = pygame.time.Clock()

# Fontes
fonte_titulo = pygame.font.SysFont("Courier New", 48, bold=True)
fonte_media = pygame.font.SysFont("Courier New", 24, bold=True)
fonte_pequena = pygame.font.SysFont("Courier New", 18)

audio = GerenciadorAudio()
audio.iniciar_musica()

def desenhar_grade(tela):
    tela.fill(PRETO_FUNDO)
    espaco = 50
    for x in range(0, LARGURA, espaco):
        pygame.draw.line(tela, GRADE_COR, (x, 0), (x, ALTURA))
    for y in range(0, ALTURA, espaco):
        pygame.draw.line(tela, GRADE_COR, (0, y), (LARGURA, y))

def criar_explosao(particulas, x, y, cor, qtd=15):
    for _ in range(qtd):
        ang = random.uniform(0, math.pi * 2)
        vel = random.uniform(1.5, 5.5)
        particulas.append(Particula(x, y, cor, random.randint(3, 7), math.cos(ang)*vel, math.sin(ang)*vel, random.randint(20, 40)))

def main():
    global tela
    estado = "MENU" # MENU, JOGANDO, LOJA, GAMEOVER
    tela_cheia_atual = TELA_CHEIA

    player = Jogadora()
    projeteis = []
    inimigos = []
    projeteis_inimigos = []
    orbes = []
    particulas = []
    smokes = []

    onda = 1
    inimigos_para_spawnar = 8
    timer_spawn = 0
    cristais = 0
    abates = 0
    frase_morte = ""

    frases_skill_issue = [
        "SKILL ISSUE DETECTADO! Morreu sem usar a Smoke?",
        "Faltou carregar a Ult da Clove antes de rushar!",
        "Culpa do ping de Brasilia... tenta de novo!",
        "O Matchmaking venceu essa rodada. Revanche?"
    ]

    rodando = True
    while rodando:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # --- EVENTOS DE TECLADO E MOUSE ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                # F11 alterna Tela Cheia a qualquer momento
                if evento.key == pygame.K_F11:
                    tela_cheia_atual = not tela_cheia_atual
                    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN if tela_cheia_atual else 0)

                if estado == "MENU" and evento.key == pygame.K_RETURN:
                    estado = "JOGANDO"

                elif estado == "JOGANDO":
                    # Habilidade Q: Smoke da Clove
                    if evento.key == pygame.K_q and player.cooldown_smoke == 0:
                        smokes.append(SmokeClove(mouse_pos[0], mouse_pos[1]))
                        player.cooldown_smoke = 240 # 4 segundos de recarga
                        criar_explosao(particulas, mouse_pos[0], mouse_pos[1], CLOVE_ROXO, 20)
                        # Dentro do if evento.key == pygame.K_q ...
                        audio.tocar_efeito("smoke")

                    # Habilidade E: Vitalidade (Vida temporaria apos abate)
                    if evento.key == pygame.K_e:
                        if player.usar_vitalidade():
                            criar_explosao(particulas, player.x, player.y, CLOVE_ROSA, 25)
                            # Dentro do if player.usar_vitalidade():
                            audio.tocar_efeito("vitalidade")

                elif estado == "LOJA":
                    if evento.key == pygame.K_1 and cristais >= 50:
                        cristais -= 50
                        player.dano += 8
                    elif evento.key == pygame.K_2 and cristais >= 50:
                        cristais -= 50
                        player.cadencia_tiro = max(6, player.cadencia_tiro - 2)
                    elif evento.key == pygame.K_3 and cristais >= 40:
                        cristais -= 40
                        player.vida_max += 20
                        player.vida = min(player.vida_max, player.vida + 40)
                    elif evento.key == pygame.K_4 and cristais >= 60:
                        cristais -= 60
                        player.velocidade += 0.5
                    elif evento.key == pygame.K_RETURN:
                        onda += 1
                        inimigos_para_spawnar = 8 + (onda * 3)
                        timer_spawn = 10
                        if onda % 5 == 0:
                            chefoes = ["boss_omen", "boss_reyna", "boss_spike"]
                            indice_boss = ((onda // 5) - 1) % len(chefoes)
                            inimigos.append(Inimigo(onda, chefoes[indice_boss]))
                            audio.tocar_efeito("compra")
                        estado = "JOGANDO"


                elif estado == "GAMEOVER" and evento.key == pygame.K_r:
                    player = Jogadora()
                    projeteis.clear()
                    inimigos.clear()
                    orbes.clear()
                    smokes.clear()
                    onda = 1
                    inimigos_para_spawnar = 8
                    cristais = 0
                    abates = 0
                    estado = "JOGANDO"

        # ======================================================================
        # TELA 1: MENU INICIAL
        # ======================================================================
        if estado == "MENU":
            desenhar_grade(tela)
            t1 = fonte_titulo.render("CLOVE PROTOCOL", True, CLOVE_ROSA)
            t2 = fonte_media.render("Sobreviva as ondas e domine a arena!", True, CLOVE_CIANO)
            t3 = fonte_pequena.render("[WASD] Mover  |  [Mouse] Atirar  |  [Q] Smoke  |  [E] Vitalidade (Pos-Abate)", True, BRANCO)
            t4 = fonte_pequena.render("[Passiva] Ultimate 'Ainda Nao Morri' revive voce aos 100%!", True, CLOVE_ROXO)
            t5 = fonte_media.render("Pressione [ENTER] para iniciar (F11: Tela Cheia)", True, OURO_CRISTAL)

            tela.blit(t1, (LARGURA//2 - t1.get_width()//2, ALTURA//2 - 140))
            tela.blit(t2, (LARGURA//2 - t2.get_width()//2, ALTURA//2 - 70))
            tela.blit(t3, (LARGURA//2 - t3.get_width()//2, ALTURA//2 + 10))
            tela.blit(t4, (LARGURA//2 - t4.get_width()//2, ALTURA//2 + 45))
            tela.blit(t5, (LARGURA//2 - t5.get_width()//2, ALTURA//2 + 130))

        # ======================================================================
        # TELA 2: ARENA DE COMBATE (JOGANDO)
        # ======================================================================
        elif estado == "JOGANDO":
            teclas = pygame.key.get_pressed()
            botoes_mouse = pygame.mouse.get_pressed()

            player.mover(teclas)

            if evento.key == pygame.K_m:
                audio.alternar_mudo()


            # Tiro continuo segurando o botao esquerdo do mouse
            if botoes_mouse[0] and player.timer_tiro == 0:
                projeteis.append(Projetil(player.x, player.y, mouse_pos[0], mouse_pos[1], player.dano))
                player.timer_tiro = player.cadencia_tiro
                audio.tocar_efeito("tiro")

            # Spawn progressivo de inimigos na onda
            if inimigos_para_spawnar > 0:
                timer_spawn -= 1
                if timer_spawn <= 0:
                    tipo_sorteado = random.choices(["padrao", "rush", "tanque"], weights=[60, 25, 15])[0]
                    inimigos.append(Inimigo(onda, tipo_sorteado))
                    inimigos_para_spawnar -= 1
                    timer_spawn = max(20, 65 - (onda * 3))

            # Se derrotou todos da onda -> Abre a Loja
            if inimigos_para_spawnar == 0 and len(inimigos) == 0:
                estado = "LOJA"

            # Atualiza Smokes
            for s in smokes[:]:
                s.atualizar()
                if s.duracao <= 0:
                    smokes.remove(s)

            # Atualiza Projeteis e Colisoes
            for p in projeteis[:]:
                p.atualizar()
                if p.x < 0 or p.x > LARGURA or p.y < 0 or p.y > ALTURA:
                    projeteis.remove(p)
                    continue

                for ini in inimigos[:]:
                    if math.hypot(p.x - ini.x, p.y - ini.y) < p.raio + ini.raio:
                        ini.vida -= p.dano
                        criar_explosao(particulas, p.x, p.y, CLOVE_CIANO, 5)
                        if p in projeteis:
                            projeteis.remove(p)
                        if ini.vida <= 0:
                            abates += 1
                            player.registrar_abate() # Libera habilidade E (Vitalidade)
                            orbes.append(OrbeEssencia(ini.x, ini.y, ini.recompensa))
                            criar_explosao(particulas, ini.x, ini.y, ini.cor, 20)
                            inimigos.remove(ini)
                        break

            # Atualiza Inimigos e Dano na Jogadora
            for ini in inimigos[:]:
                ini.mover(player, smokes, projeteis_inimigos)
                if math.hypot(player.x - ini.x, player.y - ini.y) < player.raio + ini.raio:
                    player.receber_dano(ini.dano)
                    criar_explosao(particulas, player.x, player.y, VERMELHO_ALERTA, 15)
                    if not ini.eh_boss:
                        inimigos.remove(ini)
                    else:
                        ini.x -= (player.x - ini.x) * 1.5
                        ini.y -= (player.y - ini.y) * 1.5

            # Atualiza Projeteis dos Chefoes
            for pi in projeteis_inimigos[:]:
                pi.atualizar()
                if pi.x < 0 or pi.x > LARGURA or pi.y < 0 or pi.y > ALTURA:
                    projeteis_inimigos.remove(pi)
                    continue
                if math.hypot(player.x - pi.x, player.y - pi.y) < player.raio + pi.raio:
                    player.receber_dano(pi.dano)
                    criar_explosao(particulas, player.x, player.y, pi.cor, 12)
                    projeteis_inimigos.remove(pi)


                    # CHECA MORTE OU ULTIMATE DA CLOVE ("AINDA NAO MORRI!")
                    if player.vida <= 0:
                        audio.tocar_efeito("explosao")
                        if player.ult_carga >= 100:
                            player.ult_carga = 0
                            player.vida = int(player.vida_max * 0.75)
                            player.invencivel_timer = 60
                            criar_explosao(particulas, player.x, player.y, CLOVE_ROSA, 60)
                            for outro in inimigos:
                                ang_empurrao = math.atan2(outro.y - player.y, outro.x - player.x)
                                outro.x += math.cos(ang_empurrao) * 180
                                outro.y += math.sin(ang_empurrao) * 180
                                audio.tocar_efeito("ult")                               
                        else:
                            frase_morte = random.choice(frases_skill_issue)
                            estado = "GAMEOVER"

            # Atualiza Orbes de Essencia
            for orbe in orbes[:]:
                orbe.atualizar(player)
                if math.hypot(player.x - orbe.x, player.y - orbe.y) < player.raio + orbe.raio + 5:
                    cristais += orbe.valor_cristal
                    player.ult_carga = min(100, player.ult_carga + 10)
                    orbes.remove(orbe)
                elif orbe.tempo_vida <= 0:
                    orbes.remove(orbe)

            # Atualiza Particulas
            for part in particulas[:]:
                part.atualizar()
                if part.duracao <= 0:
                    particulas.remove(part)

            # --- DESENHO NA TELA ---
            desenhar_grade(tela)
            for s in smokes: s.desenhar(tela)
            for orbe in orbes: orbe.desenhar(tela)
            for part in particulas: part.desenhar(tela)
            for p in projeteis: p.desenhar(tela)
            for ini in inimigos: ini.desenhar(tela)
            player.desenhar(tela, mouse_pos)

            # --- HUD (BARRAS DE VIDA, ULT E HABILIDADES) ---
            pygame.draw.rect(tela, (40, 40, 40), (20, 20, 220, 20))
            pygame.draw.rect(tela, VERDE_VIDA, (20, 20, 220 * max(0, player.vida / player.vida_max), 20))
            if player.vida_temp > 0:
                largura_extra = min(110, 220 * (player.vida_temp / player.vida_max))
                pygame.draw.rect(tela, CLOVE_ROSA, (242, 20, largura_extra, 20))
            
            texto_vida = f"HP: {max(0, player.vida)}/{player.vida_max}" + (f" (+{player.vida_temp})" if player.vida_temp > 0 else "")
            txt_hp = fonte_pequena.render(texto_vida, True, BRANCO)
            tela.blit(txt_hp, (25, 20))

            # Barra da Ultimate
            cor_ult = CLOVE_ROSA if player.ult_carga >= 100 else CLOVE_ROXO
            pygame.draw.rect(tela, (40, 40, 40), (20, 48, 220, 16))
            pygame.draw.rect(tela, cor_ult, (20, 48, 220 * (player.ult_carga / 100), 16))
            status_ult = "ULT PRONTA (AUTO-REVIVE)" if player.ult_carga >= 100 else f"ULT: {player.ult_carga}%"
            txt_ult = fonte_pequena.render(status_ult, True, BRANCO)
            tela.blit(txt_ult, (25, 46))

            # Status das Habilidades Q e E
            q_txt = "Q (Smoke): PRONTA" if player.cooldown_smoke == 0 else f"Q (Smoke): {player.cooldown_smoke//60 + 1}s"
            
            if player.vida_temp > 0:
                e_txt = f"E (Vitalidade): ATIVA ({player.timer_vida_temp//60 + 1}s)"
                cor_e = CLOVE_ROSA
            elif player.janela_absorcao > 0:
                e_txt = f"E (Vitalidade): PRONTA! ({player.janela_absorcao//60 + 1}s)"
                cor_e = VERDE_VIDA
            else:
                e_txt = "E (Vitalidade): Elimine um inimigo"
                cor_e = (120, 120, 120)

            tela.blit(fonte_pequena.render(q_txt, True, CLOVE_ROSA if player.cooldown_smoke == 0 else (120, 120, 120)), (20, ALTURA - 55))
            tela.blit(fonte_pequena.render(e_txt, True, cor_e), (20, ALTURA - 30))

            # Onda e Cristais
            txt_onda = fonte_media.render(f"ONDA {onda}", True, CLOVE_CIANO)
            txt_cristais = fonte_media.render(f"CRISTAIS: {cristais}", True, OURO_CRISTAL)
            tela.blit(txt_onda, (LARGURA - txt_onda.get_width() - 20, 20))
            tela.blit(txt_cristais, (LARGURA - txt_cristais.get_width() - 20, 50))

        # ======================================================================
        # TELA 3: LOJA DE UPGRADES
        # ======================================================================
        elif estado == "LOJA":
            desenhar_grade(tela)
            t1 = fonte_titulo.render(f"ONDA {onda} CONCLUIDA!", True, VERDE_VIDA)
            t2 = fonte_media.render(f"Cristais Disponiveis: {cristais}", True, OURO_CRISTAL)
            
            op1 = fonte_pequena.render("[Tecla 1] +8 Dano dos Orbes (Custo: 50 Cristais)", True, BRANCO)
            op2 = fonte_pequena.render("[Tecla 2] +Velocidade de Tiro (Custo: 50 Cristais)", True, BRANCO)
            op3 = fonte_pequena.render("[Tecla 3] +20 Vida Max & Cura (Custo: 40 Cristais)", True, BRANCO)
            op4 = fonte_pequena.render("[Tecla 4] +Velocidade de Movimento (Custo: 60 Cristais)", True, BRANCO)
            
            t_cont = fonte_media.render("Pressione [ENTER] para iniciar a proxima onda!", True, CLOVE_ROSA)

            tela.blit(t1, (LARGURA//2 - t1.get_width()//2, 100))
            tela.blit(t2, (LARGURA//2 - t2.get_width()//2, 165))
            tela.blit(op1, (LARGURA//2 - op1.get_width()//2, 250))
            tela.blit(op2, (LARGURA//2 - op2.get_width()//2, 295))
            tela.blit(op3, (LARGURA//2 - op3.get_width()//2, 340))
            tela.blit(op4, (LARGURA//2 - op4.get_width()//2, 385))
            tela.blit(t_cont, (LARGURA//2 - t_cont.get_width()//2, 480))

        # ======================================================================
        # TELA 4: GAME OVER
        # ======================================================================
        elif estado == "GAMEOVER":
            desenhar_grade(tela)
            t1 = fonte_titulo.render("ELIMINADA DA RODADA", True, VERMELHO_ALERTA)
            t2 = fonte_media.render(frase_morte, True, CLOVE_ROSA)
            t3 = fonte_pequena.render(f"Onda Alcancada: {onda}  |  Inimigos Eliminados: {abates}", True, BRANCO)
            t4 = fonte_media.render("Pressione [R] para jogar novamente", True, CLOVE_CIANO)

            tela.blit(t1, (LARGURA//2 - t1.get_width()//2, ALTURA//2 - 120))
            tela.blit(t2, (LARGURA//2 - t2.get_width()//2, ALTURA//2 - 40))
            tela.blit(t3, (LARGURA//2 - t3.get_width()//2, ALTURA//2 + 20))
            tela.blit(t4, (LARGURA//2 - t4.get_width()//2, ALTURA//2 + 100))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()