import pygame, sys, random

# General setup
pygame.init()
clock = pygame.time.Clock()

# Main window
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game variables
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,20,20)
player = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,110)
opponent = pygame.Rect(10,screen_height/2 - 70,10,110)

bg_colour = pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 8 * random.choice((1,-1)) # Speed of ball in terms of the x axis
ball_speed_y = 8 * random.choice((1,-1)) # Speed of ball in terms of the y axis
player_speed = 0
opponent_speed = 0

# Text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf',32)

# Timer
score_time = True


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x 
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
    
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # Collision mechanics

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0: 
        if abs(ball.left - opponent.right) < 10: 
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    opponent.y += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, current_time, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2,screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render('3',True,light_grey)
        screen.blit(number_three,(screen_width/2 - 10,screen_height/2 + 20))
    
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2',True,light_grey)
        screen.blit(number_two,(screen_width/2 - 10,screen_height/2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1',True,light_grey)
        screen.blit(number_one,(screen_width/2 - 10,screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 8 * random.choice((1,-1)) #
        ball_speed_x = 8 * random.choice((1,-1)) #
        score_time = None

while True:
    # Handling user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                opponent_speed += 7
            if event.key == pygame.K_w:
                opponent_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                opponent_speed -= 7
            if event.key == pygame.K_w:
                opponent_speed += 7
           

    
    ball_animation()
    player_animation()
    opponent_animation()


    # Visuals
    screen.fill(bg_colour)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height)) # anti-aliased line

    player_text = game_font.render(f'{player_score}',True,light_grey)
    screen.blit(player_text,(660,400))

    opponent_text = game_font.render(f'{opponent_score}',True,light_grey)
    screen.blit(opponent_text,(600,400))

    if score_time:
        ball_restart()

    # Updating game window
    pygame.display.flip()
    clock.tick(60) # max times/frames per second
