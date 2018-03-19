#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero
# CPSC-386 - Intro to Video Game Development
# Project 2: Simple Classic Video Game in Pygame
# California State University, Fullerton
# March 18, 2018
# REQD:#################################################################################################################
# TODO: Finish by 11pm Friday March 23rd for 10% Extra Credit
# TODO: Finish start menu by allowing player to choose opponent
# TODO: Create Level-0 Brain opponent
# TODO: Need to add the "bunny" - give players option of selecting which "bunny" avatar and use it to mark box
# NICE:#################################################################################################################
# TODO: Update game logic to display score of players within game
# TODO: Add some keys to allow player to create new game / restart game
# TODO: Detect when game ends, announce winner, ask player if they want to play again or return to main menu
# TODO: Give player the option to select grid size.. maybe pre-defined list of grid sizes based on desired play length
# TODO: Maybe give players the option of choosing a color
# TODO: Play a sound when a box is completed, when game is over?
# TODO: Replace any conditional checking for vertical/horizontal to use line's orientation property @ line[3]
# ######################################################################################################################

import pygame
from pygame.locals import *

########################################################################################################################
# Some "constants"
########################################################################################################################
GAME_TITLE = 'Dots and Boxes'
COLS = 5
ROWS = 5
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
WHITE = (255, 255, 255)
PLAYER_COLORS = [BLUE, RED]
########################################################################################################################
# Initialization values..
########################################################################################################################
boxes = []
player_score = [0, 0]
opponent_turn = False
computer_opponent = False
########################################################################################################################

pygame.init()
pygame.display.set_caption(GAME_TITLE)  # title of the window...
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
clock = pygame.time.Clock()


def is_box_completed(new_line, lines_used):  # line ~> start_pos, end_pos, color, orientation
    box_count = len(boxes)
    if new_line[3] == HORIZONTAL:  # either the top of a box, or bottom of a box
        for line in lines_used:  # check if line is parallel and that distance is one cell away
            if line[0][0] == new_line[0][0] and line[1][0] == new_line[1][0] and \
                    (abs(line[0][1] - new_line[0][1])) == int(((DISPLAY_HEIGHT - (2 * PADDING)) / (ROWS - 1))):
                if line[0][1] > new_line[0][1]:  # our line may be the top side of a box
                    left = right = False
                    vert_lines_used = (x for x in lines_used if x[3] == VERTICAL)
                    for vert_line in vert_lines_used:
                        if new_line[0][0] == vert_line[0][0] and new_line[0][1] == vert_line[0][1]:  # left?
                            left = True
                        elif new_line[1][0] == vert_line[0][0] and new_line[1][1] == vert_line[0][1]:  # right?
                            right = True
                    if left and right:
                        print('We have created a box by adding a TOP')
                        player_score[opponent_turn] += 1
                        box = (new_line[0], PLAYER_COLORS[opponent_turn])
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
                        print('We have created a box by adding a BOTTOM')
                        player_score[opponent_turn] += 1
                        box = (line[0], PLAYER_COLORS[opponent_turn])
                        boxes.append(box)

    elif new_line[3] == VERTICAL:  # either the left or right hand side of a box
        for line in lines_used:  # check if line is parallel and that distance is one cell away
            if line[0][1] == new_line[0][1] and line[1][1] == new_line[1][1] \
                    and (abs(line[0][0] - new_line[0][0])) == int(((DISPLAY_WIDTH - (2 * PADDING)) / (COLS - 1))):
                if line[0][0] > new_line[0][0]:  # our line may be the left side of a box
                    top = bottom = False
                    horz_lines_used = (x for x in lines_used if x[3] == HORIZONTAL)
                    for horz_line in horz_lines_used:
                        if new_line[0][1] == horz_line[0][1] and new_line[0][0] == horz_line[0][0]:  # top?
                            top = True
                        elif new_line[1][1] == horz_line[0][1] and new_line[1][0] == horz_line[0][0]:  # bottom?
                            bottom = True
                    if top and bottom:
                        print('We have created a box by adding a LEFT')
                        player_score[opponent_turn] += 1
                        box = (new_line[0], PLAYER_COLORS[opponent_turn])
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
                        print('We have created a box by adding a RIGHT')
                        player_score[opponent_turn] += 1
                        box = (line[0], PLAYER_COLORS[opponent_turn])
                        boxes.append(box)

    if len(boxes) > box_count:
        return True
    else:
        return False


