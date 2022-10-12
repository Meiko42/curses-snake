import curses
from time import sleep
from collections import deque
import random
from playsound import playsound

soundOn = True

def play_game(subwin):

    subwin_height, subwin_width = subwin.getmaxyx()

    snake_head = [int(subwin_height / 2), int(subwin_width / 2)]
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

        # Up
        if snake_direction == 119:
            snake_head[0] = snake_head[0]-1
        # Down
        if snake_direction == 115:
            snake_head[0] = snake_head[0]+1
        # Left
        if snake_direction == 97:
            snake_head[1] = snake_head[1]-1
        # Right
        if snake_direction == 100:
            snake_head[1] = snake_head[1]+1

        if 0 > snake_head[0] or snake_head[0] >= subwin_height or 0 > snake_head[1] or snake_head[1] >= subwin_width:
            if soundOn == True:
                playsound('wav/splat.wav')
            game_over = True

        if snake_head == food_coordinates:
            if soundOn == True:
                playsound('wav/nom.wav')
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
            curses.beep()
            return len(snake_segments)

        if not game_over:
            subwin.clear()
            # addstr advances cursor, causes exception when going near bottom right of window
            # addchstr isn't exposed, so using try/except instead. 
            try:
                subwin.addstr(snake_head[0],snake_head[1], "@")
            except curses.error:
                pass
            if snake_segments:
                for snake_body_coordinate in snake_segments:
                    # addstr advances cursor, causes exception when going near bottom right of window
                    # addchstr isn't exposed, so using try/except instead. 
                    try:
                        subwin.addstr(snake_body_coordinate[0],snake_body_coordinate[1], "#")
                    except curses.error:
                        pass
                    if snake_body_coordinate == snake_head:
                        game_over = True
            subwin.addstr(food_coordinates[0],food_coordinates[1], food_symbol)
            subwin.refresh()
            sleep(.1)



def do_it(win):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.curs_set(0)
    win.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    height,width = win.getmaxyx()

    subwin_height = 20
    subwin_width = 20
    subwin_y_begin = int(height / 2 - int(subwin_height / 2))
    subwin_x_begin = int(width / 2 - int(subwin_width / 2))

    subwin = curses.newwin(subwin_height, subwin_width, subwin_y_begin, subwin_x_begin)
    subwin.bkgd(' ', curses.color_pair(2))
    subwin.nodelay(1)
    subwin.addstr(10,10, "@")
    win.refresh()
    subwin.refresh()

    high_score = 0

    while True:
        win.addstr(subwin_y_begin - 1, subwin_x_begin, f"High Score: {high_score}")
        win.refresh()
        last_max_length = play_game(subwin)
        win.addstr(0, int(width / 2 - 5), f"GAME OVER")
        if last_max_length > high_score:
            high_score = last_max_length
        win.addstr(subwin_y_begin - 1, subwin_x_begin, f"High Score: {high_score}")
        win.refresh()
        sleep(10)
        win.clear()


if __name__ == '__main__':
    curses.wrapper(do_it)