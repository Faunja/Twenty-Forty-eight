# twentyfourtyeight.py
# By Kayden Campbell
# Copyright 2024
# Licensed under the terms of the GPL 3
# If pygame is not installed: sudo apt install python3-pygame
# To run: python3 ./twentyfourtyeight.py
import pygame, random
from copy import deepcopy
pygame.init()
DISPLAYSURF = pygame.display.get_desktop_sizes()
SCREEN_WIDTH, SCREEN_HEIGHT = DISPLAYSURF[0]
grid_height = 4
SCREEN_HEIGHT = round(SCREEN_HEIGHT*3/4/grid_height)*grid_height
cell_size = round(SCREEN_HEIGHT/grid_height)
Line_Offset = SCREEN_HEIGHT*(grid_height-1)/(grid_height*100)
screen = pygame.display.set_mode((SCREEN_HEIGHT+Line_Offset, SCREEN_HEIGHT+Line_Offset+SCREEN_HEIGHT/8))
grid = []
def set_grid():
	if len(grid) != 0:
		grid.clear()
	for row in range(grid_height):
		grid.append([0] * grid_height)
	tiles = 0
	while tiles != 2:
		for row in range(grid_height):
			for col in range(grid_height):
				if tiles == 2:
					break
				newtile = random.randint(1, 16)
				if newtile == 1 and grid[row][col] == 0:
					tileweight = random.randint(1, 2)
					grid[row][col] = tileweight
					tiles += 1
			if tiles == 2:
				break
