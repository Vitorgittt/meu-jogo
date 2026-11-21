import pygame
import os
import math
import array

class GerenciadorAudio:
    def __init__(self):
        self.mutado = False
        self.sons = {}
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.ativo = True
        except:
            self.ativo = False
            return

        # Gera os efeitos sonoros sintetizados automaticamente
        self.sons["tiro"] = self._gerar_onda(freq_inicio=700, freq_fim=250, duracao=0.08, volume=0.15)
        self.sons["smoke"] = self._gerar_onda(freq_inicio=180, freq_fim=350, duracao=0.35, volume=0.25)
        self.sons["vitalidade"] = self._gerar_onda(freq_inicio=300, freq_fim=850, duracao=0.25, volume=0.25)
        self.sons["explosao"] = self._gerar_onda(freq_inicio=140, freq_fim=40, duracao=0.22, volume=0.3)
        self.sons["ult"] = self._gerar_onda(freq_inicio=250, freq_fim=1100, duracao=0.75, volume=0.4)
        self.sons["compra"] = self._gerar_onda(freq_inicio=500, freq_fim=900, duracao=0.15, volume=0.25)

    def _gerar_onda(self, freq_inicio, freq_fim, duracao, volume=0.2):
        """Cria um efeito sonoro retro/neon direto na memoria."""
        sample_rate = 22050
        n_samples = int(sample_rate * duracao)
        buf = array.array('h')
        
        for i in range(n_samples):
            progresso = i / n_samples
            freq_atual = freq_inicio + (freq_fim - freq_inicio) * progresso
            envelope = 1.0 - progresso # Diminui o volume suavemente no final
            valor = int(32767 * volume * envelope * math.sin(2.0 * math.pi * freq_atual * i / sample_rate))
            buf.append(valor)
            
        return pygame.mixer.Sound(buffer=buf)

    def tocar_efeito(self, nome):
        if self.ativo and not self.mutado and nome in self.sons:
            self.sons[nome].play()

    def iniciar_musica(self):
        """Toca 'assets/musica.mp3' em loop se o arquivo existir."""
        if not self.ativo:
            return
        caminho_musica = os.path.join("assets", "musica.mp3")
        if os.path.exists(caminho_musica):
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.35) # Volume equilibrado para nao abafar os tiros
            pygame.mixer.music.play(-1) # -1 faz repetir infinitamente

    def alternar_mudo(self):
        if not self.ativo:
            return
        self.mutado = not self.mutado
        if self.mutado:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()