from turtle import Turtle, Screen
import random
import time

SIZE = 20

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def drawself(self, turtle):
        """ draw a black box at its coordinates, leaving a small gap between cubes """

        turtle.goto(self.x - SIZE // 2 - 1, self.y - SIZE // 2 - 1)
        turtle.fillcolor("yellow")

        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(SIZE - SIZE // 10)
            turtle.left(90)
        turtle.end_fill()

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def changelocation(self):
        # I haven't programmed it to spawn outside the snake's body yet
        self.x = random.randint(0, SIZE) * SIZE - 100
        self.y = random.randint(0, SIZE) * SIZE - 100

    def drawself(self, turtle):
        # similar to the Square drawself, but blinks on and off
        turtle.goto(self.x - SIZE // 2 - 1, self.y - SIZE // 2 - 1)
        turtle.fillcolor("red")

        turtle.begin_fill()
        turtle.circle(SIZE // 1.8)  # Draw a circle with radius equal to half the size
        for _ in range(4):
            turtle.forward(SIZE - SIZE // 10)
            turtle.left(90)
        turtle.end_fill()

class Snake:
    def __init__(self):
        self.headposition = [SIZE, 0]  # keeps track of where it needs to go next
        self.body = [Square(-SIZE, 0), Square(0, 0), Square(SIZE, 0)]  # body is a list of squares
        self.nextX = 1  # tells the snake which way it's going next
        self.nextY = 0
        self.crashed = False  # I'll use this when I get around to collision detection
        self.nextposition = [self.headposition[0] + SIZE * self.nextX, self.headposition[1] + SIZE * self.nextY]
        # prepares the next location to add to the snake

    def moveOneStep(self):
        if Square(self.nextposition[0], self.nextposition[1]) not in self.body: 
            # attempt (unsuccessful) at collision detection
            self.body.append(Square(self.nextposition[0], self.nextposition[1])) 
            # moves the snake head to the next spot, deleting the tail
            del self.body[0]
            self.headposition[0], self.headposition[1] = self.body[-1].x, self.body[-1].y 
            # resets the head and nextposition
            self.nextposition = [self.headposition[0] + SIZE * self.nextX, self.headposition[1] + SIZE * self.nextY]
        else:
            self.crashed = True  # more unsuccessful collision detection

    def moveup(self):  # pretty obvious what these do
        self.nextX, self.nextY = 0, 1

    def moveleft(self):
        self.nextX, self.nextY = -1, 0

    def moveright(self):
        self.nextX, self.nextY = 1, 0

    def movedown(self):
        self.nextX, self.nextY = 0, -1

    def eatFood(self):
        # adds the next spot without deleting the tail, extending the snake by 1
        self.body.append(Square(self.nextposition[0], self.nextposition[1]))
        self.headposition[0], self.headposition[1] = self.body[-1].x, self.body[-1].y
        self.nextposition = [self.headposition[0] + SIZE * self.nextX, self.headposition[1] + SIZE * self.nextY]

    def drawself(self, turtle):  # draws the whole snake when called
        for segment in self.body:
            segment.drawself(turtle)

class Game:
    def __init__(self):
        # game object has a screen, a turtle, a basic snake and a food
        self.screen = Screen()
        self.artist = Turtle(visible=False)
        self.artist.up()
        self.artist.speed("slowest")

        self.snake = Snake()
        self.food = Food(100, 0)
        self.counter = 0  # this will be used later
        self.commandpending = False  # as will this

        self.screen.tracer(0)  # follow it so far?

        self.screen.listen()
        self.screen.onkey(self.snakedown, "Down")
        self.screen.onkey(self.snakeup, "Up")
        self.screen.onkey(self.snakeleft, "Left")
        self.screen.onkey(self.snakeright, "Right")

        self.create_button()
        self.start_game()

    def create_button(self):
        # Register the "play_button.gif" image as a shape
        self.screen.register_shape("./images/tinywow_playbtn_23882175.gif")

    def start_game(self):
        # Create the button turtle and set its shape
        button_turtle = Turtle(shape="./images/tinywow_playbtn_23882175.gif")
        button_turtle.up()
        button_turtle.goto(0, -100)

        def on_button_click(x, y):
            # Check if the button was clicked
            if button_turtle.distance(x, y) < 50:
                self.screen.onclick(None)  # Disable further click events
                button_turtle.hideturtle()  # Hide the button turtle
                self.nextFrame()  # Start the game

        self.screen.onclick(on_button_click)

    # def start_game(self):
    #     play = self.screen.textinput("Snake Game", "Press Play to start the game")
    #     if play == "Play":
    #         self.nextFrame()
    #     else:
    #         self.screen.bye()

    def nextFrame(self):
        self.artist.clear()

        if (self.snake.nextposition[0], self.snake.nextposition[1]) == (self.food.x, self.food.y):
            self.snake.eatFood()
            self.food.changelocation()
        
        self.snake.moveOneStep()

        self.food.drawself(self.artist)  # show the food and snake
        self.snake.drawself(self.artist)
        self.screen.update()
        self.screen.ontimer(lambda: self.nextFrame(), 100)

    def snakeup(self):
        if not self.commandpending: 
            self.commandpending = True
            self.snake.moveup()
            self.commandpending = False

    def snakedown(self):
        if not self.commandpending:
            self.commandpending = True
            self.snake.movedown()
            self.commandpending = False

    def snakeleft(self):
        if not self.commandpending:
            self.commandpending = True
            self.snake.moveleft()
            self.commandpending = False

    def snakeright(self):
        if not self.commandpending:
            self.commandpending = True
            self.snake.moveright()
            self.commandpending = False

game = Game()

screen = Screen()
screen.bgpic("./images/battleground.png")  # Replace with the path to your background image

screen.ontimer(lambda: game.nextFrame(), 100)

screen.mainloop()