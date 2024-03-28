import pygame
import sys
from random import randint
from data.entities import Fireball
from csv import reader, writer


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dodgeball")
        self.screen = pygame.display.set_mode((640,480))
        self.background = pygame.image.load("data/surfaces/background.png")
        self.arena = pygame.image.load("data/surfaces/arena.png")
        self.clock = pygame.time.Clock()

        self.player = pygame.image.load("data/entities/player.png")
        self.player_pos = [310, 230]
        self.v_movement = [False, False]
        self.h_movement = [False, False]

        self.collision_area = pygame.Rect(120, 120, 400, 240)

        self.coin = pygame.image.load("data/entities/coin2.png")
        self.coin.set_colorkey((0, 0, 0))
        self.coin_pos = [randint(125, 505), randint(125, 345)]
        self.score = 0

        self.fireballs = []
        self.end = 30

        self.highscore_info = list(reader(open("data/highscores.csv")))

        self.new = []


    def start(self):
        while True:
            self.home = pygame.image.load("data/surfaces/titlescreen.png")
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arena, (120, 120))
            self.screen.blit(self.home, (160, 65))

            font = pygame.font.SysFont("impact", 20)
            score1 = font.render(f"1. {self.highscore_info[0][1]} :  {self.highscore_info[0][0]}", False, (0, 0, 0), (127, 127, 127))
            score2 = font.render(f"2. {self.highscore_info[1][1]} :  {self.highscore_info[1][0]}", False, (0, 0, 0), (127, 127, 127))
            score3 = font.render(f"3. {self.highscore_info[2][1]} :  {self.highscore_info[2][0]}", False, (0, 0, 0), (127, 127, 127))
            score4 = font.render(f"4. {self.highscore_info[3][1]} :  {self.highscore_info[3][0]}", False, (0, 0, 0), (127, 127, 127))
            score5 = font.render(f"5. {self.highscore_info[4][1]} :  {self.highscore_info[4][0]}", False, (0, 0, 0), (127, 127, 127))
            self.screen.blit(score1, (270, 210))
            self.screen.blit(score2, (270, 250))
            self.screen.blit(score3, (270, 290))
            self.screen.blit(score4, (270, 330))
            self.screen.blit(score5, (270, 370))

            font = pygame.font.SysFont("impact", 52)
            title = font.render("Dodgeball", False, (0, 0, 0), (127, 127, 127))
            self.screen.blit(title, ((640 - title.get_width())/2, 72))

            new_game_button = pygame.Rect(245, 145, 150, 20)
            exit_button = pygame.Rect(245, 175, 150, 20)
            mouse_pos = pygame.mouse.get_pos()
            mouse_r = pygame.Rect(mouse_pos[0], mouse_pos[1], 3, 3)

            button = pygame.image.load("data/surfaces/title_button.png")
            self.screen.blit(button, (245, 145))
            self.screen.blit(button, (245, 175))

            font = pygame.font.SysFont("impact", 12)
            new_game_text = font.render("New Game", False, (0, 0, 0), (195, 195, 195))
            exit_text = font.render("Exit", False, (0, 0, 0), (195, 195, 195))
            self.screen.blit(new_game_text, (292, 146))
            self.screen.blit(exit_text, (307, 176))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_r.colliderect(new_game_button):
                    Game().run()
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_r.colliderect(exit_button):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


    def run(self):
        while True:
            pygame.mouse.set_visible(False)

            player_r = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player.get_width(), self.player.get_height())
            self.screen.blit(self.background, (0, 0))
            if not player_r.colliderect(self.collision_area):
                self.score = 0

            self.screen.blit(self.arena, (120, 120))

            font = pygame.font.SysFont("timesnewroman", 20)
            text = font.render(f"Score: {self.score}   Level: {31 - self.end}", False, (0, 0, 0), (255, 255, 255))
            scoreboard_back = pygame.Rect(0, 0, text.get_width() + 30, text.get_height() + 20)
            pygame.draw.rect(self.screen, (255, 255, 255), scoreboard_back)
            self.screen.blit(text, (15, 10))

            self.screen.blit(self.coin, self.coin_pos)
            coin_r = pygame.Rect(self.coin_pos[0], self.coin_pos[1], self.coin.get_width(), self.coin.get_height())
            if player_r.colliderect(coin_r):
                self.score += 10
                self.coin_pos = [randint(130, 510), randint(130, 350)]

            if randint(1, 500) == 1 and self.end != 1:
                self.end -= 1
            rand = randint(1, self.end)
            if rand == 1:
                self.fireballs.append(Fireball())

            for i in range(len(self.fireballs)):
                fireball_r = pygame.Rect(self.fireballs[i].position[0], self.fireballs[i].position[1], self.fireballs[i].image.get_width(), self.fireballs[i].image.get_height())
                if player_r.colliderect(fireball_r):
                    if self.score > int(self.highscore_info[4][0]):
                        for i in range(5):
                            if self.score > int(self.highscore_info[i][0]):
                                rank = i
                                break
                        start = 4
                        while start > rank:
                            self.highscore_info[start] = self.highscore_info[start-1]
                            start -= 1
                        self.highscore_info[rank] = [f'{self.score}', 'AAA']
                    else:
                        rank = 5
                    with open("data/highscores.csv", "w", newline='') as csvfile:
                        scorewriter = writer(csvfile)
                        scorewriter.writerows(self.highscore_info)
                    Game().end_game(rank)

                self.screen.blit(self.fireballs[i].image, self.fireballs[i].position)
                self.fireballs[i].position[0] += self.fireballs[i].slope * 3.5
                self.fireballs[i].position[1] += 3.5
                if self.fireballs[i].position[1] == 480:
                    del self.fireballs[i]
                    break

            self.player_pos[1] += (self.v_movement[1] - self.v_movement[0]) * 3
            self.player_pos[0] += (self.h_movement[1] - self.h_movement[0]) * 3
            self.screen.blit(self.player, self.player_pos)

            if self.player_pos[0] < 0:
                self.player_pos[0] = 0
            elif self.player_pos[0] > 625:
                self.player_pos[0] = 625
            elif self.player_pos[1] < 0:
                self.player_pos[1] = 0
            elif self.player_pos[1] > 465:
                self.player_pos[1] = 465

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.v_movement[0] = True
                    if event.key == pygame.K_s:
                        self.v_movement[1] = True
                    if event.key == pygame.K_a:
                        self.h_movement[0] = True
                    if event.key == pygame.K_d:
                        self.h_movement[1] = True
                    if event.key == pygame.K_UP:
                        self.v_movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.v_movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.h_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.h_movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.v_movement[0] = False
                    if event.key == pygame.K_s:
                        self.v_movement[1] = False
                    if event.key == pygame.K_a:
                        self.h_movement[0] = False
                    if event.key == pygame.K_d:
                        self.h_movement[1] = False
                    if event.key == pygame.K_UP:
                        self.v_movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.v_movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.h_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.h_movement[1] = False

            pygame.display.update()
            self.clock.tick(60)


    def end_game(self, rank):
        while True:
            pygame.mouse.set_visible(True)

            self.home = pygame.image.load("data/surfaces/titlescreen.png")
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arena, (120, 120))
            self.screen.blit(self.home, (160, 65))

            font = pygame.font.SysFont("impact", 20)
            score1 = font.render(f"1. {self.highscore_info[0][1]} :  {self.highscore_info[0][0]}", False, (0, 0, 0), (127, 127, 127))
            score2 = font.render(f"2. {self.highscore_info[1][1]} :  {self.highscore_info[1][0]}", False, (0, 0, 0), (127, 127, 127))
            score3 = font.render(f"3. {self.highscore_info[2][1]} :  {self.highscore_info[2][0]}", False, (0, 0, 0), (127, 127, 127))
            score4 = font.render(f"4. {self.highscore_info[3][1]} :  {self.highscore_info[3][0]}", False, (0, 0, 0), (127, 127, 127))
            score5 = font.render(f"5. {self.highscore_info[4][1]} :  {self.highscore_info[4][0]}", False, (0, 0, 0), (127, 127, 127))
            self.screen.blit(score1, (270, 210))
            self.screen.blit(score2, (270, 250))
            self.screen.blit(score3, (270, 290))
            self.screen.blit(score4, (270, 330))
            self.screen.blit(score5, (270, 370))

            font = pygame.font.SysFont("impact", 52)
            if rank == 5:
                game_over = font.render("Game Over", False, (0, 0, 0), (127, 127, 127))
            else: 
                game_over = font.render("New Score!", False, (180, 12, 12), (127, 127, 127))
            self.screen.blit(game_over, ((640 - game_over.get_width())/2, 72))

            new_game_button = pygame.Rect(245, 145, 150, 20)
            home_button = pygame.Rect(245, 175, 150, 20)
            mouse_pos = pygame.mouse.get_pos()
            mouse_r = pygame.Rect(mouse_pos[0], mouse_pos[1], 3, 3)

            button = pygame.image.load("data/surfaces/title_button.png")
            self.screen.blit(button, (245, 145))
            self.screen.blit(button, (245, 175))

            font = pygame.font.SysFont("impact", 12)
            new_game_text = font.render("New Game", False, (0, 0, 0), (195, 195, 195))
            home_text = font.render("Title Screen", False, (0, 0, 0), (195, 195, 195))
            self.screen.blit(new_game_text, (292, 146))
            self.screen.blit(home_text, (288, 176))

            if rank != 5:
                events = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]
                letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                csvfile = open("data/highscores.csv", "w", newline='')
                scorewriter = writer(csvfile)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key in events:
                            self.new.append(letters[events.index(event.key)])
                        if event.key == pygame.K_BACKSPACE:
                            if len(self.new) > 0:
                                del self.new[-1]
                        if event.key == pygame.K_RETURN:
                            rank = 5
                if len(self.new) == 4:
                    del self.new[-1]
                if len(self.new) == 0:
                    initials = "AAA"
                elif len(self.new) == 1:
                    initials = f"{self.new[0]}AA"
                elif len(self.new) == 2:
                    initials = f"{self.new[0]}{self.new[1]}A"
                elif len(self.new) == 3:
                    initials = f"{self.new[0]}{self.new[1]}{self.new[2]}"
                score = self.highscore_info[rank][0]
                self.highscore_info[rank] = [score, initials]

                scorewriter.writerows(self.highscore_info)

            if rank == 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and mouse_r.colliderect(new_game_button):
                        Game().run()
                    if event.type == pygame.MOUSEBUTTONDOWN and mouse_r.colliderect(home_button):
                        Game().start()

            pygame.display.update()
            self.clock.tick(60)


Game().start()