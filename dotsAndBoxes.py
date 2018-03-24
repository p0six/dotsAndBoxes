#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero / romerom@csu.fullerton.edu
# CPSC-386 - Intro to Video Game Development
# Project 2: Simple Classic Video Game in Pygame
# California State University, Fullerton
# March 23, 2018
# ######################################################################################################################
# DONE: 60% for playable game
# DONE: 10% for a clearly defined win and lose state
# DONE: 10% for a legal and random Brain opponent
# TODO: 10% for online instructions or tutoring
# TODO: 5% for a reasonable README.txt file
# TODO: 5% for following the Submission rules
# ######################################################################################################################
# TODO: Add some keys to allow player to create new game / restart game
# TODO: Play a sound when game is over?
# TODO: Maybe give players the option of choosing a color
# TODO: Boxes to represent punches / kicks to opponents bunny avatar, SF2 with an energy bar based on lines_remaining
# ######################################################################################################################

import random
import pygame
import math
from pygame.locals import *

########################################################################################################################
# Some "constants"
########################################################################################################################
GAME_TITLE = 'Dots and Boxes'
COLS = 7
ROWS = 7
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
PADDING = 100
HORIZONTAL = 0
VERTICAL = 1
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # unused thus far.. could potentially add 2 or more opponents
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (240, 250, 250)
DARK_GREY = (90, 90, 50)
WHITE = (255, 255, 255)
PLAYER_COLORS = [BLUE, RED]
########################################################################################################################
# Initialization values..
########################################################################################################################
boxes = []
menu_buttons = []
continue_buttons = []
player_score = [0, 0]
opponent_turn = False
computer_opponent = False
continue_game = True
button_bg = [WHITE, BLUE]
button_fg = [BLACK, WHITE]
player_button_bg = [WHITE, BLACK]
continue_button_bg = [BLUE, GREEN]
p1_button_fg = [BLUE, WHITE]
p2_button_fg = [RED, WHITE]
bunnies = []
display_help = False
########################################################################################################################

pygame.init()
pygame.display.set_caption(GAME_TITLE)  # title of the window...
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
clock = pygame.time.Clock()
random.seed()


