import random
import pygame
import pygame.gfxdraw

# Global Variables
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500

SRC_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
# draw.circle is not anti-aliased and looks rather ugly.
# pygame.draw.circle(ATOM_IMG, (0, 255, 0), (15, 15), 15)
# gfxdraw.aacircle looks a bit better.
# pygame.gfxdraw.aacircle(SRC_IMG, 15, 15, 14, (0, 255, 0))
pygame.gfxdraw.filled_circle(SRC_IMG, 15, 15, 14, (0, 255, 0))

# Object class
class Dot(pygame.sprite.Sprite):
	def __init__(self, color, height, width):
		super().__init__()
		self.image = SRC_IMG
		self.rect = self.image.get_rect(center=(150, 200))

	def moveRight(self, pixels):
		self.rect.x += pixels

	def moveLeft(self, pixels):
		self.rect.x -= pixels

	def moveForward(self, pixels):
		self.rect.y += pixels

	def moveBack(self, pixels):
		self.rect.y -= pixels


pygame.init()


RED = (255, 0, 0)


size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")


all_sprites_list = pygame.sprite.Group()

src = Dot(RED, 20, 30)

all_sprites_list.add(src)

exit = True
clock = pygame.time.Clock()

while exit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				exit = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		src.moveLeft(1)
	if keys[pygame.K_RIGHT]:
		src.moveRight(1)
	if keys[pygame.K_DOWN]:
		src.moveForward(1)
	if keys[pygame.K_UP]:
		src.moveBack(1)

	all_sprites_list.update()
	screen.fill(SURFACE_COLOR)
	all_sprites_list.draw(screen)
	pygame.display.flip()
	clock.tick(60)

pygame.quit()
