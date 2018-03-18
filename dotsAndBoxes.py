#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Some colors...
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
light_grey = (240, 250, 250)
white = (255, 255, 255)

########
display_width = 800
display_height = 600
padding = 100

cols = 5
rows = 5
horizontal_lines = (cols - 1) * rows
vertical_lines = cols * (rows - 1)
total_turns = horizontal_lines + vertical_lines
horizontal = 0
vertical = 1

boxes = []
player_colors = [blue, red]
player_score = [0, 0]
opponent_turn = False
######

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption('Dots and Boxes')  # title of the window...


def is_box_completed(new_line, lines_used):  # line ~> start_pos, end_pos, color, orientation (0 = horz, 1 = vert)
    box_count = len(boxes)
    if new_line[3] == 0:  # either the top of a box, or bottom of a box
        for line in lines_used:
            if line[0][0] == new_line[0][0] and line[1][0] == new_line[1][0]:  # partial horizontal match, check dist
                if (abs(line[0][1] - new_line[0][1])) == int(((display_height - (2 * padding)) / (rows - 1))):
                    if line[0][1] > new_line[0][1]:  # our line may be the top side of a box
                        left = right = False
                        for vert_line in lines_used:
                            if vert_line[0][1] != vert_line[1][1]:  # line is vertical
                                if new_line[0][0] == vert_line[0][0] and new_line[0][1] == vert_line[0][1]:  # left?
                                    left = True
                                elif new_line[1][0] == vert_line[0][0] and new_line[1][1] == vert_line[0][1]:  # right?
                                    right = True
                        if left is True and right is True:
                            print('We have created a box by adding a TOP')
                            player_score[opponent_turn] += 1
                            box = (new_line[0], player_colors[opponent_turn])
                            boxes.append(box)
                    else:  # our line may be the bottom side of a box THIS CHECK IS BAD
                        sys.stdout.write('Our Line: ')
                        print(new_line)
                        left = right = False
                        for vert_line in lines_used:
                            if vert_line[0][1] != vert_line[1][1]:  # line is vertical
                                if new_line[0][0] == vert_line[1][0] and new_line[0][1] == vert_line[1][1]:  # left?
                                    left = True
                                elif new_line[1][0] == vert_line[1][0] and new_line[1][1] == vert_line[1][1]:  # right?
                                    right = True
                        if left is True and right is True:
                            print('We have created a box by adding a BOTTOM')
                            player_score[opponent_turn] += 1
                            box = (line[0], player_colors[opponent_turn])
                            boxes.append(box)

    elif new_line[3] == 1:  # either the left or right hand side of a box
        for line in lines_used:
            if line[0][1] == new_line[0][1] and line[1][1] == new_line[1][1]:  # partial vertical match, check dist
                if (abs(line[0][0] - new_line[0][0])) == int(((display_width - (2 * padding)) / (cols - 1))):
                    if line[0][0] > new_line[0][0]:  # our line may be the left side of a box
                        top = bottom = False
                        for horz_line in lines_used:
                            if horz_line[0][0] != horz_line[1][0]:  # line is horizontal
                                if new_line[0][1] == horz_line[0][1] and new_line[0][0] == horz_line[0][0]:  # top?
                                    top = True
                                elif new_line[1][1] == horz_line[0][1] and new_line[1][0] == horz_line[0][0]:  # bottom?
                                    bottom = True
                        if top and bottom:
                            print('We have created a box by adding a LEFT')
                            player_score[opponent_turn] += 1
                            box = (new_line[0], player_colors[opponent_turn])
                            boxes.append(box)
                    else:  # our line may be the right side of a box
                        top = bottom = False
                        for horz_line in lines_used:
                            if horz_line[0][0] != horz_line[1][0]:  # line is horizontal
                                if new_line[0][1] == horz_line[1][1] and new_line[0][0] == horz_line[1][0]:  # top?
                                    top = True
                                elif new_line[1][1] == horz_line[1][1] and new_line[1][0] == horz_line[1][0]:  # bottom?
                                    bottom = True
                        if top and bottom:
                            print('We have created a box by adding a RIGHT')
                            player_score[opponent_turn] += 1
                            box = (line[0], player_colors[opponent_turn])
                            boxes.append(box)
    if len(boxes) > box_count:
        return True
    else:
        return False


def game_intro():
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
        screen.fill(white)

        # Display our 'Dots and Boxes' banner..
        banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 90)
        text_surface = banner_font.render('Dots and Boxes', True, black)
        text_rect = text_surface.get_rect()  # get rect, byoch!
        text_rect.center = ((display_width / 2), 45)
        screen.blit(text_surface, text_rect)

        # This must run after all draw commands
        pygame.display.flip()


