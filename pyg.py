#!/usr/bin/python3
import pygame
import glob
import os
import sys
import subprocess
from config import *
from PIL import Image

pygame.init()


background_color = "black"

# Task to do simple draw app (which will draw by lines)
# Todo
# 	Change background color on click or on push the button 'e' + 
# 	Add change color that draw +
#	Add keep the same main game after menu launch +
#	Add change size of the brush +
# 	Add Screenshot save
# 	Add Gif save
	

class Game_Events:

	def text_object(self, msg, font):
		text_surface = font.render(msg, True, WHITE)
		return text_surface, text_surface.get_rect()

	def button(self, window, msg,pos, size, colors, action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if (pos[0]+size[0] > mouse[0] > pos[0] and pos[1]+size[1] > mouse[1] > pos[1]):
			pygame.draw.rect(window, colors[1], (pos[0], pos[1], size[0],size[1]))
			if (click[0] == 1 and action != None):
				action()
		else:
			pygame.draw.rect(window, colors[0], (pos[0], pos[1], size[0],size[1]))

		text = pygame.font.SysFont("Arial", 20)
		text_surface, text_rect = self.text_object(msg, text)	
		text_rect.center = ( (pos[0]+(size[0]/2), (pos[1]+(size[1]/2) )))
		window.blit(text_surface, text_rect)

	def button_change_color(self,win,msg,pos,size,color,action=None):
		global current_color
		color = current_color
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		pygame.draw.rect(win, color, ((pos[0],pos[1]), (size[0],size[1])))
		if (pos[0]+size[0] > mouse[0] > pos[0] and pos[1]+size[1]>mouse[1]>pos[1]):
			if (click[0] == 1 and action != None):
				action()

		font_text = pygame.font.SysFont("Arial", 30)
		text_surface, text_rect = self.text_object("Color", font_text)
		text_rect.center = ((pos[0]+(size[0]/2)), (pos[1]+(size[1]/2)))
		win.blit(text_surface, text_rect)

	def size_surface(self, win, txt, pos, size, color):
		pygame.draw.rect(win, color, (pos[0], pos[1], size[0],size[1]))
		font_text = pygame.font.SysFont("Arial", 30)
		text_surface, text_rect = self.text_object(txt, font_text)
		text_rect.center = ((pos[0]+(size[0]/2)), (pos[1]+(size[1]/2)))
		win.blit(text_surface, text_rect)

class Game_States:

	game_events = Game_Events()

	def __init__(self, window):
		self.window = window

	def pause_state(self, surface):
		global brush_size
		pause = True
		clock = pygame.time.Clock()
		while (pause):
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pause = False
					break

				keys = pygame.key.get_pressed()

				self.game_events.button(self.window,"+",(WIDTH/2-100,HEIGHT/2-200),(50,50),(PURPLE, DARK_PURPLE), self.increment)
				self.game_events.size_surface(self.window,str(brush_size),(WIDTH/2-200,HEIGHT/2-200),(50,50),ORANGE)
				self.game_events.button(self.window,"-",(WIDTH/2-300,HEIGHT/2-200),(50, 50),(DARK_GREEN,GREEN), self.decrement)

				self.game_events.button_change_color(self.window, "Click", (WIDTH/2, HEIGHT/2), (100,100), (DARK_RED), self.change_color)
				if (keys[pygame.K_w]):
					# if (background_color == "black"):
					# 	self.window.fill(BLACK)
					# if (background_color == "white"):
					# 	self.window.fill(WHITE)
					self.window.blit(surface, (0,0))
					pause = False	
					

			clock.tick(30)
			pygame.display.update()
	
	def increment(self):
		global brush_size
		brush_size += 1

	def decrement(self):
		global brush_size
		if (brush_size <= 1):
			brush_size = 1
		else:
			brush_size -= 1

	def change_color(self):
		global current_color, count
		if (count == len(COLORS)-1):
			count = 0
			current_color = COLORS[count]
		else:
			count += 1
			current_color = COLORS[count]
	
def do_screenshot(win, count):
	if (count < 10):
		pygame.image.save(win, f"screenshot0{count}.png")
	else:
		pygame.image.save(win, f"screenshot{count}.png")

def make_gif():
	frames = []
	images = glob.glob("*.png")

	for frame in images:
		new_frame = Image.open(frame)
		frames.append(new_frame)

	frames[0].save("animated.gif", format="GIF",
					append_images=frames[1:],
					save_all=True,
					duration=500,loop=0)

	if (sys.platform == "win32"):
		os.startfile('animated.gif')
	else:
		opener = "open" if sys.platform == "darwin" else "xdg-open"
		subprocess.call([opener, "animated.gif"])

def drawing(window, brushs):
	global current_color
	click = pygame.mouse.get_pressed()
	mouse = pygame.mouse.get_pos()
	
	if (click[0] == 1):
		pygame.draw.rect(window, current_color, ((int(mouse[0])-brushs, int(mouse[1])-brushs), (brushs,brushs)))

def main():
	global brush_size, current_color, count
	window = pygame.display.set_mode(SCREEN_SIZE)

	brush_size = 10
	current_color = WHITE
	count = 0
	c = 0

	game_states = Game_States(window)
	game_events = Game_Events()
	play = True

	clock = pygame.time.Clock()
	while (play):

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				play = False
				break

		keys = pygame.key.get_pressed()

		#Pause the game
		if (keys[pygame.K_q]):
			new_surface = window.copy()
			game_states.pause_state(new_surface)

		#Change colors
		if (keys[pygame.K_e]):
			window.fill(WHITE)
			background_color = "white"
		
		if (keys[pygame.K_r]):
			window.fill(BLACK)
			background_color = "black"

		if (keys[pygame.K_c]):
			window.fill(BLACK)

		#Make a screenshot
		if (keys[pygame.K_s]):
			do_screenshot(window, c)
			c += 1

		#Save to the gif
		if (keys[pygame.K_g]):
			make_gif()

		

		drawing(window, brush_size)
	
		clock.tick(30)
		pygame.display.update()

	pygame.quit()
if __name__ == '__main__':
	main()