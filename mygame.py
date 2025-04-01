import turtle
import random
import math
import time

# Screen setup
screen = turtle.Screen()
screen.setup(600, 600)  # Larger screen
screen.bgcolor("black")
screen.title("Galactic Tie Fighter Assault")
screen.tracer(0)  # Disable auto-update for smoother animation

# Game variables
score = 0
high_score = 0
game_over = False
level = 1
xf = random.randint(-250, 250)
yf = random.randint(-250, 250)
xr = 0
yr = 0
tie_speed = 5 + level  # Speed increases with level
dx = random.choice([-1, 1]) * tie_speed
dy = random.choice([-1, 1]) * tie_speed
laser_cooldown = 0  # Prevents rapid firing

# Create turtle objects
tie_fighter = turtle.Turtle()
tie_fighter.hideturtle()
tie_fighter.speed(0)

reticle = turtle.Turtle()
reticle.shape("circle")
reticle.color("cyan")  # More visible color
reticle.shapesize(0.8, 0.8)  # Slightly larger
reticle.speed(0)
reticle.penup()

# Score and level display
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-280, 260)

level_display = turtle.Turtle()
level_display.hideturtle()
level_display.color("yellow")
level_display.penup()
level_display.goto(200, 260)

# Laser effects
laser = turtle.Turtle()
laser.hideturtle()
laser.color("red")
laser.speed(0)
laser.pensize(3)

# Explosion effect
explosion = turtle.Turtle()
explosion.hideturtle()
explosion.speed(0)

# Enhanced background with twinkling stars
stars = []
for _ in range(100):
    star = turtle.Turtle()
    star.hideturtle()
    star.penup()
    star.shape("circle")
    star.shapesize(random.uniform(0.05, 0.3))
    star.color("white")
    star.goto(random.randint(-300, 300), random.randint(-300, 300))
    star.speed = random.uniform(0.02, 0.1)
    stars.append(star)

# Draw planet
planet = turtle.Turtle()
planet.hideturtle()
planet.penup()
planet.goto(random.randint(-200, 200), random.randint(-200, 200))
planet.color("blue")
planet.shapesize(3)
planet.dot(80, "navy")

def draw_tie_fighter(x, y):
    """Draws a more detailed Tie Fighter"""
    tie_fighter.clear()
    tie_fighter.penup()
    tie_fighter.goto(x, y)
    
    # Main cockpit
    tie_fighter.dot(25, "darkgray")
    tie_fighter.dot(20, "gray")
    
    # Wings
    tie_fighter.pensize(3)
    tie_fighter.pencolor("darkgray")
    tie_fighter.setheading(90)
    
    for _ in range(2):  # Draw both wings
        tie_fighter.penup()
        tie_fighter.goto(x + 25 if _ == 0 else x - 25, y)
        tie_fighter.pendown()
        tie_fighter.forward(50)
        tie_fighter.backward(100)
        tie_fighter.forward(50)
        
        # Wing details
        tie_fighter.penup()
        tie_fighter.goto(x + 15 if _ == 0 else x - 15, y - 30)
        tie_fighter.pendown()
        tie_fighter.goto(x + 15 if _ == 0 else x - 15, y + 30)

def fire_laser():
    """Enhanced laser firing with cooldown and sound effect"""
    global laser_cooldown, score
    
    if game_over or laser_cooldown > 0:
        return
    
    # Play sound (if using pygame)
    # pygame.mixer.Sound("laser.wav").play()
    
    # Draw laser with animation
    laser.clear()
    laser.penup()
    laser.goto(xr, yr)
    
    # Pulsing laser effect
    for size in [15, 20, 15]:
        laser.clear()
        for angle in [0, 45, 90, 135]:
            laser.setheading(angle)
            laser.pendown()
            laser.forward(size)
            laser.backward(size)
            laser.penup()
        screen.update()
        time.sleep(0.03)
    
    # Hit detection with visual feedback
    distance = math.sqrt((xf - xr)**2 + (yf - yr)**2)
    if distance < 40:  # Larger hit area
        score += level  # More points at higher levels
        create_explosion(xf, yf)
        reset_tie_fighter()
        update_displays()
        
        if score >= level * 3:  # More hits needed at higher levels
            level_up()
    
    laser_cooldown = 10  # Cooldown frames

def create_explosion(x, y):
    """Creates an explosion animation at given coordinates"""
    explosion.clear()
    explosion.penup()
    explosion.goto(x, y)
    
    colors = ["red", "orange", "yellow"]
    for size in range(5, 35, 5):
        explosion.dot(size, colors[size % 3])
        screen.update()
        time.sleep(0.05)
    
    explosion.clear()

