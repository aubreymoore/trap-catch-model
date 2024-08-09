import pygame
import random
from icecream import ic
from PIL import Image
import numpy as np

WIDTH = 500
HEIGHT = 500
Y_WINDSPEED = 1.0
X_WINDSPEED = 0.0
NATURAL_SOURCE_COUNT = 0
FPS = 40
MAX_FRAMES = 500 # max frames for GIF recording

# game variables
source_list = []
particle_list = []

class Source:

    def __init__(self, x_pos, y_pos, release_rate, radius, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.release_rate = 1
        self.radius = radius
        self.color = color

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def release_particles(self):
        particle_list.append(Particle(self.x_pos, self.y_pos, 2, 'white', 1, 0.02))

class Particle:

    def __init__(self, x_pos, y_pos, radius, color, id, circle):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.id = id
        self.circle = ''

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def update_pos(self):
        y_dispersal = random.normalvariate(0.0, 1.5)
        x_dispersal = random.normalvariate(0.0, 1.5)
        self.y_pos += Y_WINDSPEED + y_dispersal
        self.x_pos += X_WINDSPEED + x_dispersal

"""
PygameRecord - A utility for recording Pygame screens as GIFS.

This module provides a class, PygameRecord, which can be used to record Pygame
animations and save them as GIF files. It captures frames from the Pygame display
and saves them as images, then combines them into a GIF file.

Credits:
- Author: Ricardo Ribeiro Rodrigues
- Date: 21/03/2024
- source: https://gist.github.com/RicardoRibeiroRodrigues/9c40f36909112950860a410a565de667

Usage:
1. Initialize PygameRecord with a filename and desired frames per second (fps).
2. Enter a Pygame event loop.
3. Add frames to the recorder at desired intervals.
4. When done recording, exit the Pygame event loop.
5. The recorded GIF will be saved automatically.
"""
class PygameRecord:
    def __init__(self, filename: str, fps: int):
        self.fps = fps
        self.filename = filename
        self.frames = []

    def add_frame(self):
        curr_surface = pygame.display.get_surface()
        x3 = pygame.surfarray.array3d(curr_surface)
        x3 = np.moveaxis(x3, 0, 1)
        array = Image.fromarray(np.uint8(x3))
        self.frames.append(array)

    def save(self):
        self.frames[0].save(
            self.filename,
            save_all=True,
            optimize=False,
            append_images=self.frames[1:],
            loop=0,
            duration=int(1000 / self.fps),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred: {exc_value}")
        self.save()
        # Return False if you want exceptions to propagate, True to suppress them
        return False

# MAIN 
######  

if __name__ == "__main__":

    # Create sources
    source_list.append(Source(WIDTH/2, HEIGHT/2, 1, 10, 'red')) 
    # source_list.append(Source(WIDTH/4, HEIGHT/2, 1, 10, 'green')) 
    # source_list.append(Source(3*WIDTH/4, HEIGHT/2, 1, 10, 'green')) 
    for i in range(NATURAL_SOURCE_COUNT):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        source_list.append(Source(x, y, 1, 10, 'green')) 

    with PygameRecord("output.gif", FPS) as recorder:
        pygame.init()
        screen = pygame.display.set_mode([WIDTH, HEIGHT])
        running = True
        clock = pygame.time.Clock()
        n_frames = MAX_FRAMES
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))


            # pygame.draw.circle(
            #     screen,
            #     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            #     (200, 200),
            #     50,
            # )

            # draw sources an release particles
            for source in source_list:
                source.draw()
                source.release_particles()

            # move particles and draw them
            ic(len(particle_list))
            for particle in particle_list:
                particle.update_pos()
                particle.draw()

            # Remove particles from list if they are outside the view frame
            for particle in particle_list:
                if particle.y_pos > HEIGHT:
                    particle_list.remove(particle)  

            # Add frame to recorder
            recorder.add_frame()

            pygame.display.flip()
            clock.tick(FPS)

            # Used here to limit the size of the GIF, not necessary for normal usage.
            n_frames -= 1
            if n_frames == 0:
                break
        recorder.save()
    pygame.quit()
