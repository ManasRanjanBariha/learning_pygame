import pygame
from os.path import join

from random import randint,uniform

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        
        #cooldown
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration =400
        
        self.mask=pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        
        # self.image = mask_surf
        
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot=True
        
    def update(self,dt):
        # print("ship being Updated")
        keys=pygame.key.get_pressed()
        
        self.direction.x=int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y=int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        self.rect.center += self.direction * self.speed * dt
        
        recent_keys=pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            # print("FIre laser")
            Laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time=pygame.time.get_ticks()
            laser_sound.play()
            
        self.laser_timer()
        
class Star(pygame.sprite.Sprite):
     def __init__(self,groups):
         super().__init__(groups)
         self.image=pygame.image.load(star_path).convert_alpha()
         self.rect=self.image.get_frect(center= (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups ):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.rect.y -=400 * dt
        if self.rect.bottom < 0 :
            self.kill()
        
class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf,groups):
        super().__init__(groups)
        self.orginal=surf
        self.image = surf
        self.rect = self.image.get_frect(midtop = (randint(0,WINDOW_WIDTH),0))
        self.created_time=pygame.time.get_ticks()
        self.lifetime =3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        self.rotational_speed = randint(10,100)
        self.rotation=0
        # self.mask = pygame.mask.from_surface(self.image)
        
        
        
    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        current_time=pygame.time.get_ticks()
        
        self.rotation += self.rotational_speed * dt
        self.image=pygame.transform.rotozoom(self.orginal,self.rotation,1)
        self.rect= self.image.get_frect(center= self.rect.center)
        
        if current_time - self.created_time >= self.lifetime:
            self.kill()
        
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[0]
        self.rect=self.image.get_frect(center = pos)
    
    def update(self,dt):
        self.frame_index  += 50 * dt
        if self.frame_index < len(self.frames):
            self.image =self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()
    
    
def collisons():
    global running
    collison_sprites= pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask)
    if collison_sprites:
        # damage_sound.play()
        running=False
    
    for laser in laser_sprites:
        collided_sprites=pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(exploation_frames, laser.rect.midtop,all_sprites)
            explosion_sound.play()
    all_sprites.draw(display_surface)

def display_score():
    current_time=pygame.time.get_ticks()//100
    text_surf=font.render(str(current_time),True,(240,240,240)) 
    text_rect=text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    pygame.draw.rect(display_surface,'#ffffff',text_rect.inflate(20,30).move(0,-10),5,10)
    display_surface.blit(text_surf,text_rect)
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

r_position=[(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(20)]
meteor_surf=pygame.image.load(meteor_path).convert_alpha()
laser_surf=pygame.image.load(lesser_path).convert_alpha()
star_surf=pygame.image.load(player_path).convert_alpha()
font=pygame.font.Font(join('images','Oxanium-Bold.ttf'),36)
exploation_frames =[ pygame.image.load( join('images','explosion',f'{i}.png')).convert_alpha()   for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio','damage.ogg'))
game_music = pygame.mixer.Sound(join('audio','game_music.wav'))

game_music.set_volume(0.3)
game_music.play( loops =-1)



# player_direction=pygame.math.Vector2()
# player_speed= 300

# plain_rect=pygame.FRect()

all_sprites = pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
player=Player(all_sprites,star_surf)
for i in range(20):
    Star(all_sprites)
    

#custom events ->meteor event

meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)

while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == meteor_event:
            # print("meteor")
            Meteor(meteor_surf,(all_sprites,meteor_sprites))
    
    
    display_surface.fill('#3a2e3f')
    

    all_sprites.update(dt)
    display_score()
    # display_surface.blit(text_surf,(0,0))

    collisons()
    
    
    # pygame.draw.rect(display_surface, 'red', player.rect, 10,)
    

    
    pygame.display.update()
    

pygame.quit()