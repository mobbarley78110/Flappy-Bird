import pygame
from settings import Settings


class Score:

    def __init__(self, flappy):
        self.screen = flappy.screen
        self.dead = flappy.dead
        self.s = Settings()
        self.h = 60
        self.w = 0
        self.x = 0
        self.y = 0
        self.number = Numbers()

    def draw(self, score, y=50, alpha=255):
        surf = self.number.write(score, alpha)
        self.w = surf.get_width()
        if self.dead == False:
            self.screen.blit(surf, (self.s.w // 2 - self.w // 2, y))

class Bird:

    def __init__(self, flappy):
        self.screen = flappy.screen
        self.s = Settings()
        self.x = 140
        self.y = self.s.h / 2
        self.w = self.s.b_x
        self.h = self.s.b_y
        self.gravity = self.s.g
        self.dy = 0

        # load sprites
        self.sprites = pygame.image.load('images/bird.png')
        self.surf_normal = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surf_flapping = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        self.surf_normal.blit(self.sprites, (0, 0), (0, 0, self.w, self.h))
        self.surf_flapping.blit(self.sprites, (0, 0), (self.w, 0, self.w, self.h))

        # load sound
        # self.sound_flapping = pygame.mixer.Sound('sounds/sfx_wing.wav')

    def draw(self):
        # self.surface.fill((200, 200, 0))
        if self.dy < 0:
            self.screen.blit(self.surf_flapping, (self.x, self.y))
        else:
            self.screen.blit(self.surf_normal, (self.x, self.y))

    def dead(self):
        pass

    def update(self):
        self.dy += self.gravity
        if self.dy > self.s.m:
            self.dy = self.s.m
        self.dy *= self.s.f
        self.y += self.dy
        if self.y > self.s.h - self.s.floor_h - self.s.b_y:
            self.y = self.s.h - self.s.floor_h - self.s.b_y
            self.dy = 0
        if self.y < 0:
            self.y = 0
            self.dy = 0

    def jump(self):
        self.dy += -self.s.j

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.s.b_x, self.s.b_y)


class Pipes:

    def __init__(self, flappy, h, d):
        self.s = Settings()
        self.pipe_sprite = pygame.image.load('images/pipe.png')
        self.head_sprite = pygame.image.load('images/pipe_head.png')
        self.screen = flappy.screen
        self.x = self.s.w + 20
        self.h = h
        self.delta = d

        # create 4 rects for the pipes
        self.rect_t = pygame.Rect(self.x, 0, self.s.pipe_thickness, self.h)
        self.rect_t_head = pygame.Rect(self.x - 6, self.h, self.s.pipe_thickness + 12, self.s.pipe_head_height)
        self.rect_b = pygame.Rect(self.x, self.h + self.delta, self.s.pipe_thickness, self.s.h - self.h - self.delta-self.s.floor_h)
        self.rect_b_head = pygame.Rect(self.x-6, self.h + self.delta - self.s.pipe_head_height, self.s.pipe_thickness + 12, self.s.pipe_head_height)

        # create 4 surfaces
        self.surf_t = pygame.Surface((self.rect_t.w, self.rect_t.h))
        self.surf_t_head = pygame.Surface((self.rect_t_head.w, self.rect_t_head.h))
        self.surf_b = pygame.Surface((self.rect_b.w, self.rect_b.h))
        self.surf_b_head = pygame.Surface((self.rect_b_head.w, self.rect_b_head.h))

        # for the long pipes, iterate sprites as slices
        for i in range(self.rect_t.h):
            self.surf_t.blit(self.pipe_sprite, (0, i))
        for i in range(self.rect_b.h):
            self.surf_b.blit(self.pipe_sprite, (0, i))
        self.surf_t_head.blit(self.head_sprite, (0,0))
        self.surf_b_head.blit(self.head_sprite, (0, 0))

    def draw(self):
        self.screen.blit(self.surf_t, (self.x, self.rect_t.y))
        self.screen.blit(self.surf_b, (self.x, self.rect_b.y))
        self.screen.blit(self.surf_t_head, (self.x-6, self.rect_t_head.y))
        self.screen.blit(self.surf_b_head, (self.x-6, self.rect_b_head.y))

    def update(self, speed):
        self.x += speed
        self.rect_t = pygame.Rect(self.x, 0, self.s.pipe_thickness, self.h)
        self.rect_t_head = pygame.Rect(self.x - 6, self.h, self.s.pipe_thickness + 12, self.s.pipe_head_height)
        self.rect_b = pygame.Rect(self.x, self.h + self.delta, self.s.pipe_thickness, self.s.h - self.h - self.delta - self.s.floor_h)
        self.rect_b_head = pygame.Rect(self.x - 6, self.h + self.delta - self.s.pipe_head_height,
                                       self.s.pipe_thickness + 12, self.s.pipe_head_height)


class Floor:

        def __init__(self, flappy, x):
            self.screen = flappy.screen
            self.s = Settings()
            self.x = x
            self.y = self.s.h - self.s.floor_h
            self.sprite = pygame.image.load('images/floor.png')
            self.surf = pygame.Surface((self.s.floor_w, self.s.floor_h))
            self.surf.blit(self.sprite, (0,0))

        def draw(self):
            self.screen.blit(self.sprite, (self.x, self.y))


class Numbers:

    def __init__(self):
        self.sprite_sheet = pygame.image.load('images/numbers.png')

        self.thickness = [40, 24, 36, 36, 40, 36, 40, 32, 40, 40]
        self.x_pos = [0, 40, 64, 100, 136, 176, 212, 252, 284, 324]

        self.sprites = []

        for i in range(0, len(self.x_pos)):
            self.sprites.append(pygame.Surface((self.thickness[i], 60), pygame.SRCALPHA))
            self.sprites[i].blit(self.sprite_sheet, (0, 0), (self.x_pos[i], 0, self.thickness[i], 60))

    def write(self, number, alpha=255):
        number = str(number)
        # figure out final surface size
        x_size = 0

        for digit in number:
            x_size += self.thickness[int(digit)]
        temp_surface = pygame.Surface((x_size, 60), pygame.SRCALPHA)
        # blit the sprites into the temp surface
        x_pos = 0
        for digit in number:
            temp_surface.blit(self.sprites[int(digit)], (x_pos, 0))
            x_pos += self.thickness[int(digit)]

        return temp_surface
