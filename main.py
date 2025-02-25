# main.py
import pygame
import sys
import os  # Necessário para SDL_VIDEO_CENTERED

from config import (
    FONT_PATH, BACKGROUND_MUSIC, CLICK_SOUND_PATH,
    BASE_WIDTH, BASE_HEIGHT
)
from states.menu_state import MenuState
from states.opcoes_state import OpcoesState
from states.gameplay_state import GameplayState

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Resolução inicial da janela
        self.largura = 1920
        self.altura = 1080
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Munchkin")

        self.clock = pygame.time.Clock()
        self.running = True

        # Estado do jogo (pode ser MENU, OPCOES, JOGAR, SAIR)
        self.estado = "MENU"

        # Volume do jogo (0..100)
        self.volume = 50
        pygame.mixer.music.set_volume(self.volume / 100.0)

        # ====== SURFACE BASE (lógica 1280x720) ======
        self.base_width = BASE_WIDTH   # Ex: 1280
        self.base_height = BASE_HEIGHT # Ex: 720
        self.base_surface = pygame.Surface((self.base_width, self.base_height))

        # Fonte
        self.fonte = pygame.font.Font(FONT_PATH, 40)

        # Música e sons
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play(-1)  # Loop infinito

        self.click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)
        self.click_sound.set_volume(self.volume / 100.0)

        # Instancia estados
        self.menu_state = MenuState(self)
        self.opcoes_state = OpcoesState(self)
        self.gameplay_state = GameplayState(self)

    def apply_changes(self, resolution, volume):
        """
        Ajusta a resolução real da janela e o volume do jogo.
        Se a nova resolução for menor que a atual, a janela é centralizada.
        """
        w, h = resolution

        # Centraliza a janela se for menor que a anterior
        if (w < self.largura) or (h < self.altura):
            os.environ["SDL_VIDEO_CENTERED"] = "1"
        else:
            if "SDL_VIDEO_CENTERED" in os.environ:
                del os.environ["SDL_VIDEO_CENTERED"]

        # Ajusta a resolução real
        self.largura, self.altura = w, h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Munchkin")

        # Ajusta o volume
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume / 100.0)
        self.click_sound.set_volume(self.volume / 100.0)

        print(f"Nova resolução: {w}x{h} | Volume: {volume}")

    def run(self):
        """
        Loop principal do jogo. 
        Redireciona os eventos, update e draw para o estado atual
        (MENU, OPCOES, JOGAR, SAIR).
        """
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time em segundos
            events = pygame.event.get()

            if self.estado == "MENU":
                self.menu_state.handle_events(events)
                self.menu_state.update(dt)
                self.menu_state.draw()

            elif self.estado == "OPCOES":
                self.opcoes_state.handle_events(events)
                self.opcoes_state.update(dt)
                self.opcoes_state.draw()

            elif self.estado == "JOGAR":
                self.gameplay_state.handle_events(events)
                self.gameplay_state.update(dt)
                self.gameplay_state.draw()

            elif self.estado == "SAIR":
                self.running = False

            # Escalonar a base_surface para a janela atual
            scaled_surf = pygame.transform.scale(self.base_surface, (self.largura, self.altura))
            self.screen.blit(scaled_surf, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