def generate_lines():
    lines_remaining = []
    # Generate our horizontal lines..
    for x in range(0, cols - 1):
        for y in range(0, rows):
            x_start = int((padding + ((display_width - 2 * padding) / (cols - 1)) * x))
            x_end = int((padding + ((display_width - 2 * padding) / (cols - 1)) * (x + 1)))
            y_cord = int((padding + ((display_height - 2 * padding) / (rows - 1)) * y))
            start_pos = (x_start, y_cord)
            end_pos = (x_end, y_cord)
            line = (start_pos, end_pos, light_grey, horizontal)
            lines_remaining.append(line)

    # Generate our vertical lines...
    for x in range(0, cols):
        for y in range(0, rows - 1):
            x_cord = int((padding + ((display_width - 2 * padding) / (cols - 1)) * x))
            y_start = int((padding + ((display_height - 2 * padding) / (rows - 1)) * y))
            y_end = int((padding + ((display_height - 2 * padding) / (rows - 1)) * (y + 1)))
            start_pos = (x_cord, y_start)
            end_pos = (x_cord, y_end)
            line = (start_pos, end_pos, light_grey, vertical)
            lines_remaining.append(line)
    return lines_remaining


def game_loop():
    global opponent_turn
    lines_remaining = generate_lines()
    lines_used = []

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        clock.tick(10)  # limits while loop to 10 iterations/second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continue_loop = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for line in lines_remaining:  # start_pos, end_pos, color
                    x_start = line[0][0]
                    y_start = line[0][1]
                    x_end = line[1][0]
                    y_end = line[1][1]

                    # NEED TO ADJUST THIS TO MAKE HORIZONTAL LINES HAVE LARGER VERTICAL WIGGLE
                    # NEED TO ADJUST THIS TO MAKE VERTICAL LINES HAVE LARGER HORIZONTAL WIGGLE
                    if x_start == x_end:  # horizontal
                        horizontal_wiggle = 20
                        vertical_wiggle = 4
                    else:
                        horizontal_wiggle = 4
                        vertical_wiggle = 20

                    if x_end + horizontal_wiggle >= x >= x_start - horizontal_wiggle \
                            and y_end + vertical_wiggle >= y >= y_start - vertical_wiggle:  # match
                        lines_remaining.remove(line)
                        start_pos = line[0]
                        end_pos = line[1]
                        orientation = line[3]
                        my_line = (start_pos, end_pos, player_colors[opponent_turn], orientation)

                        # If box, player continues next turn, and box added to boxes[]
                        if is_box_completed(line, lines_used):  # player continue, box added to boxes[]
                            print('We completed a box!')
                            print('Player 1 Score: ' + str(player_score[opponent_turn]) +
                                  ', Player 2 Score: ' + str(player_score[not opponent_turn]))
                        else:  # next player's turn
                            opponent_turn = not opponent_turn
                        lines_used.append(my_line)
                        break

        # Things we're drawing...
        screen.fill(white)

        # Display our 'Dots and Boxes' banner..
        banner_font = pygame.font.Font('ARCADECLASSIC.TTF', 46)
        text_surface = banner_font.render('Dots and Boxes', True, black)
        text_rect = text_surface.get_rect()  # get rect, byoch!
        text_rect.center = ((display_width / 2), 23)
        screen.blit(text_surface, text_rect)

        # Draw out lines from lines_remaining
        for line in lines_remaining:
            pygame.draw.line(screen, line[2], line[0], line[1], 1)
        for line in lines_used:
            pygame.draw.line(screen, line[2], line[0], line[1], 4)

        # Time to draw some dots...
        for x in range(0, cols):
            for y in range(0, rows):
                x_cord = int((padding + ((display_width - 2 * padding) / (cols - 1)) * x))
                y_cord = int((padding + ((display_height - 2 * padding) / (rows - 1)) * y))
                pos = (x_cord, y_cord)
                pygame.draw.circle(screen, black, pos, 5)

        # We must draw our '1' or '2' inside of boxes the players own
        box_font = pygame.font.Font('ARCADECLASSIC.TTF', 25)
        for box in boxes:
            if box[1] == player_colors[0]:
                box_text_surface = box_font.render('1', True, box[1])
            else:
                box_text_surface = box_font.render('2', True, box[1])
            box_text_rect = box_text_surface.get_rect()
            box_text_rect.center = (box[0][0] + 15, box[0][1] + 15)
            screen.blit(box_text_surface, box_text_rect)

        # This must run after all draw commands
        pygame.display.flip()


def main():
    game_intro()
    game_loop()
    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
