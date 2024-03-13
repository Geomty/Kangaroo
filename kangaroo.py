# Import modules
from graphics import *
import random
import time

# Define variables

# Jump height set by the user in the entry box
height = 10
# Prevents a background animation that changes the time of day to the
# same time of day
day = True
# Keeps track of which obstacle is supposed to go in front of the other
# Also printed out once the loop ends
count = 0

# Define functions

def drawFill(obj, color):
    """Draw an inputted graphics object and set the fill and outline
       to an inputted color"""
    obj.draw(win)
    obj.setFill(color)
    obj.setOutline(color)

def quadratic(x):
    """Input is an x coordinate, output is the respective y coordinate
       for the parabola that the kangaroo follows"""
    # Calculate the a value of a parabola in vertex form
    # (y = a(x - h)^2 + k) using the vertex (320, (257 - 17.7 * height))
    # and the point (132, -257)

    # (0, 0) is in the top left of the window, meaning the parabola
    # exists in the fourth quadrant, hence the negative y-values

    # The (257 - 17.7 * height) calculation ensures a custom height of 0
    # keeps the kangaroo on the ground, and the default height of 10
    # looks nice enough proportionally to be the default

    # -257 = a(132 - 320)^2 - (257 - 17.7 * height)
    # a(132 - 320)^2 = -257 + (257 - 17.7 * height)

    a = (-257 + (257 - 17.7 * height)) / ((132 - 320) ** 2)
    # The actual parabolic function
    y = a * ((x - 320) ** 2) - (257 - 17.7 * height)
    # The parabola exists in the fourth quadrant, but the window has only positive coordinates
    y = y * -1
    return y

def jump():
    """Procedural function, make the kangaroo jump by following a
       parabola until it touches the ground again"""
    # While the kangaroo hasn't reached its final position
    while kangaroo.getAnchor().getX() < 508:
        # Calculate the new y coordinate
        y = quadratic(kangaroo.getAnchor().getX() + 8)
        # Move function takes in how much it moves by, not the new
        # coordinates
        kangaroo.move(8, y - kangaroo.getAnchor().getY())
        time.sleep(0.01)
        # Always check for text input
        changeHeight()

def fade():
    """Check if the last click was within the left or right box and fade
       the background to yellow or black respectively. If not, begin the
       process for stopping the loop and closing the window."""
    global day
    click = win.checkMouse()
    if not click == None:
        x = click.getX()
        y = click.getY()
        # Day button
        if 500 <= x <= 555 and 325 <= y <= 350 and day == False:
            day = True
            # Since day is now true, fade to yellow
            for i in range(0, 251, 5):
                # Yellow is #FFFF00, black is #000000
                win.setBackground(color_rgb(i, i, 0))
                time.sleep(0.01)
                # Always check for text input
                changeHeight()
        # Night button
        elif 570 <= x <= 625 and 325 <= y <= 350 and day == True:
            day = False
            # Since day is now false, fade to black
            for i in range(250, -1, -5):
                win.setBackground(color_rgb(i, i, 0))
                time.sleep(0.01)
                changeHeight()
        else:
            # Notify the while loop at the endthat the click is outside
            # of the boxes
            return True
        return False

def pan():
    """Procedural function, move the kangaroo and two obstacles left until
       the kangaroo reaches its original position, and move the obstacle
       that is off screen to the left over to off screen to the right"""
    global count
    # While the kangaroo hasn't reached its starting point
    while kangaroo.getAnchor().getX() > 132:
        kangaroo.move(-8, 0)
        obstacle1.move(-8, 0)
        obstacle2.move(-8, 0)
        time.sleep(0.01)
        # Always check for text input
        changeHeight()
    # Obstacle 1 goes in front of obstacle 2 every other time and vice versa
    if count % 2 == 0:
        obstacle1.move(752, 0)
    else:
        obstacle2.move(752, 0)
    count += 1

def changeHeight():
    """Procedural function, change the height of the kangaroo's jumps
       based on the number in the entry box"""
    global height
    global obstacle1
    global obstacle2
    
    text = entry.getText()
    # Check if the text is a new number
    if text.isdigit() and not int(text) == height:
        height = int(text)

        # Replace the obstacles with a shorter/taller version depending on the new height
        # The obstacles have a pixel height of 135 with a default height of 10
        p1 = obstacle1.getP1()
        obstacle1.undraw()
        obstacle1 = Rectangle(Point(p1.getX(), 315 - 13.5 * height), Point(p1.getX() + 80, 315))
        drawFill(obstacle1, "saddle brown")

        p2 = obstacle2.getP1()
        obstacle2.undraw()
        obstacle2 = Rectangle(Point(p2.getX(), 315 - 13.5 * height), Point(p2.getX() + 80, 315))
        drawFill(obstacle2, "saddle brown")

# Draw the graphics        

# Create the yellow window
win = GraphWin("Kangaroo!", 640, 360)
win.setBackground("yellow")

# Draw 50 yellow stars at random positions
for i in range(50):
    x = random.randint(0, 640)
    y = random.randint(0, 315)
    star = Point(x, y)
    drawFill(star, "yellow")

# Draw the orange ground
ground = Rectangle(Point(0, 315), Point(640, 360))
drawFill(ground, "orange")

# Draw the first brown obstacle
obstacle1 = Rectangle(Point(280, 180), Point(360, 315))
drawFill(obstacle1, "saddle brown")

# Draw the second obstacle off-screen
obstacle2 = Rectangle(Point(656, 180), Point(736, 315))
drawFill(obstacle2, "saddle brown")

# Draw the kangaroo
kangaroo = Image(Point(132, 257), "kangaroo.gif")
kangaroo.draw(win)

# Draw the entry object and its label
entry = Entry(Point(105, 338), 5)
entry.draw(win)
entry.setText("10")

entryLabel = Text(Point(45, 338), "Height:")
entryLabel.draw(win)
entryLabel.setSize(14)

# Draw the day button and its label
dayBox = Rectangle(Point(500, 325), Point(555, 350))
drawFill(dayBox, "gray")

dayLabel = Text(Point(527, 338), "Day")
dayLabel.draw(win)
dayLabel.setSize(12)

# Draw the night button and its label
nightBox = Rectangle(Point(570, 325), Point(625, 350))
drawFill(nightBox, "gray")

nightLabel = Text(Point(598, 338), "Night")
nightLabel.draw(win)
nightLabel.setSize(12)

# Draw text instructing how to close the window
instructions = Text(Point(90, 15), "Click anywhere to close")
instructions.draw(win)
instructions.setSize(12)

# Run the animation
while True:
    jump()
    pan()
    clickedWin = fade()
    # Stop the animation if the user clicked outside of the boxes
    if clickedWin:
        win.close()
        # Print the number of times the kangaroo has jumped
        print("Number of jumps:", count)
        break