def is_box_completed(new_line, lines_used):  # line ~> start_pos, end_pos, color, orientation
    box_count = len(boxes)
    if new_line[3] == HORIZONTAL:  # either the top of a box, or bottom of a box
        for line in lines_used:  # check if line is parallel and that distance is one cell away
            if line[0][0] == new_line[0][0] and line[1][0] == new_line[1][0] and \
                    (abs(line[0][1] - new_line[0][1])) <= math.ceil(((DISPLAY_HEIGHT - (2 * PADDING)) / (ROWS - 1))):
                if line[0][1] > new_line[0][1]:  # our line may be the top side of a box
                    left = right = False
                    vert_lines_used = (x for x in lines_used if x[3] == VERTICAL)
                    for vert_line in vert_lines_used:
                        if new_line[0][0] == vert_line[0][0] and new_line[0][1] == vert_line[0][1]:  # left?
                            left = True
                        elif new_line[1][0] == vert_line[0][0] and new_line[1][1] == vert_line[0][1]:  # right?
                            right = True
                    if left and right:
                        # print('We have created a box by adding a TOP')
                        player_score[opponent_turn] += 1
                        bunny = False
                        if random.sample(range(1, 4), 1)[0] % 4 == 0:
                            bunny = True
                            player_score[opponent_turn] += 3
                        box = (new_line[0], PLAYER_COLORS[opponent_turn], bunny)
                        boxes.append(box)
                else:  # our line may be the bottom side of a box
                    left = right = False
                    vert_lines_used = (x for x in lines_used if x[3] == VERTICAL)
                    for vert_line in vert_lines_used:
                        if new_line[0][0] == vert_line[1][0] and new_line[0][1] == vert_line[1][1]:  # left?
                            left = True
                        elif new_line[1][0] == vert_line[1][0] and new_line[1][1] == vert_line[1][1]:  # right?
                            right = True
                    if left and right:
                        # print('We have created a box by adding a BOTTOM')
                        player_score[opponent_turn] += 1
                        bunny = False
                        if random.sample(range(1, 48), 1)[0] % 12 == 0:
                            bunny = True
                            player_score[opponent_turn] += 3
                        box = (line[0], PLAYER_COLORS[opponent_turn], bunny)
                        boxes.append(box)

    elif new_line[3] == VERTICAL:  # either the left or right hand side of a box
        for line in lines_used:  # check if line is parallel and that distance is one cell away
            if line[0][1] == new_line[0][1] and line[1][1] == new_line[1][1] \
                    and (abs(line[0][0] - new_line[0][0])) <= math.ceil(((DISPLAY_WIDTH - (2 * PADDING)) / (COLS - 1))):
                if line[0][0] > new_line[0][0]:  # our line may be the left side of a box
                    top = bottom = False
                    horz_lines_used = (x for x in lines_used if x[3] == HORIZONTAL)
                    for horz_line in horz_lines_used:
                        if new_line[0][1] == horz_line[0][1] and new_line[0][0] == horz_line[0][0]:  # top?
                            top = True
                        elif new_line[1][1] == horz_line[0][1] and new_line[1][0] == horz_line[0][0]:  # bottom?
                            bottom = True
                    if top and bottom:
                        # print('We have created a box by adding a LEFT')
                        player_score[opponent_turn] += 1
                        bunny = False
                        if random.sample(range(1, 48), 1)[0] % 12 == 0:
                            bunny = True
                            player_score[opponent_turn] += 3
                        box = (new_line[0], PLAYER_COLORS[opponent_turn], bunny)
                        boxes.append(box)
                else:  # our line may be the right side of a box
                    top = bottom = False
                    horz_lines_used = (x for x in lines_used if x[3] == HORIZONTAL)
                    for horz_line in horz_lines_used:
                        if new_line[0][1] == horz_line[1][1] and new_line[0][0] == horz_line[1][0]:  # top?
                            top = True
                        elif new_line[1][1] == horz_line[1][1] and new_line[1][0] == horz_line[1][0]:  # bottom?
                            bottom = True
                    if top and bottom:
                        # print('We have created a box by adding a RIGHT')
                        player_score[opponent_turn] += 1
                        bunny = False
                        if random.sample(range(1, 48), 1)[0] % 12 == 0:
                            bunny = True
                            player_score[opponent_turn] += 3
                        box = (line[0], PLAYER_COLORS[opponent_turn], bunny)
                        boxes.append(box)

    if len(boxes) > box_count:
        return True
    else:
        return False


def evaluate_menu_click(event):
    # rectangle's: (top left x, top left y, width, height)
    x, y = event.pos
    for button in menu_buttons:
        if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
            return button
    return None


def evaluate_continue_click(event):
    x, y = event.pos
    for button in continue_buttons:
        if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
            return button
    return None


