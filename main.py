# Space Invaders Game.

import turtle
import winsound
import math
import random

#Set up the screen.
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")

#Register the shapes with Turtle.
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

#Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range (4):
    border_pen.fd(600)
    border_pen.lt(90)
#border_pen.hideTurtle()

#Set the score in game.
score = 0

#Draw the score.
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s"%score
score_pen.write(scorestring, False, align="left", font=("Arial",14, "normal"))
score_pen.hideturtle()

#Create the player turtle.
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

#Create movement with arrow keys.
playerspeed = 30

def move_left():
    x = player.xcor() #This is where the player is.
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    #Declare bulletstate as a global because it needs to reflect upon the global variable.
    global bulletstate

    if bulletstate == "ready":
        bulletstate = "fire"
        #When we fire the bullet, we need to set the bullet just above the player.
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        #Add sound when firing bullet.
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC)

#Determine if the bullet hits an enemy. Use pythagorean theorem.
def isCollision(t1 , t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

#Need to create the player's "bullet" that can shoot at the invaders.
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()
bulletspeed = 20

#Need to define bullet state.
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Create the bindings for the arrow keys.
turtle.listen()
turtle.onkey(move_left, "Left") #Hit the left arrow key, will move player left.
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#Choose the number of Space Invaders.
number_of_enemies = 5
enemies = []
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    #Time to create some invaders.
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200,200)
    y = random.randint(100,250)
    enemy.setposition(x, y)

enemyspeed = 2

#Main game loop. Logic or enemy.
while True:

    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #boundary check the enemy
        if enemy.xcor() > 280:
            #Move all the enemies down.
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #Change enemy direction.
            enemyspeed *= -1

        if enemy.xcor() < -280:
            #Move all the enemies down.
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #Change enemy direction.
            enemyspeed *= -1

        # Collision detection between enemy and bullet.
        if isCollision(bullet, enemy):
            # Need to reset the bullet.
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy.
            x = random.randint(-200,200)
            y = random.randint(100,250)
            enemy.setposition(x, y)
            # Update the score on bullet/enemy collision.
            score += 10
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            #Add the sound when collision between enemy and bullet.
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)

        # Check if the enemy collides with the player.
        if isCollision(player, enemy):
            #Add the sound when collision between enemy and player.
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    #Move the bullet.
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #Border check the bullet.
    if bullet.ycor() > 280:
        bullet.hideturtle()
        bulletstate = "ready"


#need to loop so screen doesn't disppear.
wn.mainloop()