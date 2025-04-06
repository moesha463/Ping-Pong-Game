import pygame;

pygame.init();

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40
BALL_SIZE = 10

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]);

icon = pygame.image.load('./assets/images/icon.png');
pygame.display.set_icon(icon);

pygame.display.set_caption('Ping Pong Game');

timer = pygame.time.Clock()
framerate = 60;

black = (0, 0, 0);
white = (255, 255, 255);

game_over = False;

bounce_sound = pygame.mixer.Sound('./assets/sounds/bounce.mp3')

font = pygame.font.Font('./assets/fonts/PixelOperator.ttf', 30);

player_y = 130;
computer_y = 130;
ball_x = 145;
ball_y = 145;

player_direction = 0;
player_speed = 3;

ball_x_direction = 1;
ball_y_direction = 1;
ball_speed = 2;
ball_y_speed = 1;

score = 0;
current_level = 1;
level_up_time = 0;


def update_ai(ball_y, computer_y):
    computer_y = ball_y - PADDLE_HEIGHT // 2
    if computer_y < 0:
        computer_y = 0
    elif computer_y > SCREEN_HEIGHT - PADDLE_HEIGHT:
        computer_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    return computer_y


def check_collisions(ball, player, computer, ball_x_direction, score):
    if ball.colliderect(player) and ball_x_direction == -1:
        ball_x_direction = 1
        score += 1
        bounce_sound.play()
    elif ball.colliderect(computer) and ball_x_direction == 1:
        ball_x_direction = -1
        score += 1
        bounce_sound.play()
    
    return ball_x_direction, score


def update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed):
    if ball_x_direction == 1 and ball_x < 290:
        ball_x += ball_speed;
    elif ball_x_direction == 1 and ball_x >= 290:
        ball_x_direction *= -1;
    
    if ball_x_direction == -1 and ball_x > 0:
        ball_x -= ball_speed;
    elif ball_x_direction == -1 and ball_x <= 0:
        ball_x_direction *= -1;
    
    if ball_y_direction == 1 and ball_y < 290:
        ball_y += ball_y_speed;
    elif ball_y_direction == 1 and ball_y >= 290:
        ball_y_direction *= -1;
    
    if ball_y_direction == -1 and ball_y > 0:
        ball_y -= ball_y_speed;
    elif ball_y_direction == -1 and ball_y <= 0:
        ball_y_direction *= -1;

    return ball_x_direction, ball_y_direction, ball_x, ball_y;

def check_game_over(ball_x, game_over):
    if ball_x <= 0 or ball_x >= 290 and game_over == False:
        game_over = True;
    
    return game_over;

def reset_game():
    global player_y, computer_y, ball_x, ball_y, player_direction, ball_x_direction, ball_y_direction, ball_speed, ball_y_speed, score, game_over
    player_y = 130
    computer_y = 130
    ball_x = 145
    ball_y = 145
    player_direction = 0
    ball_x_direction = 1
    ball_y_direction = 1
    ball_speed = 2
    ball_y_speed = 1
    score = 0
    game_over = False


running = True;

while running:
    timer.tick(framerate);
    screen.fill(black);
    
    player = pygame.draw.rect(screen, white, [5, player_y, PADDLE_WIDTH, PADDLE_HEIGHT]);
    computer = pygame.draw.rect(screen, white, [285, computer_y, PADDLE_WIDTH, PADDLE_HEIGHT]);
    ball = pygame.draw.rect(screen, white, [ball_x, ball_y, BALL_SIZE, BALL_SIZE])
    game_over = check_game_over(ball_x, game_over);

    score_text = font.render(str(score), True, white);
    screen.blit(score_text, (140, 70));


    if not game_over:
        computer_y = update_ai(ball_y, computer_y);
        ball_x_direction, ball_y_direction, ball_x, ball_y = update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed);

        new_level = 1 + (score // 10)
        if new_level > current_level:
            current_level = new_level
            level_up_time = pygame.time.get_ticks()

    if level_up_time > 0 and pygame.time.get_ticks() - level_up_time < 2000:
        level_text = font.render(f'Level {current_level}', True, white)
        screen.blit(level_text, (120, 130))

    ball_x_direction, score = check_collisions(ball, player, computer, ball_x_direction, score);

    if game_over:
        game_over_text = font.render('Game Over', True, white, black);
        screen.blit(game_over_text, (100, 130));

        current_time = pygame.time.get_ticks() // 500

        if current_time % 2 == 0:
            restart_text = font.render('Press any button', True, white, black)
            screen.blit(restart_text, (65, 170))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_direction = -1;
            if event.key == pygame.K_s:
                player_direction = 1;
            if game_over:
                reset_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_direction = 0;
            if event.key == pygame.K_s:
                player_direction = 0;

    player_y += player_speed * player_direction
    if player_y < 0:
        player_y = 0
    elif player_y > 260:
        player_y = 260

    ball_speed = 2 + (score//10);
    ball_y_speed = 1 + (score//15);

    pygame.display.flip();

pygame.quit()