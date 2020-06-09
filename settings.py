class Settings:

    def __init__(self):
        self.h = 620
        self.w = 480

        # floor
        self.floor_w = 48
        self.floor_h = 70

        # bird
        self.b_x = 60  # bird size
        self.b_y = 48
        self.g = 0.85  # gravity
        self.f = 0.95  # frottements
        self.j = 25  # jump
        self.m = 10  # max bird down speed

        # pipes
        self.pipe_min_size = 40  # min pipe height
        self.pipe_thickness = 80  # add 12 for the head, 6 on each size
        self.pipe_head_height = 40
        self.pipe_gap = 260  # 260
        self.speed = 3
        self.spread = 90