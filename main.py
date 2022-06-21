import pygame
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
import random

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

# Timer
clock = pygame.time.Clock()
currentTime = 100


# Title and Icon
pygame.display.set_caption("Mamad Game")
icon = pygame.image.load('images/logo.png').convert_alpha()
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load('images/background.png').convert()


# Player
playerPosition = [370, 480]
playerMovement = [0, 0]
x = width/2 - 64
y = height/2 - 64
playerImgCrude = pygame.image.load('images/openHand.png').convert_alpha()
playerImg = pygame.transform.scale(playerImgCrude, (128, 128))
player_rect = playerImg.get_rect(topleft=(x, y))


# Insects
InsectX = random.randint(0, 1366)
InsectY = random.randint(0, 768)
InsectImg = pygame.image.load('images/enemy.png').convert_alpha()
InsectImg = pygame.transform.scale(InsectImg, (32, 32))
insect_rect = InsectImg.get_rect(topleft=(InsectX, InsectY))


## Game Texts
 # Score Text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_timer():
    if currentTime/1000 >= 80:
        timer = font.render("Time: " + str(int(101 - currentTime / 1000)), True, (255, 0, 0))
    else:
        timer = font.render("Time: " + str(int(101 - currentTime/1000)), True, (255, 255, 255))
    screen.blit(timer, (1210, 10))


################################################################################################## Game Loop
iteratorX = 0
iteratorY = 0
while True:
    # Game code
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

        # if Keystroke is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerMovement[0] = -15
            if event.key == pygame.K_RIGHT:
                playerMovement[0] = 15
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerMovement[0] = 0
            if event.key == pygame.K_RIGHT:
                playerMovement[0] = 0
    success, frame = cap.read()


    # Mediapipe code for hand detection and Landmarks
    hands, frame = detector.findHands(frame)

    # Landmarks value - (x,y,z) * 21
    if hands:
        #Get the first hand detected
        lmList = hands[0]
        positionOfTheHand = lmList['lmList']
        player_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
        player_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
            # boundaries for hand
        # if player_rect.left >= 932:
        #     player_rect.left = 932
        # elif player_rect.left <= 80:
        #     player_rect.left = 80
        # if player_rect.top >= 560:
        #     player_rect.top = 560
        # elif player_rect.top <= 80:
        #     player_rect.top = 80



    # Opencv Screen
    #frame = cv2.resize(frame, (0, 0), None, 0.3, 0.3)
    cv2.imshow("webcam", frame)

    # Game screen
    # moving the Player
    screen.blit(playerImg, player_rect)

    ## placing Insects
    screen.blit(InsectImg, insect_rect)
    # InsectY += 5
    ## moving Insects

        # moving X
    if insect_rect.right >= width - 32:
        iteratorX = 0
    if insect_rect.right <= 0:
        iteratorX = 1
    if iteratorX == 0:
        insect_rect.right -= 20
    if iteratorX == 1:
        insect_rect.right += 20

        # moving Y
    if insect_rect.top >= height - 32:
        iteratorY = 0
    if insect_rect.top <= 0:
        iteratorY = 1
    if iteratorY == 0:
        insect_rect.top -= 10
    if iteratorY == 1:
        insect_rect.top += 10


    # showing texts
    show_score(textX, textY)
    currentTime = pygame.time.get_ticks()
    show_timer()

    # check collision
    print(player_rect.colliderect(insect_rect))

    # display update
    pygame.display.update()
    clock.tick(60)