def draw_grid(score, lost, present, future, rate):
	Line = round(SCREEN_HEIGHT*1/(grid_height*100))
	for row in range(grid_height):
		for col in range(grid_height):
			x = col * cell_size + Line * col
			y = row * cell_size + Line * row + round(SCREEN_HEIGHT/8)
			rect = pygame.Rect(x, y, cell_size, cell_size)
			color = grid[row][col]*15
			pygame.draw.rect(screen, (255-grid[row][col]*15, 255-grid[row][col]*15, 255-grid[row][col]*15), rect)
			if grid[row][col] > 17:
				if future <= 2:
					if future == 1:
						pygame.draw.rect(screen, (255, round(255*present/rate-present/rate), 0), rect)
					else:
						pygame.draw.rect(screen, (round(255*(rate-present)/rate-(rate-present)/rate), 255, 0), rect)
				elif future <= 4:
					if future == 3:
						pygame.draw.rect(screen, (0, 255, round(255*present/rate-(present/rate))), rect)
					else:
						pygame.draw.rect(screen, (0, round(255*(rate-present)/rate-((rate-present)/rate)), 255), rect)
				else:
					if future == 5:
						pygame.draw.rect(screen, (round(255*(present/rate)-(present/rate)), 0, 255), rect)
					else:
						pygame.draw.rect(screen, (255, 0, round(255*(rate-present)/rate-((rate-present)/rate))), rect)
			if grid[row][col] != 0:
				font = pygame.font.Font('freesansbold.ttf', cell_size//4)
				if grid[row][col] <= 8:
					text = font.render(str(2**grid[row][col]), True, (0, 0, 0))
				else:
					if grid[row][col] <= 23:
						text = font.render(str(2**grid[row][col]), True, (255, 255, 255))
					else:
						text = font.render('2^'+str(grid[row][col]), True, (255, 255, 255))
				textRect = text.get_rect()
				textRect.center = (x+cell_size/2, y+cell_size/2)
				screen.blit(text, textRect)
	font = pygame.font.Font('freesansbold.ttf', round(SCREEN_HEIGHT/24))
	text = font.render('Score', True, (255, 255, 255))
	textRect = text.get_rect()
	textRect.center = (SCREEN_HEIGHT/2, round(SCREEN_HEIGHT/32))
	screen.blit(text, textRect)
	font = pygame.font.Font('freesansbold.ttf', round(SCREEN_HEIGHT/16))
	text = font.render(str(score), True, (255, 255, 255))
	textRect = text.get_rect()
	textRect.center = (SCREEN_HEIGHT/2, round(SCREEN_HEIGHT/(32/3)))
	screen.blit(text, textRect)
	if lost == True:
		font = pygame.font.Font('freesansbold.ttf', round(SCREEN_HEIGHT/8))
		text = font.render('You Lose!', True, (255, 0, 0), (0, 0, 0))
		textRect = text.get_rect()
		textRect.center = (SCREEN_HEIGHT/2, SCREEN_HEIGHT/2+SCREEN_HEIGHT/8)
		screen.blit(text, textRect)
def update_grid(direction):
	new_score = 0
	if direction == 1:
		for col in range(grid_height):
			for row in range(grid_height):
				if grid[row][col] == 0:
					for minirow in range(row, grid_height):
						if grid[minirow][col] != 0:
							grid[row][col] = grid[minirow][col]
							grid[minirow][col] = 0
							break
				if grid[row][col] != 0 and row != 0:
					if grid[row-1][col] == grid[row][col]:
						grid[row-1][col] += 1
						new_score += 2**grid[row-1][col]
						grid[row][col] = 0
	if direction == 2:
		for row in range(grid_height):
			for col in range(grid_height-1, -1, -1):
				if grid[row][col] == 0:
					for minicol in range(col-1, -1, -1):
						if grid[row][minicol] != 0:
							grid[row][col] = grid[row][minicol]
							grid[row][minicol] = 0
							break
				if grid[row][col] != 0 and col != grid_height-1:
					if grid[row][col] == grid[row][col+1]:
						grid[row][col+1] += 1
						new_score += 2**grid[row][col+1]
						grid[row][col] = 0
	if direction == 3:
		for col in range(grid_height):
			for row in range(grid_height-1, -1, -1):
				if grid[row][col] == 0:
					for minirow in range(row-1, -1, -1):
						if grid[minirow][col] != 0:
							grid[row][col] = grid[minirow][col]
							grid[minirow][col] = 0
							break
				if grid[row][col] != 0 and row != grid_height-1:
					if grid[row+1][col] == grid[row][col]:
						grid[row+1][col] += 1
						new_score += 2**grid[row+1][col]
						grid[row][col] = 0
	if direction == 4:
		for row in range(grid_height):
			for col in range(grid_height):
				if grid[row][col] == 0:
					for minicol in range(col, grid_height):
						if grid[row][minicol] != 0:
							grid[row][col] = grid[row][minicol]
							grid[row][minicol] = 0
							break
				if grid[row][col] != 0 and col != 0:
					if grid[row][col] == grid[row][col-1]:
						grid[row][col-1] += 1
						new_score += 2**grid[row][col-1]
						grid[row][col] = 0
	empty_tiles = 0
	for row in range(grid_height):
		for col in range(grid_height):
			if grid[row][col] == 0:
				empty_tiles += 1
	if empty_tiles > 0:
		tiles = 0
		while tiles != 1:
			for row in range(grid_height):
				for col in range(grid_height):
					if tiles == 1:
						break
					new_tile = random.randint(1, 16)
					if new_tile == 1 and grid[row][col] == 0:
						tile_weight = random.randint(1, 2)
						grid[row][col] = tile_weight
						tiles += 1
				if tiles == 1:
					break
	return new_score
def auto_grid():
	highest_score = [0, 0, 0, 0]
	copy_grid = deepcopy(grid)
	for row in range(grid_height):
		for col in range(grid_height-1, -1, -1):
			if copy_grid[row][col] == 0:
				for minicol in range(col-1, -1, -1):
					if copy_grid[row][minicol] != 0:
						copy_grid[row][col] = copy_grid[row][minicol]
						copy_grid[row][minicol] = 0
						break
			if copy_grid[row][col] != 0 and col != grid_height-1:
				if copy_grid[row][col] == copy_grid[row][col+1]:
					copy_grid[row][col+1] += 1
					highest_score[1] += 2**copy_grid[row][col+1]
					copy_grid[row][col] = 0
	copy_grid.clear()
	copy_grid = deepcopy(grid)
	for col in range(grid_height):
		for row in range(grid_height-1, -1, -1):
			if copy_grid[row][col] == 0:
				for minirow in range(row-1, -1, -1):
					if copy_grid[minirow][col] != 0:
						copy_grid[row][col] = copy_grid[minirow][col]
						copy_grid[minirow][col] = 0
						break
			if copy_grid[row][col] != 0 and row != grid_height-1:
				if copy_grid[row+1][col] == copy_grid[row][col]:
					copy_grid[row+1][col] += 1
					highest_score[2] += 2**copy_grid[row+1][col]
					copy_grid[row][col] = 0
	copy_grid.clear()
	copy_grid = deepcopy(grid)
	for row in range(grid_height):
		for col in range(grid_height):
			if copy_grid[row][col] == 0:
				for minicol in range(col, grid_height):
					if copy_grid[row][minicol] != 0:
						copy_grid[row][col] = copy_grid[row][minicol]
						copy_grid[row][minicol] = 0
						break
			if copy_grid[row][col] != 0 and col != 0:
				if copy_grid[row][col] == copy_grid[row][col-1]:
					copy_grid[row][col-1] += 1
					highest_score[3] += 2**copy_grid[row][col-1]
					copy_grid[row][col] = 0
	highest = [0, random.randint(3, 4)]
	for score in range(len(highest_score)):
		if highest[0] < highest_score[score]:
			highest[0] = highest_score[score]
			highest[1] = score+1
	return highest[1]
def grid_check():
	empty_tiles = 0
	for row in range(grid_height):
		for col in range(grid_height):
			if grid[row][col] == 0:
				empty_tiles += 1
	if empty_tiles == 0:
		copy_grid = deepcopy(grid)
		for col in range(grid_height):
			for row in range(grid_height):
				if copy_grid[row][col] == 0:
					for minirow in range(row, grid_height):
						if copy_grid[minirow][col] != 0:
							copy_grid[row][col] = copy_grid[minirow][col]
							copy_grid[minirow][col] = 0
							break
				if copy_grid[row][col] != 0 and row != 0:
					if copy_grid[row-1][col] == copy_grid[row][col]:
						copy_grid[row-1][col] += 1
						copy_grid[row][col] = 0
		for row in range(grid_height):
			for col in range(grid_height):
				if copy_grid[row][col] == 0:
					empty_tiles += 1
		if empty_tiles == 0:
			for row in range(grid_height):
				for col in range(grid_height-1, -1, -1):
					if copy_grid[row][col] == 0:
						for minicol in range(col-1, -1, -1):
							if copy_grid[row][minicol] != 0:
								copy_grid[row][col] = copy_grid[row][minicol]
								copy_grid[row][minicol] = 0
								break
					if copy_grid[row][col] != 0 and col != grid_height-1:
						if copy_grid[row][col] == copy_grid[row][col+1]:
							copy_grid[row][col+1] += 1
							copy_grid[row][col] = 0
			for row in range(grid_height):
				for col in range(grid_height):
					if copy_grid[row][col] == 0:
						empty_tiles += 1
			if empty_tiles == 0:
				for col in range(grid_height):
					for row in range(grid_height-1, -1, -1):
						if copy_grid[row][col] == 0:
							for minirow in range(row-1, -1, -1):
								if copy_grid[minirow][col] != 0:
									copy_grid[row][col] = copy_grid[minirow][col]
									copy_grid[minirow][col] = 0
									break
						if copy_grid[row][col] != 0 and row != grid_height-1:
							if copy_grid[row+1][col] == copy_grid[row][col]:
								copy_grid[row+1][col] += 1
								copy_grid[row][col] = 0
				for row in range(grid_height):
					for col in range(grid_height):
						if copy_grid[row][col] == 0:
							empty_tiles += 1
				if empty_tiles == 0:
					for row in range(grid_height):
						for col in range(grid_height):
							if copy_grid[row][col] == 0:
								for minicol in range(col, grid_height):
									if copy_grid[row][minicol] != 0:
										copy_grid[row][col] = copy_grid[row][minicol]
										copy_grid[row][minicol] = 0
										break
							if copy_grid[row][col] != 0 and col != 0:
								if copy_grid[row][col] == copy_grid[row][col-1]:
									copy_grid[row][col-1] += 1
									copy_grid[row][col] = 0
					for row in range(grid_height):
						for col in range(grid_height):
							if copy_grid[row][col] == 0:
								empty_tiles += 1
					if empty_tiles == 0:
						return True
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False	
def main():
	FPS = 60
	clock = pygame.time.Clock()
	run = True
	auto = False
	shift = False
	control = False
	score = 0
	lost = False
	reset = False
	
	present = 1
	future = 1
	rate = FPS*2
	set_grid()
	while run:
		clock.tick(FPS)
		if reset == True:
			auto = False
			score = 0
			lost = False
			reset = False
			present = 1
			future = 1
			rate = FPS*2
			set_grid()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
				if event.key == pygame.K_r:
					reset = True
				if event.key == pygame.K_LSHIFT:
					shift = True
				if event.key == pygame.K_LCTRL:
					control = True
				if event.key == pygame.K_SPACE:
					if auto == False and shift == True and control == True:
						auto = True
					else:
						auto = False
				if lost == False:
					if event.key == pygame.K_UP or event.key == pygame.K_w:
						score += update_grid(1)
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						score += update_grid(2)
					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						score += update_grid(3)
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						score += update_grid(4)
					lost = grid_check()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					shift = False
				if event.key == pygame.K_LCTRL:
					control = False
			if event.type == pygame.QUIT:
				run = False
		if auto == True and lost == False:
			for loop in range(60):
				score += update_grid(auto_grid())
				lost = grid_check()
				if lost == True:
					break
		if present >= rate:
			present = 1
			if future == 6:
				future = 1
			else:
				future += 1
		else:
			present += 1
		screen.fill((0, 0, 0))
		draw_grid(score, lost, present, future, rate)
		pygame.display.update()
	pygame.quit()
main()
