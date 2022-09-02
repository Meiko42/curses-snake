import curses
from time import sleep
from collections import deque
import random

def do_it(win):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.curs_set(0)
    win.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    height,width = win.getmaxyx()

    subwin_height = 20
    subwin_width = 20

    subwin = curses.newwin(subwin_height, subwin_width, int(height / 2 - 10), int(width / 2 - 10))
    subwin.bkgd(' ', curses.color_pair(2))
    subwin.nodelay(1)
    subwin.addstr(10,10, "@")
    win.refresh()
    subwin.refresh()

    snake_head = [10, 10]
    snake_direction = 119

    food_symbol = "*"

    food_coordinates = []
    snake_length = 0
    snake_segments = deque()

    game_over = False

    while True:

        snake_head_pre_move = snake_head.copy()

        new_snake_direction = subwin.getch()
        if new_snake_direction != -1:
            snake_direction = new_snake_direction

        if snake_direction == 119:
            snake_head[0] = snake_head[0]-1
        if snake_direction == 115:
            snake_head[0] = snake_head[0]+1
        if snake_direction == 97:
            snake_head[1] = snake_head[1]-1
        if snake_direction == 100:
            snake_head[1] = snake_head[1]+1

        if 0 > snake_head[0] or snake_head[0] >= subwin_height or 0 > snake_head[1] or snake_head[1] >= subwin_width:
            game_over = True

        if snake_head == food_coordinates:
            food_coordinates = []
            snake_length += 1
            snake_segments.append(snake_head_pre_move)

        if food_coordinates:
            snake_segments.append(snake_head_pre_move)
            snake_segments.popleft()

        if not food_coordinates:
            food_y = random.randint(1, 19)
            food_x = random.randint(1, 19)
            food_coordinates = [food_y, food_x]

        if game_over:
            win.addstr(0, int(width / 2 - 5), "GAME OVER")
            win.refresh()
            sleep(30)

        if not game_over:
            subwin.clear()
            subwin.addstr(snake_head[0],snake_head[1], "@")
            if snake_segments:
                for snake_body_coordinate in snake_segments:
                    subwin.addstr(snake_body_coordinate[0],snake_body_coordinate[1], "#")
                    if snake_body_coordinate == snake_head:
                        game_over = True
            subwin.addstr(food_coordinates[0],food_coordinates[1], food_symbol)
            subwin.refresh()
            sleep(.3)


    
    # while True:
    #     # Check if screen was re-sized (True or False)
    #     resize = True

    #     # Action in loop if resize is True:
    #     if resize is True:
    #         y, x = win.getmaxyx()
    #         win.clear()
    #         curses.resizeterm(y, x)
    #         win.refresh()



if __name__ == '__main__':
    curses.wrapper(do_it)