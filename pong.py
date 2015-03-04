'''
# Todo: 
# Paddle AI
# Wii controls
# Pause
# Start menu
'''
import pygame, sys
from pygame.locals import *
import math

# ball movement:
def move_ball(b, x_dir, y_dir):
    b.x += x_dir * BALL_SPEED
    b.y += y_dir * BALL_SPEED
    return b

# arena collision detection
def edge_collide(ball, x, y):
    if ball.top <= LINE_THICKNESS or ball.bottom >= (DISP_H - LINE_THICKNESS):
        PLOP.play()
        y = -y
    if ball.left <= LINE_THICKNESS or ball.right >= (DISP_W - LINE_THICKNESS):
        PLOP.play()
        x = -x 
    return x, y

# control paddles and keep them within arena bounds
def move_paddle(p, upkey, downkey):
    keys = pygame.key.get_pressed()
    if keys[upkey]:
        p.top -= PADDLE_SPEED
        if p.top < LINE_THICKNESS:
            p.top = LINE_THICKNESS
    if keys[downkey]:
        p.top += PADDLE_SPEED
        if p.top > DISP_H - (PADDLE_H + LINE_THICKNESS):
            p.top = DISP_H - (PADDLE_H + LINE_THICKNESS)
    return p

# paddle collision detection
def paddle_collide(ball, paddle1, paddle2, x):
    global BALL_SPEED
    left_paddle_conditions = [paddle1.right >= ball.left, x < 0,
                              paddle1.top < ball.top, paddle1.bottom > ball.bottom] 
    right_paddle_conditions = [paddle2.left <= ball.right, x > 0,
                              paddle2.top < ball.top, paddle2.bottom > ball.bottom]

    if all(left_paddle_conditions) or all(right_paddle_conditions):
        BEEEP.play()
        return -1
    else:
        return 1

# goal collision detection / scorekeeping
def goal_collide(ball, score1, score2):
    global BALL_SPEED
    if ball.left <= LINE_THICKNESS:
        PEEEEEEP.play()
        score2 += 1
    elif ball.right >= (DISP_W - LINE_THICKNESS):
        PEEEEEEP.play()
        score1 += 1
    return score1, score2


pygame.init()

# Global variables
FPS = 60
CLOCK = pygame.time.Clock()
DISP_W = 400
DISP_H = 300
DISPLAYSURF = pygame.display.set_mode((DISP_W, DISP_H))
pygame.display.set_caption('Pong by Eli ;3')

# colors, bg, paddle and ball graphics
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREEN   = (  0, 192,   0)
MAGENTA = (192,   0, 192)

LINE_THICKNESS = 10
PADDLE_H = 75
BALL_X = (DISP_W - LINE_THICKNESS) / 2
BALL_Y = (DISP_H - LINE_THICKNESS) / 2

P1_XPOS = LINE_THICKNESS
P2_XPOS = DISP_W - (LINE_THICKNESS*2)
YPOS = (DISP_H - PADDLE_H) / 2
PADDLE_SPEED = 5
BALL_SPEED = 5


# sound effects courtesy of 
# http://opengameart.org/content/3-ping-pong-sounds-8-bit-style
PEEEEEEP = pygame.mixer.Sound('sounds/ping_pong_8bit_peeeeeep.ogg')
BEEEP = pygame.mixer.Sound('sounds/ping_pong_8bit_beeep.ogg')
PLOP = pygame.mixer.Sound('sounds/ping_pong_8bit_plop.ogg')

# instantiate paddle/ball objects
player1_paddle = pygame.Rect(P1_XPOS, YPOS, LINE_THICKNESS, PADDLE_H)
player2_paddle = pygame.Rect(P2_XPOS, YPOS, LINE_THICKNESS, PADDLE_H)
ball = pygame.Rect(BALL_X, BALL_Y, LINE_THICKNESS, LINE_THICKNESS)

#initialize ball direction
x_dir = 1
y_dir = 1

# initialize score and score disp. font
p1_score = p2_score = 0
fontpath = "/Library/Fonts/Andale Mono.ttf"
myfont = pygame.font.Font(fontpath, 24)

# main game loop
while True:
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, GREEN, 
        ((0, 0), (DISP_W, DISP_H)), LINE_THICKNESS * 2)
    pygame.draw.rect(DISPLAYSURF, WHITE, player1_paddle)
    pygame.draw.rect(DISPLAYSURF, WHITE, player2_paddle)
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # paddle movement handling
    player1_paddle = move_paddle(player1_paddle, pygame.K_w, pygame.K_s) 
    player2_paddle = move_paddle(player2_paddle, pygame.K_i, pygame.K_k) 

    # move ball & check for an edge collision
    # change direction if necessary
    ball = move_ball(ball, x_dir, y_dir)
    x_dir, y_dir = edge_collide(ball, x_dir, y_dir)
    x_dir = x_dir * paddle_collide(ball, player1_paddle, player2_paddle, x_dir)

    p1label = myfont.render("%s" % (p1_score), True, MAGENTA)
    p2label = myfont.render("%s" % (p2_score), True, MAGENTA)
    label1pos = (LINE_THICKNESS * 3, LINE_THICKNESS * 2)
    label2pos = (DISP_W - (LINE_THICKNESS * 5), LINE_THICKNESS * 2)
    DISPLAYSURF.blit(p1label, label1pos)    
    DISPLAYSURF.blit(p2label, label2pos)    

    # check for a goal and update score
    p1_score, p2_score = goal_collide(ball, p1_score, p2_score)

    pygame.display.update()
    CLOCK.tick(FPS)
