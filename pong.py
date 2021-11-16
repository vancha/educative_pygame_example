#!/usr/bin/env python

import pygame

WINDOW_WIDTH  = 400
WINDOW_HEIGHT = 400

pygame.init()
display = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

#the paddle class, representing a player in the game
class paddle():
    #initializing all the variables, called when instantiated
    def __init__(self,move_up_key, move_down_key,x,y):
        #this sets the key that is used to make this paddle move up
        self.move_up_key = move_up_key
        #this sets the key that is used to make this paddle move down
        self.move_down_key = move_down_key
        #this sets the paddles initial x position, so it knows where to draw itself
        self.x = x
        #this sets the paddles initial y position, also required to draw itself
        self.y = y
        #this is used to set the paddles speed, increase it to make the paddle move faster
        self.speed = 5
        #width of the paddle in pixels,for drawing
        self.width = 20
        #height of the paddle in pixels,for drawing
        self.height = 100
        #upon instantiation, the paddle is not meant to move up, this variable keeps track of that
        self.moving_up = False
        #upon instantiation,it's not meant to move down either
        self.moving_down = False
    
    #moves the paddle up a little
    def move_up(self):
       self.y -= self.speed
    #moves the paddle down a little
    def move_down(self):
        self.y += self.speed
    #tells the paddle that it should start moving up
    def start_moving_up(self):
        self.moving_up = True
    #tells the paddle that it should start moving down
    def start_moving_down(self):
        self.moving_down = True
    #tells the paddle that it should stop moving up
    def stop_moving_up(self):
        self.moving_up = False
    #tells the paddle that it should stop moving down
    def stop_moving_down(self):
        self.moving_down = False
    def touches_ball(self,b):
        #is the balls x position larger than this paddles, and is it smaller than it's width?
        #if so, then they are aligned horizontally
        #if they are also aligned vertically, that means they are touching
        return pygame.Rect(self.x,self.y,self.width,self.height).colliderect(pygame.Rect(b.x,b.y,b.width,b.height))
    #pdates the paddle, and draws it to the screen at the same time
    def update(self):
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()
        self.draw()
    #draws the paddle to the screen
    def draw(self):
        pygame.draw.rect(display, (255, 255, 255), (self.x,self.y,self.width,self.height))

#describes our ball
class ball:
    def __init__(self):
        #the ball has an x and y position as well
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        #the ball has a radius
        self.width = 10
        self.height = 10
        #and it has a velocity
        self.x_velocity = 5
        self.y_velocity = 4
    #this updates and draws the ball
    def update(self):
        if(self.out_through_top_or_bottom()):
            self.reverse_vertical_direction()
        #if(self.out_through_sides()):
        #    self.reverse_horizontal_direction()
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.draw()
    #this reverses the balls horizontal direction
    def reverse_horizontal_direction(self):
        self.x_velocity *= -1
    #this reverses the balls vertical direction
    def reverse_vertical_direction(self):
        self.y_velocity *= -1
    #this checks if the ball left the visible window horizontally
    def out_through_sides(self):
        return self.x > WINDOW_WIDTH or self.x < 0
    #this checks if the ball left the visible window vertically
    def out_through_top_or_bottom(self):
        return self.y > WINDOW_HEIGHT or self.y < 0
    #draws the ball
    def draw(self):
        pygame.draw.rect(display, (255, 255, 255), (self.x,self.y,self.width,self.height))

#creates a new ball
b = ball()
#creates two players, and puts them in a list called players
players = [paddle(pygame.K_w,pygame.K_s,0,0),paddle(pygame.K_UP,pygame.K_DOWN,WINDOW_WIDTH-20,WINDOW_HEIGHT/2)]
#run forever
while True:
    #make the screen black
    display.fill((0,0,0))
    #this unwieldy code is called once so we don't have to send the entire
    #list of events to every object in our game. For performance reasons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key ==  players[0].move_up_key:
                players[0].start_moving_up();
            elif event.key ==  players[0].move_down_key:
                 players[0].start_moving_down();
            elif event.key == players[1].move_up_key:
                players[1].start_moving_up();
            elif event.key == players[1].move_down_key:
                players[1].start_moving_down();
        elif event.type == pygame.KEYUP:
            if event.key ==  players[0].move_up_key:
                 players[0].stop_moving_up();
            elif event.key ==  players[0].move_down_key:
                 players[0].stop_moving_down();
            elif event.key == players[1].move_up_key:
                players[1].stop_moving_up();
            elif event.key == players[1].move_down_key:
                players[1].stop_moving_down();
                
    #update the ball
    b.update()
    if(b.out_through_sides()):
        pygame.quit()
    #update the players
    for player in players:
        #update the players state
        player.update()
        #if a player is currently touching the ball
        if(player.touches_ball(b)):
            #make sure the ball goes in the other direction
            b.reverse_horizontal_direction()
    #make sure the game runs at the same speed for slow as well as fast computers
    clock.tick(60)
    # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
    #This will update the contents of the entire display.
    pygame.display.flip()
