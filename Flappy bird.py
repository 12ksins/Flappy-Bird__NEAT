
# made by 12ksins


# imports and initilaizations
import pygame
import random
import neat
import os
import winsound
import time


pygame.font.init() # font initialization

score = 0 # score
GEN = 0 # GENARATION 
Winh = 700 # window height
Winw = 500 # window Width



sp = input("Enter frame speed per sec in integers or u for unlimited: ") or 30
sp = int(sp) # speed 

Ginp = input("Enter gap between top and bottom pipes in integers :  ") or 275
Ginp = int(Ginp) # 
inp = input("g for playing other for AI :  ") or "g" # pretty self explanatory

# Bird imgs is bird images list
Bird_imgs = [pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
    
# Pipe's image
Pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

# Base's image
Base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

# background image
Bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# fonts 
font = pygame.font.SysFont('MV Boli', 20)
font_go = pygame.font.SysFont('Papyrus', 50) # this isn't used but looks nice so...

# highscore file not encrypted! 
file = open("highscore.txt")
content = file.read() # reading the file
hs = int(content) # its content
file.close() 


def frame():
    # frame control and the speed input var
    clock = pygame.time.Clock()
    global sp
    if sp == "u" or sp == "U":
        pass
    elif sp == "":
        clock.tick(30)
    else:
        clock.tick(int(sp))

# bird class
class Bird():
    # constants
    IMGS = Bird_imgs # Bird_imgs list
    Maxr = 25 # max rotation 
    Rotv = 20 # rotational velocity
    Animtime = 5 # animation time

        # init method
    def __init__(self, x, y): # init
        self.x = x  # x coordinates
        self.y = y # y coordinates
        self.tilt = 0 # tilt 
        self.tickc = 0 # tick counter
        self.vel = 0 # velocity
        self.height = self.y # height
        self.img_count = 0 # to scroll through imgs
        self.img = self.IMGS[0] # image

        # jump
    def jump(self):
        self.vel = -10.5 
        self.tickc = 0
        self.height = self.y

        # moving
    def move(self):
        self.tickc += 1 
        
        # vertical distance var
        d = self.vel*self.tickc + 1.5*self.tickc**2 # physics to do the jump

        if d >= 16:
            d = 16 # making sure you dont jump more than 16

        if d < 0:
            d -= 2 # falling

        self.y += d # the distance added to the coordinates


        # rotation
        if d < 0 or self.y < self.height + 50:
          # tilt if distance is less than 0 ie. falling
            if self.tilt < self.Maxr:
                self.tilt = self.Maxr
        elif self.tilt > -90:
                self.tilt -= self.Rotv

       # drawing function 
    def draw(self, win):
      
      
        self.img_count += 1

            # animation
            # checking wt image we should show based on animtime constant
            # making bird (flappy-bird) wings move for animation
        if self.img_count <= self.Animtime:
            self.img = self.IMGS[0]
        elif self.img_count <= self.Animtime*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.Animtime*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.Animtime*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.Animtime*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        # don't flap if falling
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.Animtime*2


            # rotates img
        rot_img = pygame.transform.rotate(self.img, self.tilt)
        nrect = rot_img.get_rect(
            center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rot_img, nrect.topleft)

    # pixel perfect collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# PIPE class
class Pipe():
    Gap = int(Ginp) # gap between pipes User input
    Vel = 5 # velocity

    def __init__(self, x):
        self.x = x # X - coordinates
        self.height = 0 # height
        
        """
        dude if you're reading this I wont be writing comments i
        forgot the comments because i was dumb and new to 
        this shit, so I wrote the comments above even
        through its been more than 50 days since i programmed
        this, and I am in line 166 and theres like 300 more to go
        , to be honest i don't know what my code does either but 
        it works and that's what its supposed to do i guess
        
        your on your own if you want to read the rest but I 
        advice not to
        """

        self.top = 0 
        self.bottom = 0
        self.PIPE_top = pygame.transform.flip(Pipe_img, False, True)
        self.PIPE_bottom = Pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
            self.height = random.randrange(50, 350)
            self.top = self.height - self.PIPE_top.get_height()
            self.bottom = self.height + self.Gap

    def move(self):
        self.x -= self.Vel

    def draw(self, win):
        win.blit(self.PIPE_top, (self.x, self.top))
        win.blit(self.PIPE_bottom, (self.x, self.bottom))

    def collision(self, bird):
        birdm = bird.get_mask()
        topm = pygame.mask.from_surface(self.PIPE_top)
        bottomm = pygame.mask.from_surface(self.PIPE_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_p = birdm.overlap(bottomm, bottom_offset)
        t_p = birdm.overlap(topm, top_offset)

        if t_p or b_p:
            return  True

        return  False

# base class
class Base():
    Vel = 5
    W = Base_img.get_width()
    IMG = Base_img
    def __init__(self, y)   :
        self.y = y
        
        self.xs = 0
        self.xe = self.W

    def move(self):
        self.xs -= self.Vel
        self.xe -= self.Vel

        if self.xs + self.W < 0:
            self.xs = self.xe + self.W
        if self.xe + self.W < 0:
            self.xe = self.xs + self.W

    def draw(self, win):
        win.blit(self.IMG, (self.xs, self.y))
        win.blit(self.IMG, (self.xe, self.y))


def draw_window(win, birds, pipes, base, score, gen, high_score):
    win.blit(Bg_img, (0, 0))

    for bird in birds:
        bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    text = font.render("SCORE :  " + str(score), 1, (0, 0, 0))
    win.blit(text, (Winw - 10 - text.get_width(), 10))

    text = font.render("GENARATION :  " + str(gen), 1, (0, 0, 0))
    win.blit(text, (10 , 10))

    text = font.render("HIGH SCORE :  " + str(high_score), 1, (0, 0, 0))
    win.blit(text, (10, 60))

    base.draw(win)
    pygame.display.update()


def draw_p_window(win, bird, pipes, base, score, high_score):
    win.blit(Bg_img, (0, 0))

    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    text = font.render("SCORE :  " + str(score), 1, (0, 0, 0))
    win.blit(text, (Winw - 10 - text.get_width(), 10))

    text2 = font.render("HIGH SCORE :  " + str(high_score), 1, (0, 0, 0))
    win.blit(text2, (10 , 10))



    base.draw(win)
    pygame.display.update()


def play():
    global hs
    bird = Bird(230, 350)
    base = Base(630)
    pipes = [Pipe(500)]
    win = pygame.display.set_mode((Winw, Winh))
    pygame.display.set_caption('Flappy bird')
    score = 0

    running = True
    while running:

        frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        Key = pygame.key.get_pressed()
        if Key[pygame.K_UP] or Key[pygame.K_w] or Key[pygame.K_SPACE]:
            bird.jump()


        addp = False
        delp = []

        for pipe in pipes:
            if pipe.collision(bird):
                winsound.PlaySound('sfx_hit.wav', winsound.SND_ASYNC)
                play()

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                addp = True
                winsound.PlaySound('sfx_point.wav', winsound.SND_ASYNC)

            if pipe.x + pipe.PIPE_top.get_width() < 0:
                delp.append(pipe)

            pipe.move()

        if addp:
            score += 1
            pipes.append(Pipe(500))
        for x in delp:
            pipes.remove(x)


        if bird.y + bird.img.get_height() >= 630 or bird.y < 0:
            winsound.PlaySound('sfx_die.wav', winsound.SND_ASYNC)
            play()

        bird.move()
        base.move()

        if hs < score:
            hs = score
            file = open("highscore.txt", "w")
            file.write(str(hs))
            file.close()

        draw_p_window(win, bird, pipes, base, score, hs)


def main(genomes, config):
    global GEN
    global hs
    nets = []
    ge = []
    birds = []
    GEN += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(630)
    pipes = [Pipe(500)]
    win = pygame.display.set_mode((Winw, Winh))
    pygame.display.set_caption('Flappy Bird AI (Neat)')
    clock = pygame.time.Clock()
    score = 0

    Key = pygame.key.get_pressed()

    running = True

    while running:
        frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipeind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_top.get_width():
                pipeind = 1

        else:
            running = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y , abs(bird.y - pipes[pipeind].height), abs(bird.y - pipes[pipeind].bottom)))

            if output[0] > 0.5:
                bird.jump()


        addp = False
        delp = []

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collision(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)


                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    addp = True
                    winsound.PlaySound('sfx_point.wav', winsound.SND_ASYNC)

            if pipe.x + pipe.PIPE_top.get_width() < 0:
               delp.append(pipe)


            pipe.move()

        if addp:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(500))
        for x in delp:
            pipes.remove(x)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 630 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        if score > hs:
            hs = score
        draw_window(win, birds, pipes, base, score, GEN, hs)

def run(config_p):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_p)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 50)

# play or ai
def main2():
    if inp == "g" or inp == 'G':
        play()


    else:
        if __name__ == '__main__':
            ld = os.path.dirname(__file__)
            config_p = os.path.join(ld, 'config-feedforward.txt')
            run(config_p)
main2()