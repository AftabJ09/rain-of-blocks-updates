import os
import sys
import pygame, sys
from pygame.locals import *
import random
import json
import os

def resources_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path,relative_path)

pygame.mixer.init()
pygame.init()


Display_windows = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Rain Of Blocks')
myfont = pygame.font.SysFont(None, 25,'#ffffff')
myfont1 = pygame.font.SysFont('Segoe UI',15,'#ffffff',italic=True)


intro_image = pygame.image.load(resources_path('assets/intro_image.jpg'))
intro_image = pygame.transform.scale(intro_image, (180,360))
heart_img = pygame.image.load(resources_path('assets/heart.png'))
heart_img = pygame.transform.scale(heart_img, (20, 20))
icon = pygame.image.load('assets/game_icon.png')
pygame.display.set_icon(icon)


pygame.mixer.music.load(resources_path('assets/intro_music.mp3'))
pop_sound = pygame.mixer.Sound(resources_path('assets/box_collison_sound.wav'))
warning = pygame.mixer.Sound(resources_path('assets/warning.mp3'))


file_path = resources_path("config/person_data.json")
tile_position = 20
tile_width = 50
object_position = 20
object_postiton_x = random.randint(0, 270)
drop_delay = 300
last_drop_time = pygame.time.get_ticks()
score = 0
lives = 5
INDEX = 0
level = 0



current_screen = "menu"
button_rect = pygame.Rect(50, 150, 200, 60)
def load_player_data():
    if os.path.exists(file_path):
        with open(file_path,'r') as f:
            return json.load(f)
    else:
        return {'score':0, "level": 1,"matches_played":0,"time_spent":0}
def save_player_data(data):
    with open(file_path,'w') as f:
        json.dump(data,f,indent=3)

def draw_menu():
    pygame.mixer.music.play(-1)
    Display_windows.fill('black')
    pygame.draw.rect(Display_windows, 'green', button_rect)
    text = myfont.render("Start Game", True, 'white')
    Display_windows.blit(intro_image, (300, 20))
    Display_windows.blit(text, (button_rect.x + 40, button_rect.y + 20))


def draw_game(current_data):
    global object_position, object_postiton_x, INDEX, score, lives, last_drop_time, drop_delay, tile_position,level,pop_sound,game_guide ,current_screen
    player_data = current_data
    Display_windows.fill('#0f0f0f')


    for i in range(lives):
        Display_windows.blit(heart_img, (190 + i * 22, 10))
    level = score // 100 + 1
    if player_data['score'] < score:
        player_data['score'] = score
    if player_data['level'] < level:
        player_data['level'] = level
    label = myfont.render(f'Score:{score} level {level}',1, (255, 255, 255))
    game_guide1 = myfont1.render('PRESS LEFT OR RIGHT KEY  ',1, (255, 255, 255))
    game_guide2 = myfont1.render('< OR > TO MOVE THE TILE',1,(255, 255, 255))
    game_data = myfont.render('PLAYER STATUS',-1,(255,255,255))
    game_data_score = myfont1.render(f'1) Highest Score {player_data['score']}',1,(200,200,200))
    game_data_level = myfont1.render(f'2) Highest level {player_data['level']}',1,(200,200,200))
    game_data_matches_played = myfont1.render(f'3) Matches played {player_data['matches_played']}',1,(200,200,200))
    
    Display_windows.blit(label, (10, 10))
    Display_windows.blit(game_guide1,(310,100))
    Display_windows.blit(game_guide2,(310,120))
    Display_windows.blit(game_data,(330,150))

    
    Display_windows.blit(game_data_score,(340,170))
    Display_windows.blit(game_data_level,(340,190))
    Display_windows.blit(game_data_matches_played,(340,210))

    
    pygame.draw.line(Display_windows, 'white', (300, 0), (300, 400), 3)

    colors = ['BLUE', 'CYAN', 'PURPLE', 'YELLOW', 'ORANGE', 'NAVYBLUE']
    box = pygame.draw.rect(Display_windows, colors[INDEX], (object_postiton_x, object_position, 30, 30))
    tile = pygame.draw.rect(Display_windows, '#00f5d4', (tile_position, 350, tile_width, 5))
    if box.colliderect(tile):
        pop_sound.play()
        INDEX = random.randint(0, 5)
        score += 2
        object_postiton_x = random.randint(0, 270)
        object_position = 20
        if score > 10 and drop_delay > 100:
            drop_delay -= 20
        if score > 100 and drop_delay > 80:
            drop_delay -= 10
    elif object_position > 340:
        warning.play()
        INDEX = random.randint(0, 5)
        score -= 1
        lives -= 1
        object_postiton_x = random.randint(0, 270)
        object_position = 20
    if score < 0:
        score = 0
    current_time = pygame.time.get_ticks()
    if current_time - last_drop_time > drop_delay:
        object_position += 20
        last_drop_time = current_time
    if lives == 0:
        player_data["matches_played"]  += 1
        if player_data['score'] < score:
            player_data['score'] = score
        if player_data['level'] < level:
            player_data['level'] = level
        save_player_data(player_data)
        current_screen = 'menu'
        lives = 5
        score = 0        
        drop_delay = 300 
        object_position = 20
        object_postiton_x = random.randint(0, 270)
    save_player_data(player_data)


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            player_data["matches_played"]  += 1
            if player_data['score'] < score:
                player_data['score'] = score
            if player_data['level'] < level:
                player_data['level'] = level
            save_player_data(player_data)
            pygame.quit()
            sys.exit()

        if current_screen == "menu":
            if event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    current_screen = "game"

        elif current_screen == "game":
            if event.type == KEYDOWN:
                if event.key == K_LEFT and tile_position > 0:
                    tile_position -= 30
                elif event.key == K_RIGHT and tile_position + tile_width < 300:
                    tile_position += 30

    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        player_data = load_player_data()
        draw_game(player_data)
        save_player_data(player_data)

    pygame.display.update()
