import pygame
import random


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Heredamos funcionalidades de la clase Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load("./Assets/Player/bird1.png"),
            pygame.image.load("./Assets/Player/bird2.png"),
            pygame.image.load("./Assets/Player/bird3.png")
        ]
        self.counter = 0
        self.index = 0
        self.cooldown = 6
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #Hacemos un rectángulo de nuestra imágen.
        self.rect.center = [x, y] #Le damos su posición
        self.velocity_y = 0
        self.flying = False
        self.game_over = False
        
    def animation(self):
        self.movement()
        if self.game_over == False:
            self.counter += 1
            #Hacemos un cooldown antes de cambiar de imagen
            if self.counter > self.cooldown:
                self.counter = 0
                self.index += 1 #Aumentamos nuestro índice para recorrer las imágenes
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            
            #Rotamos la imagen cuandi este de caída
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity_y * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
    
    def movement(self):
        #En nuestro pajara tenemos dos fuerzas que están actuando,
        #Una es la gravedad que esta actuando constantemente.
        #En cada iteración la velocidad con la que cae va aumentando
       #Gravity
       if self.flying:
            self.velocity_y += 0.5
            if self.velocity_y > 8:
                self.velocity_y = 0    
        
        #Jump
        #Mientras sea menor el valor "y" del pajaro a 504 ira aumentado en "y"
       if not self.game_over:
            if self.rect.bottom < 504: 
                self.rect.y += int(self.velocity_y) 
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.rect.y > 0:
                    self.rect.y -= 10
                    print("AARINNA")


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Assets/pipe.png')
        self.rect = self.image.get_rect()
        pipe_gap = 150
        #if posisiotn  1  is from the top, -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    
    def update(self, speed):
        self.rect.x -= speed


def draw_game(screen, bg, bg2, scroll, bird_arr, bird, pipe_group):
    #Draw Background
    screen.blit(bg, [0, 0])
    #Draw Pipe
    pipe_group.draw(screen)
    #Draw scrolling background of the floor
    screen.blit(bg2, [scroll, 504])
    
    bird.animation()
    bird_arr.draw(screen) #Dibujamos a nuestro pajaro, el método drwa() lo heredamos de Sprite
    pipe_group.update(4)

    pygame.display.update()


def run():
    pygame.init()
    
    #FPS
    clock = pygame.time.Clock()
    FPS = 60
    
    #Screen set up
    screen_width = 664
    screen_height = 600
    
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption(("Flappy Bird"))
    
    #Game Variables
    scroll_speed = 4
    ground_scroll = 0
    pipe_frecuency = 1500 #Milisegundos
    last_pipe = pygame.time.get_ticks() - pipe_frecuency
    
    #Load Images
    background = pygame.transform.scale(pygame.image.load("./Assets/Bckground/bg.png"), [screen_width, 504])
    background_floor = pygame.transform.scale(pygame.image.load("./Assets/Bckground/ground.png"), [screen_width + 35, 96])
    
    
    bird_group = pygame.sprite.Group() #Creamos un grupo para nuestros sprites
    pipe_group = pygame.sprite.Group() #Grupo para nuestros Pipes
    
    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy) #Agregamos a nuestro grupo
    
    
    
    running = True
    while running:
        #Frame Rate
        clock.tick(FPS)
        
        #Scroll Background
        if not flappy.game_over and flappy.flying == True:
            
            #Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frecuency:
                pipe_height = random.randint(-100, 100)
                bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height /2) + pipe_height, 1)
                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            
            #Si el juego llega estar en game over ya no habra scroll
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            
        #Game Over
        if flappy.rect.bottom >= 504:
            flappy.game_over = True
            flappy.flying = False

        draw_game(screen, background, background_floor, ground_scroll, bird_group, flappy, pipe_group)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #JUMP
            elif event.type == pygame.KEYDOWN and not flappy.game_over:
                if event.key == pygame.K_SPACE:
                 flappy.movement()
                 flappy.flying = True
    
    pygame.quit()
    


if __name__ == '__main__':
    run()
    