def game_menu():
    global COLS
    global ROWS
    global computer_opponent
    global opponent_turn
    global boxes
    global player_score
    global display_help
    intro = True
    while intro:
        clock.tick(10)  # limits while loop to 10 iterations/second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and display_help == True:
                    display_help = False
                elif event.key == K_ESCAPE:
                    return False
                elif event.key == K_RETURN:
                    opponent_turn = False
                    boxes.clear()
                    player_score = [0, 0]
                    return True
                elif event.key == K_h:
                    display_help = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = evaluate_menu_click(event)
                if button_clicked is not None:
                    index = menu_buttons.index(button_clicked)
                    if index == 0:
                        computer_opponent = False
                    elif index == 1:
                        computer_opponent = True
                    elif index == 2:
                        COLS = ROWS = 5
                    elif index == 3:
                        COLS = ROWS = 7
                    else:
                        COLS = ROWS = 9

        # Fill our screen with white..
        screen.fill(WHITE)

        # Display our 'Dots and Boxes' banner..
        banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 90)
        text_surface = banner_font.render(GAME_TITLE, True, BLACK)
        text_rect = text_surface.get_rect()  # get rect, byoch!
        text_rect.center = ((DISPLAY_WIDTH / 2), 45)
        screen.blit(text_surface, text_rect)

        # Press Enter to Play
        banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 60)
        start_text_surface = banner_font.render('Enter to Play', True, BLACK)
        start_text_rect = start_text_surface.get_rect()  # get rect, byoch!
        start_text_rect.center = ((DISPLAY_WIDTH / 2), DISPLAY_HEIGHT - 200)
        screen.blit(start_text_surface, start_text_rect)

        # Escape to Exit
        esc_text_surface = banner_font.render('ESC to Exit', True, BLACK)
        esc_text_rect = esc_text_surface.get_rect()  # get rect, byoch!
        esc_text_rect.center = start_text_rect.center
        esc_text_rect.top = start_text_rect.bottom
        screen.blit(esc_text_surface, esc_text_rect)

        # H for Help
        help_text_surface = banner_font.render('H for Help', True, BLACK)
        help_text_rect = help_text_surface.get_rect()  # get rect, byoch!
        help_text_rect.center = esc_text_rect.center
        help_text_rect.top = esc_text_rect.bottom
        screen.blit(help_text_surface, help_text_rect)

        # Need to display a selection allowing user to choose between 2nd player or computer opponent
        menu_font = pygame.font.Font('ARCADECLASSIC.TTF', 30)

        opponent_text_surface = menu_font.render('Select Opponent', True, BLACK)
        opponent_text_rect = opponent_text_surface.get_rect()  # get rect, byoch!
        opponent_text_rect.left = 100
        opponent_text_rect.top = DISPLAY_HEIGHT / 4
        screen.blit(opponent_text_surface, opponent_text_rect)

        human_text_surface = menu_font.render('Human', True, button_fg[not computer_opponent])
        hum_t_rect = human_text_surface.get_rect()  # get rect, byoch!
        hum_t_rect.left = 100
        hum_t_rect.top = DISPLAY_HEIGHT / 3
        button_human = (hum_t_rect.left - 10, hum_t_rect.top, (hum_t_rect.right + 20) - hum_t_rect.left, 30)
        pygame.draw.rect(screen, button_bg[not computer_opponent], button_human)

        computer_text_surface = menu_font.render('Computer', True, button_fg[computer_opponent])
        comp_t_rect = computer_text_surface.get_rect()  # get rect, byoch!
        comp_t_rect.left = hum_t_rect.right + 50
        comp_t_rect.top = DISPLAY_HEIGHT / 3
        button_computer = (comp_t_rect.left - 10, comp_t_rect.top, (comp_t_rect.right + 20) - comp_t_rect.left, 30)
        pygame.draw.rect(screen, button_bg[computer_opponent], button_computer)

        # rectangle's: (top left x, top left y, width, length)

        screen.blit(human_text_surface, hum_t_rect)
        screen.blit(computer_text_surface, comp_t_rect)

        # Need to display a selection allowing user to choose grid size
        grid_text_surface = menu_font.render('Select Grid Size', True, BLACK)
        grid_text_rect = grid_text_surface.get_rect()  # get rect, byoch!
        grid_text_rect.right = DISPLAY_WIDTH - 100
        grid_text_rect.top = opponent_text_rect.top
        screen.blit(grid_text_surface, grid_text_rect)

        grid5x5_text_surface = menu_font.render('5x5', True, button_fg[COLS == 5])
        g5x5_rect = grid5x5_text_surface.get_rect()  # get rect, byoch!
        g5x5_rect.left = grid_text_rect.left
        g5x5_rect.top = DISPLAY_HEIGHT / 3
        button5x5 = (g5x5_rect.left - 10, g5x5_rect.top, (g5x5_rect.right + 20) - g5x5_rect.left, 30)
        pygame.draw.rect(screen, button_bg[COLS == 5], button5x5)

        grid7x7_text_surface = menu_font.render('7x7', True, button_fg[COLS == 7])
        g7x7_rect = grid7x7_text_surface.get_rect()  # get rect, byoch!
        g7x7_rect.left = g5x5_rect.right + 50
        g7x7_rect.top = DISPLAY_HEIGHT / 3
        button7x7 = (g7x7_rect.left - 10, g7x7_rect.top, (g7x7_rect.right + 20) - g7x7_rect.left, 30)
        pygame.draw.rect(screen, button_bg[COLS == 7], button7x7)

        grid9x9_text_surface = menu_font.render('9x9', True, button_fg[COLS == 9])
        g9x9_rect = grid9x9_text_surface.get_rect()  # get rect, byoch!
        g9x9_rect.left = g7x7_rect.right + 50
        g9x9_rect.top = DISPLAY_HEIGHT / 3
        button9x9 = (g9x9_rect.left - 10, g9x9_rect.top, (g9x9_rect.right + 20) - g9x9_rect.left, 30)
        pygame.draw.rect(screen, button_bg[COLS == 9], button9x9)

        # rectangle's: (top left x, top left y, width, length)
        screen.blit(grid5x5_text_surface, g5x5_rect)
        screen.blit(grid7x7_text_surface, g7x7_rect)
        screen.blit(grid9x9_text_surface, g9x9_rect)

        # Deal with our menu buttons...
        menu_buttons.clear()
        menu_buttons.append(button_human)
        menu_buttons.append(button_computer)
        menu_buttons.append(button5x5)
        menu_buttons.append(button7x7)
        menu_buttons.append(button9x9)

        # Draw help if requested..
        if display_help is True:
            rules_img = pygame.image.load('rules.png')
            rules_blit = pygame.transform.scale(rules_img, (800, 600))
            screen.blit(rules_blit, (0, 0))

        # This must run after all draw commands
        pygame.display.flip()


