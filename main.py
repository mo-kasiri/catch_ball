import pygame
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector


width = 1366
height = 768

# opencv code
cap = cv2.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)


# Initialize the pygame
pygame.init()

# Define the screen
screen = pygame.display.set_mode((width, height))

# Title and Icon
pygame.display.set_caption("Mamad Game")
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)

# Player
playerImgCrude = pygame.image.load('images/spaceship.png')
playerImg = pygame.transform.scale(playerImgCrude, (64, 64))
#playerX = 370
#playerY = 480
playerPosition = [370, 480]
playerMovement = [0, 0]

def player(playerPosition):
    x = playerPosition[0]
    y = playerPosition[1]
    screen.blit(playerImg, (x, y))


# Enemy
EnemyImg = pygame.image.load('images/fly.png')
EnemyX = 100
EnemyY = 100

def Enemy(x, y):
    screen.blit(EnemyImg, (x, y))



# Game Loop
iteratorX = 0
iteratorY = 0
indexNumber = 1
while True:
    # Game code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        # if Keystroke is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('Left Button has pressed!')
                playerMovement[0] = -15
            if event.key == pygame.K_RIGHT:
                playerMovement[0] = 15
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                # print('Left Button is Up now')
                playerMovement[0] = 0
            if event.key == pygame.K_RIGHT:
                playerMovement[0] = 0
    success, frame = cap.read()
    #print(frame.shape)

    # Mediapipe code for hand detection and Landmarks
    hands, frame = detector.findHands(frame)

    # Landmarks value - (x,y,z) * 21
    if hands:
        #Get the first hand detected
        lmList = hands[0]
        #print(lmList['lmList'])
        #print(lmList['bbox'])
        #print(hands[0])
        positionOfTheHand = lmList['lmList']
        #playerPosition[0] = positionOfTheHand[9][0]
        #playerPosition[1] = positionOfTheHand[9][1]
    # Opencv Screen
    #frame = cv2.resize(frame, (0, 0), None, 0.3, 0.3)
    #cv2.imshow("webcam", frame)

    # Game screen
    screen.fill((50, 10, 100))
    playerPosition[0] += playerMovement[0]
    playerPosition[1] += playerMovement[1]
    # moving the Player
    player(playerPosition)

    ## placing enemies
    Enemy(EnemyX, EnemyY)
    # EnemyY += 5
    ## moving enemies

        # moving X
    if EnemyX >= width - 32:
        iteratorX = 0
    if EnemyX <= 0:
        iteratorX = 1
    if iteratorX == 0:
        EnemyX -= 20
       # EnemyY -= 20
    if iteratorX == 1:
        EnemyX += 20
       # EnemyY -= 20

        # moving Y
    if EnemyY >= height - 32:
        iteratorY = 0
    if EnemyY <= 0:
        iteratorY = 1
    if iteratorY == 0:
        EnemyY -= 10
    if iteratorY == 1:
        EnemyY += 10





    # display update
    pygame.display.update()




