import pygame
from os.path import join

from random import randint

class Player(pygame.sprite.sprite):
    def __init__(self):
        super().__init()
        self.image = pygame.image.load(player_path).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))



#general setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT=1200,720
display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

pygame.display.set_caption("Space Shooter")
running=True
clock=pygame.time.Clock()

player_path=join('images','player.png')

star_path=join('images','star.png')

meteor_path=join('images','meteor.png')

lesser_path=join('images','laser.png')
# print(path)

player_surf=pygame.image.load(player_path).convert_alpha()
player_rect=player_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))



star_surf=pygame.image.load(star_path).convert_alpha()
star_position=[(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(20)]

meteor_surf=pygame.image.load(meteor_path).convert_alpha()
meteor_rect=meteor_surf.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

lesser_surf=pygame.image.load(lesser_path).convert_alpha()
lesser_rect=lesser_surf.get_frect(bottomleft=(20,WINDOW_HEIGHT-20))

player_direction=pygame.math.Vector2()
player_speed= 300

# plain_rect=pygame.FRect()

while running:
    dt = clock.tick() / 1000
    # print(clock.get_fps())
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
    #input
    # print(pygame.mouse.get_pressed()[0])   
    
    keys=pygame.key.get_pressed() 
    player_direction.x=int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y=int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    
    player_direction = player_direction.normalize() if player_direction else player_direction
    # if keys[pygame.K_RIGHT]:
    #     player_direction.x=1
    # else:
    #     player_direction.x=0
    player_rect.center += player_direction * player_speed * dt
    
    recent_keys=pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print("FIre laser")
    
    #drop the game
    display_surface.fill('darkgray')
    
    # print(player_rect.left)
    for pos in star_position:
        display_surface.blit(star_surf,pos)
    
    # x+=0.1

    display_surface.blit(meteor_surf,meteor_rect)
    display_surface.blit(lesser_surf,lesser_rect)    
    display_surface.blit(player_surf,player_rect)
    
    #player Movement
    # player_rect.x += player_direction * 100
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction *=-1
    
    if player_rect.bottom >=WINDOW_HEIGHT:
        player_rect.bottom =WINDOW_HEIGHT
        player_direction.y *= 1
        
     
    
    # if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0 :
    #     player_direction.y *= -1
    # if player_rect.right  >= WINDOW_WIDTH or player_rect.left <= 0:
    #     player_direction.x *= -1
    
    # player_rect.center +=player_direction * player_speed * dt
    
    pygame.display.update()
    

pygame.quit()