def generate_lines():
    lines_remaining = []
    for x in range(0, COLS - 1):  # Generate our horizontal lines..
        for y in range(0, ROWS):
            x_start = math.floor((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            x_end = math.floor((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * (x + 1)))
            y_cord = math.floor((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            start_pos = (x_start, y_cord)
            end_pos = (x_end, y_cord)
            line = (start_pos, end_pos, LIGHT_GREY, HORIZONTAL)
            lines_remaining.append(line)

    for x in range(0, COLS):  # Generate our vertical lines...
        for y in range(0, ROWS - 1):
            x_cord = math.floor((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            y_start = math.floor((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            y_end = math.floor((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * (y + 1)))
            start_pos = (x_cord, y_start)
            end_pos = (x_cord, y_end)
            line = (start_pos, end_pos, LIGHT_GREY, VERTICAL)
            lines_remaining.append(line)
    return lines_remaining


def game_loop():
    global opponent_turn
    global continue_game
    global player_score
    global computer_opponent
    lines_remaining = generate_lines()
    lines_used = []

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        clock.tick(10)  # limits while loop to 10 iterations/second

        if computer_opponent and opponent_turn and len(lines_remaining) > 0:
            my_rand = random.randint(0, len(lines_remaining) - 1)
            process_play(lines_remaining[my_rand], lines_remaining, lines_used)
            clock.tick(5000)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                    elif event.key == K_RETURN and len(lines_remaining) == 0:
                        if continue_game == False:
                            return
                        opponent_turn = False
                        boxes.clear()
                        player_score = [0, 0]
                        lines_remaining = generate_lines()
                        lines_used = []
                        computer_opponent = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if len(lines_remaining) == 0:
                        continue_button = evaluate_continue_click(event)
                        if continue_button is not None:
                            index = continue_buttons.index(continue_button)
                            if index == 0:
                                continue_game = False
                            else:
                                continue_game = True
                    else:
                        evaluate_click(event, lines_remaining, lines_used)

        draw_game(lines_remaining, lines_used)


def draw_game(lines_remaining, lines_used):  # Things we're drawing...
    global continue_buttons
    screen.fill(WHITE)

    # Display our 'Dots and Boxes' banner..
    banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 46)
    text_surface = banner_font.render(GAME_TITLE, True, BLACK)
    text_rect = text_surface.get_rect()  # get rect, byoch!
    text_rect.center = ((DISPLAY_WIDTH / 2), 23)
    screen.blit(text_surface, text_rect)

    # Display player scores....
    score_font = pygame.font.Font('JOYSTIX_MONOSPACE.ttf', 14)
    p1_text_surface = score_font.render('Player 1: ' + str(player_score[0]) + ' pts', True,
                                        p1_button_fg[not opponent_turn])
    p1_text_rect = p1_text_surface.get_rect()
    p1_text_rect.left = 10
    p1_text_rect.top = 8
    button_human = (p1_text_rect.left - 10, p1_text_rect.top, (p1_text_rect.right + 20) - p1_text_rect.left, 20)
    pygame.draw.rect(screen, p1_button_fg[opponent_turn], button_human)
    screen.blit(p1_text_surface, p1_text_rect)

    p2_text_surface = score_font.render('Player 2: ' + str(player_score[1]) + ' pts', True, p2_button_fg[opponent_turn])
    p2_text_rect = p2_text_surface.get_rect()
    p2_text_rect.left = p1_text_rect.left
    p2_text_rect.top = p1_text_rect.bottom
    button_human = (p2_text_rect.left - 10, p2_text_rect.top, (p2_text_rect.right + 20) - p2_text_rect.left, 20)
    pygame.draw.rect(screen, p2_button_fg[not opponent_turn], button_human)
    screen.blit(p2_text_surface, p2_text_rect)

    # Draw out lines from lines_remaining and lines_used
    for line in lines_remaining:
        pygame.draw.line(screen, line[2], line[0], line[1], 1)
    for line in lines_used:
        pygame.draw.line(screen, line[2], line[0], line[1], 4)

    # Draw some dots.
    for x in range(0, COLS):
        for y in range(0, ROWS):
            x_cord = math.ceil((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            y_cord = math.ceil((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            pos = (x_cord, y_cord)
            pygame.draw.circle(screen, BLACK, pos, 7)

    # We must draw our '1' or '2' inside of boxes the players own
    box_font = pygame.font.Font('ARCADECLASSIC.TTF', 25)  # TODO: should we make font size a function of grid size?
    for box in boxes:
        if box[1] == PLAYER_COLORS[0]:
            box_text_surface = box_font.render('1', True, box[1])
        else:
            box_text_surface = box_font.render('2', True, box[1])

        box_text_rect = box_text_surface.get_rect()
        box_text_rect.center = (box[0][0] + 15, box[0][1] + 15)
        screen.blit(box_text_surface, box_text_rect)

        if box[2]:  # we have a bunny
            bunny_img = pygame.image.load('bunny.png')
            bunny_blit = pygame.transform.scale(bunny_img, (50, 50))
            screen.blit(bunny_blit, (box_text_rect.right, box_text_rect.top))

    # check if end of game
    if len(lines_remaining) == 0:
        # Display the winner!
        winner_font = pygame.font.Font('ARCADECLASSIC.TTF', 80)
        if player_score[0] > player_score[1]:
            winner_text_surface = winner_font.render('Winner! P1', True, WHITE)
        elif player_score[0] < player_score[1]:
            winner_text_surface = winner_font.render('Winner! P2', True, WHITE)
        else:
            winner_text_surface = winner_font.render('Tie!', True, WHITE)

        winner_rect = winner_text_surface.get_rect()  # get rect, byoch!
        winner_rect.center = ((DISPLAY_WIDTH / 2), winner_rect.bottom)
        winner_rect.bottom = DISPLAY_HEIGHT / 3
        rect_bg_winner = (winner_rect.left - 10, winner_rect.top, (winner_rect.right + 20) - winner_rect.left, 170)
        pygame.draw.rect(screen, button_bg[not computer_opponent], rect_bg_winner)

        # display 'Play again? yes/no'
        continue_font = pygame.font.Font('VIDEOPHREAK.ttf', 30)
        continue_text_surface = continue_font.render('Continue?', True, WHITE)
        continue_rect = continue_text_surface.get_rect()  # get rect, byoch!
        continue_rect.left = winner_rect.left
        continue_rect.top = winner_rect.bottom + 30

        yes_text_surface = continue_font.render('Yes', True,WHITE)
        yes_rect = yes_text_surface.get_rect()  # get rect, byoch!
        yes_rect.left = continue_rect.right + 50
        yes_rect.top = continue_rect.top
        button_yes = (yes_rect.left - 10, yes_rect.top, (yes_rect.right + 20) - yes_rect.left, yes_rect.bottom - yes_rect.top)
        pygame.draw.rect(screen, continue_button_bg[continue_game], button_yes)

        no_text_surface = continue_font.render('No', True, WHITE)
        no_rect = no_text_surface.get_rect()  # get rect, byoch!
        no_rect.left = yes_rect.right + 50
        no_rect.top = yes_rect.top
        button_no = (no_rect.left - 10, no_rect.top, (no_rect.right + 20) - no_rect.left, no_rect.bottom - no_rect.top)
        pygame.draw.rect(screen, continue_button_bg[not continue_game], button_no)

        enter_text_surface = continue_font.render('Enter to Confirm', True, WHITE)
        enter_rect = enter_text_surface.get_rect()  # get rect, byoch!
        enter_rect.center = winner_rect.center
        enter_rect.bottom = continue_rect.top

        continue_buttons.clear()
        continue_buttons.append(button_no)
        continue_buttons.append(button_yes)

        screen.blit(winner_text_surface, winner_rect)
        screen.blit(continue_text_surface, continue_rect)
        screen.blit(yes_text_surface, yes_rect)
        screen.blit(no_text_surface, no_rect)
        screen.blit(enter_text_surface, enter_rect)

    # This must run after all draw commands
    pygame.display.flip()


def evaluate_click(event, lines_remaining, lines_used):
    x, y = event.pos
    for line in lines_remaining:  # start_pos, end_pos, color, orientation
        x_start = line[0][0]
        y_start = line[0][1]
        x_end = line[1][0]
        y_end = line[1][1]

        if x_start == x_end:  # horizontal.. make horizontal/vertical lines easier to match
            horizontal_wiggle = 20  # TODO: change wiggle if grid has lots of dots
            vertical_wiggle = 4
        else:
            horizontal_wiggle = 4
            vertical_wiggle = 20

        if x_end + horizontal_wiggle >= x >= x_start - horizontal_wiggle \
                and y_end + vertical_wiggle >= y >= y_start - vertical_wiggle:  # clicked in boundary of remaining line
            process_play(line, lines_remaining, lines_used)
            break


def process_play(line, lines_remaining, lines_used):
    global opponent_turn
    lines_remaining.remove(line)
    my_line = (line[0], line[1], PLAYER_COLORS[opponent_turn], line[3])

    box_count = len(boxes)
    if is_box_completed(line, lines_used):  # player continue, box added to boxes[]
        if len(boxes) - box_count > 1:
            pygame.mixer.Sound('smb_1-up.wav').play()
        else:
            pygame.mixer.Sound('smb_coin.wav').play()
    else:  # next player's turn
        opponent_turn = not opponent_turn
    lines_used.append(my_line)


def main():
    continue_loop = True
    while continue_loop:
        continue_loop = game_menu()
        if continue_loop:
            replay_game = game_loop()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
