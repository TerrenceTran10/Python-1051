import pygame

pygame.init()
pygame.display.set_caption("Pong!")

width = 1000
height = 700
window = pygame.display.set_mode((width, height))
FPS = 110

white = (255, 255, 255)
aqua = (0, 255, 255)
black = (0, 0, 0)

paddleWidth = 10
paddleHeight = 120
ballRadius = 15

scoreFont = pygame.font.SysFont("arial", 75)
gameWinMessage = pygame.font.SysFont("arial", 25)
winningScore = 7

class Paddle:
    color = aqua
    velocity = 4
    def __init__(self, x, y, width, height):
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up = True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY

class Ball:
    maxVelocity = 5
    ballColor = aqua

    def __init__(self, x, y, radius):
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.radius = radius
        self.x_velocity = self.maxVelocity
        self.y_velocity = 0

    def draw(self,window):
        pygame.draw.circle(window,self.ballColor, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY
        self.y_velocity = 0
        self.x_velocity *= -1


def draw(window, paddles, ball, leftScore, rightScore):
    window.fill(black)

    leftText = scoreFont.render(f"{leftScore}", 1, aqua)
    rightText = scoreFont.render(f"{rightScore}", 1, aqua)
    window.blit(leftText, (width//4 - leftText.get_width()//2, 15))
    window.blit(rightText, (width * (3/4) - rightText.get_width()//2, 15))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, height, height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, aqua, (width//2 - 5, i, 10, height//20))
    ball.draw(window)
    pygame.display.update()

def paddleMoving(keys, leftPaddle, rightPaddle):
    if keys[pygame.K_w] and leftPaddle.y - leftPaddle.velocity >= 0:
        leftPaddle.move(up = True)
    if keys[pygame.K_s] and leftPaddle.y + leftPaddle.velocity + leftPaddle.height <= height:
        leftPaddle.move(up = False)

    if keys[pygame.K_UP] and rightPaddle.y - rightPaddle.velocity >= 0:
        rightPaddle.move(up = True)
    if keys[pygame.K_DOWN] and rightPaddle.y + rightPaddle.velocity + rightPaddle.height <= height:
        rightPaddle.move(up = False)


def ballHitting(ball, leftPaddle, rightPaddle):
    if ball.y + ball.radius >= height:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= leftPaddle.y and ball.y <= leftPaddle.y + leftPaddle.height:
            if ball.x - ball.radius <= leftPaddle.x + leftPaddle.width:
                ball.x_velocity *= -1

                middleY = leftPaddle.y + leftPaddle.height/2
                differenceInY = middleY - ball.y
                reductionFactor = (leftPaddle.height / 2) / ball.maxVelocity
                y_velocity = differenceInY / reductionFactor
                ball.y_velocity = y_velocity * -1
    else:
        if ball.y >= rightPaddle.y and ball.y <= rightPaddle.y + rightPaddle.height:
            if ball.x + ball.radius >= rightPaddle.x:
                ball.x_velocity *= -1

                middleY = rightPaddle.y + rightPaddle.height / 2
                differenceInY = middleY - ball.y
                reductionFactor = (rightPaddle.height / 2) / ball.maxVelocity
                y_velocity = differenceInY / reductionFactor
                ball.y_velocity = y_velocity * -1


def main():
    run = True
    clock = pygame.time.Clock()

    leftPaddle = Paddle(10, height//2 - paddleHeight//2, paddleWidth, paddleHeight)
    rightPaddle = Paddle(width - 10 - paddleWidth, height//2 - paddleHeight//2, paddleWidth, paddleHeight)

    ball = Ball(width//2, height//2, ballRadius)
    leftScore = 0
    rightScore = 0

    while run:
        clock.tick(FPS)
        draw(window, [leftPaddle, rightPaddle], ball, leftScore, rightScore)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        paddleMoving(keys, leftPaddle, rightPaddle)

        ball.move()
        ballHitting(ball, leftPaddle, rightPaddle)

        if ball.x < 0:
            rightScore += 1
            ball.reset()
        elif ball.x > width:
            leftScore += 1
            ball.reset()

        won = False
        if leftScore >= winningScore:
            won = True
            ENDOFGAMEText = "Left player wins, right player is bad at the game!"
        elif rightScore >= winningScore:
            win = True
            ENDOFGAMEText = "Right player wins, left player is bad at the game!"

        if won:
            text = gameWinMessage.render(ENDOFGAMEText, 1, aqua)
            window.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(7000)
            leftPaddle.reset()
            rightPaddle.reset()
            ball.reset()
            leftScore = 0
            rightScore = 0

    pygame.quit()

main()