def game_menu():
    intro = True
    while intro:
        clock.tick(10)  # limits while loop to 10 iterations/second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_RETURN:
                    return

        # Fill our screen with white..
        screen.fill(WHITE)

        # Display our 'Dots and Boxes' banner..
        banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 90)
        text_surface = banner_font.render(GAME_TITLE, True, BLACK)
        text_rect = text_surface.get_rect()  # get rect, byoch!
        text_rect.center = ((DISPLAY_WIDTH / 2), 45)
        screen.blit(text_surface, text_rect)

        # This must run after all draw commands
        pygame.display.flip()


def generate_lines():
    lines_remaining = []
    for x in range(0, COLS - 1):  # Generate our horizontal lines..
        for y in range(0, ROWS):
            x_start = int((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            x_end = int((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * (x + 1)))
            y_cord = int((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            start_pos = (x_start, y_cord)
            end_pos = (x_end, y_cord)
            line = (start_pos, end_pos, LIGHT_GREY, HORIZONTAL)
            lines_remaining.append(line)

    for x in range(0, COLS):  # Generate our vertical lines...
        for y in range(0, ROWS - 1):
            x_cord = int((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            y_start = int((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            y_end = int((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * (y + 1)))
            start_pos = (x_cord, y_start)
            end_pos = (x_cord, y_end)
            line = (start_pos, end_pos, LIGHT_GREY, VERTICAL)
            lines_remaining.append(line)
    return lines_remaining


def game_loop():
    global opponent_turn
    lines_remaining = generate_lines()
    lines_used = []

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        clock.tick(10)  # limits while loop to 10 iterations/second

        if computer_opponent and opponent_turn:  # TODO: Implement this logic...
            print('Computer Turn')

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continue_loop = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        continue_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    evaluate_click(event, lines_remaining, lines_used)

        draw_game(lines_remaining, lines_used)


def draw_game(lines_remaining, lines_used):  # Things we're drawing...
    screen.fill(WHITE)

    # Display our 'Dots and Boxes' banner..
    banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 46)
    text_surface = banner_font.render(GAME_TITLE, True, BLACK)
    text_rect = text_surface.get_rect()  # get rect, byoch!
    text_rect.center = ((DISPLAY_WIDTH / 2), 23)
    screen.blit(text_surface, text_rect)

    # Draw out lines from lines_remaining and lines_used
    for line in lines_remaining:
        pygame.draw.line(screen, line[2], line[0], line[1], 1)
    for line in lines_used:
        pygame.draw.line(screen, line[2], line[0], line[1], 4)

    # Time to draw some dots.
    for x in range(0, COLS):
        for y in range(0, ROWS):
            x_cord = int((PADDING + ((DISPLAY_WIDTH - 2 * PADDING) / (COLS - 1)) * x))
            y_cord = int((PADDING + ((DISPLAY_HEIGHT - 2 * PADDING) / (ROWS - 1)) * y))
            pos = (x_cord, y_cord)
            pygame.draw.circle(screen, BLACK, pos, 5)

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
            horizontal_wiggle = 20
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
    lines_used.append(my_line)

    if is_box_completed(line, lines_used):  # player continue, box added to boxes[] TODO: success sound or message?
        print('Player 1 Score: ' + str(player_score[0]) + ', Player 2 Score: ' + str(player_score[1]))
    else:  # next player's turn  TODO: perhaps some type of player change notification?
        opponent_turn = not opponent_turn


def main():
    game_menu()
    game_loop()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()