import sys
import pygame
from objects import Bird
from objects import Score
from objects import Pipes
from objects import Floor
from settings import Settings
import random
from math import sin


class Flappy:

    def __init__(self):
        pygame.init()
        self.s = Settings()
        self.mainClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.s.w, self.s.h))
        self.running = True
        self.dead = False
        self.death_frame = 0
        self.started = False
        self.bird = Bird(self)
        self.delta = self.s.pipe_gap
        self.r = self.random_high()
        self.pipes = []
        self.floors = []
        for i in range(0, 15):
            self.floors.append(Floor(self, i * self.s.floor_w))
        self.score = 0
        self.score_text = Score(self)
        self.frame_counter = 0
        self.can_score = True
        self.score_frame = 0
        self.speed = -self.s.speed
        self.clouds = pygame.image.load('images/clouds.png')
        self.surf_death = pygame.Surface((self.s.w, self.s.h), pygame.SRCALPHA)
        self.surf_death.fill((50, 50, 50, 255))
        self.score_board = pygame.image.load('images/score_board.png').convert_alpha()
        self.restart = pygame.image.load('images/restart.png')

    def run(self):
        while self.running:
            self._check_events()
            self._update_screen()

    def random_high(self):
        return random.randrange(self.s.pipe_min_size, self.s.h - self.s.floor_h - (self.s.pipe_min_size + self.delta))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    if self.dead == False:
                        self.bird.jump()

    def _update_screen(self):
        self.mainClock.tick(60)

        # draw background
        self.screen.fill((95, 205, 228))
        self.screen.blit(self.clouds, (0, self.s.h - self.s.floor_h - 144))

        if self.dead == False:

            # PRE GAME LOOP
            if self.started == False:
                # draw floor
                for floor in self.floors:
                    floor.draw()
                # draw bird
                self.bird.y = 15 * sin(self.frame_counter/10) + (self.s.h - self.s.floor_h) / 2 - 15 / 2
                self.bird.draw()
                # escape this loop if pressing SPACE
                key_down = pygame.key.get_pressed()
                if key_down[pygame.K_SPACE]:
                    self.started = True

            # MAIN GAME LOOP
            if self.started:
                if ~self.can_score:
                    self.score_frame += 1
                if self.score_frame > 1:
                    self.can_score = True
                    self.score_frame = 0

                    # create new pipes
                if self.frame_counter % self.s.spread == 0:
                    self.pipes.append(Pipes(self, self.r, self.delta))
                    # self.delta -= 0.2
                    self.r = self.random_high()

                # draw pipes
                for i in reversed(range(len(self.pipes))):
                    self.pipes[i].update(self.speed)
                    self.pipes[i].draw()

                    # score up
                    if self.bird.x > self.pipes[i].x + 30:
                        if self.can_score:
                            self.score += 1
                            # self.speed -= 0.1
                        self.can_score = False
                        self.score_frame = 0

                    # test death
                    if self.pipes[i].rect_t.colliderect(self.bird.get_rect())\
                            | self.pipes[i].rect_b.colliderect(self.bird.get_rect())\
                            | self.pipes[i].rect_t_head.colliderect(self.bird.get_rect())\
                            | self.pipes[i].rect_b_head.colliderect(self.bird.get_rect()):
                        self.dead = True
                        self.death_frame = self.frame_counter

                    # remove pipes if passed window
                    if self.pipes[i].x < -self.s.pipe_thickness + 10:
                        self.pipes = self.pipes[:i] + self.pipes[i+1:]

                # draw floor
                for i in reversed(range(0, len(self.floors))):
                    self.floors[i].draw()
                    self.floors[i].x += self.speed
                    if self.floors[i].x < - self.s.pipe_thickness * 2:
                        self.floors = self.floors[:i] + self.floors[i+1:]
                if self.frame_counter % (self.s.floor_w / self.s.speed) == 0:
                    self.floors.append(Floor(self, self.floors[-1].x + self.s.floor_w))

                # draw bird
                self.bird.update()
                self.bird.draw()

                # draw score
                self.score_text.draw(self.score)

        # DEATH
        if self.dead:

            # still draw all the other objects
            for pipe in self.pipes:
                pipe.draw()
            self.bird.update()
            self.bird.draw()
            for floor in self.floors:
                floor.draw()

            # score board and score go down over 30 frames
            self.screen.blit(self.score_board, (self.s.w // 2 - self.score_board.get_width() // 2, 200))
            self.screen.blit(self.restart, (self.s.w // 2 - self.restart.get_width() // 2, 380))
            self.score_text.draw(self.score, 258)

            # draw the flash of death
            alpha = max(0, 255 - 51 * (self.frame_counter - self.death_frame) // 3)
            self.surf_death.fill((50, 50, 50, alpha))
            self.screen.blit(self.surf_death, (0, 0))

            key_down = pygame.key.get_pressed()
            if self.frame_counter > self.death_frame + 30:
                if key_down[pygame.K_SPACE]:
                    self.__init__()
                    self.bird.dy = 0

        # reset frame counter if too high to avoid crashing
        self.frame_counter += 1

        if self.frame_counter > 60000:
            self.frame_counter = 0

        pygame.display.flip()


if __name__ == '__main__':
    FB = Flappy()
    FB.run()