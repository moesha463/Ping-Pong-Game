import pygame;

pygame.init();

screen = pygame.display.set_mode([300, 300]);
pygame.display.set_caption('Ping Pong Game');

timer = pygame.time.Clock()
framerate = 60;

black = (0, 0, 0);
white = (255, 255, 255);

player_y = 130;
computer_y = 130;
ball_x = 145;
ball_y = 145;

player_direction = 0;
player_speed = 3;

running = True;

while running:
    timer.tick(framerate);
    screen.fill(black);
    
    player = pygame.draw.rect(screen, white, [5, player_y, 10, 40]);
    computer = pygame.draw.rect(screen, white, [285, computer_y, 10, 40]);
    ball = pygame.draw.rect(screen, white, [ball_x, ball_y, 10, 10])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_direction = -1;
            if event.key == pygame.K_s:
                player_direction = 1;
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_direction = 0;
            if event.key == pygame.K_s:
                player_direction = 0;

    player_y += player_speed * player_direction;

    pygame.display.flip();

pygame.quit()