import constants as c
import pygame
import sys
from sound_manager import SoundManager
from camera import Camera




class Game():
    def __init__(self):
        pygame.init()
        if c.FULLSCREEN:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE, flags = pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE)

        self.clock = pygame.time.Clock()
        self.crosshair = pygame.image.load("assets/images/crosshair.png")
        pygame.mouse.set_visible(False)
        Camera.init()
        SoundManager.init()
        self.main_music_started = False
        self.intro_music = pygame.mixer.Sound("")
        self.intro_music.set_volume(0.3)
        self.intro_music.play(-1)
        self.menu = False
        pygame.mixer.set_num_channels(32)


    def main(self):
        pass



    def get_events(self):
        dt = self.clock.tick(c.FRAMERATE)/1000


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame,quit()
                sys.exit()


        return dt, events


if __name__ =="__main__":
    game = Game()
    game.main()