def reset_tie_fighter():
    """Resets the Tie Fighter at a random position"""
    global xf, yf, dx, dy, tie_speed
    xf = random.randint(-250, 250)
    yf = random.randint(-250, 250)
    dx = random.choice([-1, 1]) * tie_speed
    dy = random.choice([-1, 1]) * tie_speed

def level_up():
    """Increases difficulty level"""
    global level, tie_speed, game_over
    level += 1
    tie_speed = 5 + level
    
    # Show level up message
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("yellow")
    msg.penup()
    msg.goto(0, 0)
    msg.write(f"LEVEL {level}", align="center", font=("Arial", 24, "bold"))
    screen.update()
    time.sleep(1.5)
    msg.clear()
    
    update_displays()

def update_displays():
    """Updates all on-screen information"""
    score_display.clear()
    score_display.write(f"Score: {score}  High: {high_score}", font=("Courier", 14, "bold"))
    
    level_display.clear()
    level_display.write(f"Level: {level}", font=("Courier", 14, "bold"))

def display_game_over():
    """Enhanced game over screen"""
    global game_over, high_score
    
    if score > high_score:
        high_score = score
    
    screen.bgcolor("darkred")
    reticle.hideturtle()
    tie_fighter.hideturtle()
    
    # Game over text
    go = turtle.Turtle()
    go.hideturtle()
    go.color("white")
    go.penup()
    go.goto(0, 50)
    go.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    
    # Stats
    go.goto(0, 0)
    go.write(f"Final Score: {score}", align="center", font=("Arial", 18))
    go.goto(0, -30)
    go.write(f"High Score: {high_score}", align="center", font=("Arial", 18))
    go.goto(0, -80)
    go.write("Press SPACE to restart", align="center", font=("Arial", 14))
    
    screen.update()

def restart_game():
    """Resets the game state"""
    global score, level, game_over, tie_speed, laser_cooldown
    
    # Clear screen
    for t in screen.turtles():
        t.clear()
    
    # Reset game state
    score = 0
    level = 1
    game_over = False
    tie_speed = 5 + level
    laser_cooldown = 0
    
    # Reset background
    screen.bgcolor("black")
    for star in stars:
        star.color("white")
    
    # Reset displays
    update_displays()
    
    # Reset objects
    reticle.showturtle()
    reticle.goto(0, 0)
    reset_tie_fighter()
    
    # Restart game loop
    main_loop()

# Movement and controls
def move_up():
    global yr
    if not game_over:
        yr += 15
        if yr > 290:
            yr = -290
        reticle.goto(xr, yr)

def move_down():
    global yr
    if not game_over:
        yr -= 15
        if yr < -290:
            yr = 290
        reticle.goto(xr, yr)

def move_left():
    global xr
    if not game_over:
        xr -= 15
        if xr < -290:
            xr = 290
        reticle.goto(xr, yr)

def move_right():
    global xr
    if not game_over:
        xr += 15
        if xr > 290:
            xr = -290
        reticle.goto(xr, yr)

# Set up controls
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_laser, "space")
screen.onkeypress(restart_game, "r")
screen.listen()

# Twinkling stars effect
def twinkle_stars():
    for star in stars:
        if random.random() < 0.02:  # 2% chance to twinkle
            star.color(random.choice(["white", "yellow", "lightblue"]))
            screen.ontimer(lambda s=star: s.color("white"), random.randint(200, 1000))

# Main game loop
def main_loop():
    global xf, yf, dx, dy, laser_cooldown
    
    if not game_over:
        # Move tie fighter
        xf += dx
        yf += dy
        
        # Bounce off walls with random angle changes
        if xf > 290 or xf < -290:
            dx *= -1
            dy = random.choice([-1, 1]) * tie_speed * random.uniform(0.8, 1.2)
        if yf > 290 or yf < -290:
            dy *= -1
            dx = random.choice([-1, 1]) * tie_speed * random.uniform(0.8, 1.2)
        
        # Random direction changes
        if random.random() < 0.02:
            dx = random.choice([-1, 1]) * tie_speed * random.uniform(0.8, 1.2)
            dy = random.choice([-1, 1]) * tie_speed * random.uniform(0.8, 1.2)
        
        # Update positions
        draw_tie_fighter(xf, yf)
        
        # Cooldown timer
        if laser_cooldown > 0:
            laser_cooldown -= 1
        
        # Twinkling stars
        if random.random() < 0.1:
            twinkle_stars()
        
        screen.update()
    
    # Continue the game loop
    if not game_over:
        screen.ontimer(main_loop, 30)  # ~33 FPS

# Initial setup
update_displays()
reticle.goto(xr, yr)
main_loop()

turtle.done()