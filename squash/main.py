from tkinter import *
import random
import platform

GAME_TITLE = "SQUASH GAME"
GAME_MOVE = 1 # 0:ノーマル 1:リバース
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MIN_BALL_MOVE_X = 5
MAX_BALL_MOVE_X = 25
MIN_BALL_MOVE_Y = 10
MAX_BALL_MOVE_Y = 50
BALL_ACCELERATION = 3
MAX_RACKET_SIZE_X = 180
MIN_RACKET_SIZE_X = 10
RACKET_SHRINK_SPEED = 5

win = Tk()
cv = Canvas(win, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
cv.pack()

def init_game():
    global is_gameover, ball_position_x, ball_position_y
    global ball_move_x, ball_move_y, ball_y_direction, ball_size, BALL_ACCELERATION
    global racket_position_x, racket_position_y, racket_size_x, racket_size_y, point, speed

    is_gameover = False
    ball_position_x = 300
    ball_position_y = 10
    ball_move_x = 20
    ball_move_y = MIN_BALL_MOVE_Y
    ball_y_direction = 1
    ball_size = 10
    racket_position_x = 0
    racket_position_y = 10
    racket_size_x = MAX_RACKET_SIZE_X
    racket_size_y = 20
    point = 0
    speed = 50

    set_win_title()

def draw_screen():
    cv.delete('all')
    color = background_color()
    cv.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill=color, width = 0)

def draw_ball():
    cv.create_oval(ball_position_x - ball_size, ball_position_y - ball_size,
            ball_position_x + ball_size, ball_position_y + ball_size, fill="red")

def draw_racket():
    cv.create_rectangle(racket_position_x, racket_y_position(),
            racket_position_x + racket_size_x, racket_y_position() + racket_size_y, fill = "yellow")

def move_ball():
    global ball_position_x, ball_position_y, ball_move_x, ball_move_y, ball_y_direction
    global racket_position_x, racket_size_x, racket_size_y, is_gameover, ball_size
    if is_gameover: return

    ball_position_x = ball_position_x + ball_move_x
    ball_position_y = ball_position_y + ball_move_y * ball_y_direction

    if ball_position_x <= 0:
        ball_position_x = 0
        ball_move_x = random.randint(MIN_BALL_MOVE_X, MAX_BALL_MOVE_X)
        beep(1320, 50)

    if ball_position_x + ball_size >= SCREEN_WIDTH:
        ball_position_x = SCREEN_WIDTH - ball_size
        ball_move_x = random.randint(MIN_BALL_MOVE_X, MAX_BALL_MOVE_X) * -1

    if ball_position_y <= 0:
        ball_position_y = 0
        ball_y_direction *= -1
        beep(1320, 50)

    if ball_position_y > racket_y_position() - ball_size and (
            racket_position_x <= ball_position_x and ball_position_x + ball_size <= racket_position_x + racket_size_x
            ):
        ball_position_y = racket_y_position() - ball_size
        ball_y_direction *= -1
        beep(2000, 50)
        increase_score()

    if ball_position_y > SCREEN_HEIGHT:
        beep(200, 800)
        is_gameover = True
        set_win_title("GAMEOVER! CLICK IS CONTINUE")

def motion(event):
    global racket_position_x, is_gameover
    if is_gameover: return
    racket_position_x = event.x

    # X座標反転処理
    if not is_normal_mode():
        racket_position_x = SCREEN_WIDTH - racket_position_x

    if racket_position_x < 0:
        racket_position_x = 0
    if racket_position_x > SCREEN_WIDTH - racket_size_x:
        racket_position_x = SCREEN_WIDTH - racket_size_x

def click(event):
    if event.num == 1 and is_gameover:
        init_game()

def set_win_title(text=GAME_TITLE):
    title = text + " (" + "SCORE:" + str(point) + ")"
    win.title(title)

def beep(freq, dur=100):
    if platform.system() == "windows":
        import winsound
        winsound.Beep(frep, dur)
    else:
        return
        #import os
        #os.system('play -n synth %s sin %s' % (dur/1000, freq))

def racket_y_position():
    return SCREEN_HEIGHT - racket_position_y - racket_size_y

def increase_score():
    global point
    point += 1
    set_win_title()
    ball_speed_up()

def ball_speed_up():
    global ball_move_y, racket_size_x
    ball_move_y += BALL_ACCELERATION
    if ball_move_y > MAX_BALL_MOVE_Y:
        ball_move_y = MAX_BALL_MOVE_Y
    racket_size_x -= RACKET_SHRINK_SPEED
    if racket_size_x < MIN_RACKET_SIZE_X:
        racket_size_x = MIN_RACKET_SIZE_X

def background_color():
    return "white" if is_normal_mode() else "black"

def is_normal_mode():
    if GAME_MOVE != 1: return True
    return point % 2 == 0

win.bind('<Motion>', motion)
win.bind('<Button>', click)

def game_loop():
    draw_screen()
    draw_ball()
    draw_racket()
    move_ball()
    win.after(speed, game_loop)

init_game()
game_loop()
win.mainloop()

