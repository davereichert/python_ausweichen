import turtle
import random

# setup player or obstacle figure
def setup_figure(x_pos, y_pos, shape='circle', color='red', size=3, y_size=None):
    figure = turtle.Turtle()
    figure.speed(0)
    figure.shape(shape)
    figure.color(color)
    figure.shapesize(stretch_wid=size if y_size is None else y_size, stretch_len=size)
    figure.penup()
    figure.goto(x_pos, y_pos)
    return figure

# Setting up the screen
wn = turtle.Screen()
wn.title('Ausweichen by Dave')
wn.bgcolor('grey')
wn.setup(width=600, height=800)
wn.tracer(0)
setup_figure(x_pos=-100, y_pos=0, shape='square', color='white', size=0.5, y_size=40)
setup_figure(x_pos=100, y_pos=0, shape='square', color='white', size=0.5, y_size=40)
obstacles = []

# restarting the app
def restart():
    global counter_distance
    counter_distance = 100
    global obstacle_speed
    obstacle_speed = 2
    global score
    score = 0
    global counter
    counter = 0
    global obstacles
    for obstacle in obstacles:
        obstacle.hideturtle()
    obstacles = []
    global run
    run = True

restart()

# create list of obstacles
def create_random_obstacles(prob_one=0.5, prob_two=0.5):
    rnd = random.random()
    if rnd < prob_two:
        rand_pos = random.sample([-200, 0, 200], k=2)
        return [setup_figure(x_pos=rand_pos[0], y_pos=350), setup_figure(x_pos=rand_pos[1], y_pos=350)]
    elif rnd < prob_one + prob_two:
        rand_pos = random.sample([-200, 0, 200], k=1)
        return [setup_figure(x_pos=rand_pos[0], y_pos=350)]
    else:
        return []

player = setup_figure(x_pos=0, y_pos=-350, shape='square', color='blue')

# configuring the pen to write the score
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()
pen.goto(-200, 350)

# move player left
def move_left():
    x = player.xcor()
    if x > -200:
        player.setx(x-200)

# move player right
def move_right():
    x = player.xcor()
    if x < 200:
        player.setx(x+200)

# Keyboard binding
wn.listen()
wn.onkeypress(move_left, 'Left')
wn.onkeypress(move_right, 'Right')
wn.onkeypress(restart, 'r')

run = True

# Main game loop
while True:
    wn.update()
    if run == True:
        if counter % counter_distance == 0:
            obstacles = obstacles + create_random_obstacles(prob_one=0.4, prob_two=0.4)
        counter = counter + 1
        lost = False
        for obstacle in obstacles:
            obstacle.sety(obstacle.ycor() - obstacle_speed)
            if (player.xcor() == obstacle.xcor()) and (obstacle.ycor() < -300) and (obstacle.ycor() > -400):
                lost = True
                run = False
            if obstacle.ycor() < -400:
                obstacle.hideturtle()
                score = score + 1
                obstacles.remove(obstacle)
        if lost == True:
            pen.clear()
            pen.write(f'Lost: {score}' , align='center', font=('Courier', 24, 'normal'))
        else:
            pen.clear()
            pen.write(f'Score: {score}', align='center', font=('Courier', 24, 'normal'))